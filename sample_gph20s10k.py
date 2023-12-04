"""CLI for performing qa analysis on Igra2 files"""
import io
import math
import os
from datetime import datetime
from dataclasses import dataclass
import numpy as np
from src import olieigra

SRC_PATH = 'C:/Users/oliev/Downloads'
DST_PATH = 'C:/Users/oliev/Downloads/silver'


@dataclass
class WriterState():
    """Keep track of running state"""
    filtered: int
    rejected: int
    hout: str
    filepath: str
    writer: io.TextIOWrapper
    levels: list[float]


class GphTwentySurfaceToTenK(olieigra.Callbacks):
    """Contain the callback states"""

    def __init__(self, min_effective_date: datetime):
        super().__init__()
        self.min_effective_date = min_effective_date
        self.state = WriterState(0, 0, "", "", None, [])
        self.attr = ['gph','pres','temp','dp','u','v']

    def start_file(self, filename: str) -> bool:
        """Decide if we want to process the file"""
        if not filename.endswith('-data.txt'):
            print(f'Skipping {filename}. Not sure what to do with it.')
            return False

        dst_filename = filename.replace('.txt', '-gph20s10k.csv')
        dst_filepath = f'{DST_PATH}/{dst_filename}'

        if os.path.exists(dst_filepath):
            print(f'Skipping {filename}. Destination file already exists.')
            return False

        print(f'Processing {filename}.')

        dst_filename = filename.replace('.txt', '-gph20s10k.partial.csv')
        dst_filepath = f'{DST_PATH}/{dst_filename}'

        self.state = WriterState(
            0,
            0,
            "",
            dst_filepath,
            open(dst_filepath, "w", encoding='UTF-8'),
            []
        )

        return True

    def finish_file(self, headers: int, rows: int):
        """Callback for when processing is complete"""
        self.state.writer.close()

        dst_renamed = self.state.filepath.replace('.partial.csv', '.csv')
        os.rename(self.state.filepath, dst_renamed)

        loaded = headers - self.state.filtered - self.state.rejected

        print(f" Read {headers} headers, {rows} lines. Filtered {self.state.filtered}. " +
              f"Rejected {self.state.rejected}. Wrote {loaded} records.")

    def parse_header(self, header: olieigra.HeaderModel):
        """Write the header portion of the line"""
        effective_date = datetime(header.year, header.month, header.day)

        if effective_date < self.min_effective_date:
            self.state.filtered += 1
            return False

        day_num = -math.cos(math.radians(effective_date.timetuple().tm_yday))
        self.state.hout = f'{header.id},{effective_date:%Y-%m-%d},{header.hour},{day_num:.2f}'

        return True

    def parse_body(self, body: list[olieigra.BodyModel]):
        """Perform some analytics"""
        filtered = self.filter_body(body)

        if len(filtered) == 0:
            self.state.rejected += 1
            return

        if len(self.state.levels) == 0:
            self.state.levels = np.linspace(filtered[0][0], 10000, 21)
            dynamic = ','.join([f'{level}_{x}'
                                for level in range(len(self.state.levels)) for x in self.attr])
            self.state.writer.write(f"id,effective_date,hour,day_num,{dynamic}\n")

        pivoted = self.body_pivot(filtered)
        out = ','.join([f"{item:.1f}" for item in pivoted])
        self.state.writer.write(f'{self.state.hout},{out}\n')

    def filter_body(self, body: list[olieigra.BodyModel]) -> list[list[float]]:
        """Filter out bad data"""
        result = [[], [], [], [], [], []]
        usable_count = 0
        surface_nan = 1
        last_gph = -1

        for item in body:
            if last_gph >= 10000:
                break

            if item.type[0] == '3':
                continue

            if math.isnan(item.dpdp) | math.isnan(item.rh) | math.isnan(item.temp) | \
                    math.isnan(item.wdir) | math.isnan(item.wspd) | math.isnan(item.gph):
                continue

            result.append(self.transform_body(item, result))

            if item.type == '21':
                surface_nan = 0

            last_gph = item.gph
            usable_count += 1

        if usable_count >= 20 and surface_nan == 0 and last_gph >= 10000:
            return result
        else:
            return []

    def transform_body(self, item: olieigra.BodyModel, agg: list[list[float]]):
        """Transform the body"""
        wrad = math.radians(item.wdir)

        agg[0].append(item.gph)
        agg[1].append(item.pres / 100.0)
        agg[2].append(item.temp / 10.0)
        agg[3].append((item.temp - item.dpdp) / 10.0)
        agg[4].append(-item.wspd * math.sin(wrad) / 10.0)
        agg[5].append(-item.wspd * math.cos(wrad) / 10.0)

    def body_pivot(self, body: list[list[float]]) -> list[float]:
        """Pivot and interpolate the levels"""
        return [np.interp(level, body[0], x)
                for level in self.state.levels
                for x in [body[0], body[1], body[2], body[3], body[4], body[5]]]


if __name__ == '__main__':
    callbacks = GphTwentySurfaceToTenK(datetime(2000, 1, 1))
    reader = olieigra.Reader(callbacks=callbacks)
    crawler = olieigra.Crawler(reader=reader)

    crawler.crawl(SRC_PATH)
