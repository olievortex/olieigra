"""CLI for performing qa analysis on Igra2 files"""
import io
import math
import os
from datetime import datetime
from dataclasses import dataclass
from src import olieigra

SRC_PATH = 'C:/Users/oliev/Downloads'
DST_PATH = 'C:/Users/oliev/Downloads/silver'


@dataclass
class WriterState():
    """POCO to keep track of header state"""
    filtered: int
    hout: str
    filepath: str
    writer: io.TextIOWrapper


class QualityAnalysis(olieigra.Callbacks):
    """Contain the callback states"""

    def __init__(self, min_effective_date: datetime):
        super().__init__()
        self.min_effective_date = min_effective_date
        self.state = WriterState(0, "", "", None)

    def start_file(self, filename: str) -> bool:
        """Decide if we want to process the file"""
        if not filename.endswith('-data.txt'):
            print(f'Skipping {filename}. Not sure what to do with it.')
            return False

        dst_filename = filename.replace("-data.txt", "-data-qa.csv")
        dst_filepath = f'{DST_PATH}/{dst_filename}'

        if os.path.exists(dst_filepath):
            print(f'Skipping {filename}. Destination file already exists.')
            return False

        print(f'Processing {filename}.')

        dst_filename = filename.replace("-data.txt", "-data-qa.partial.csv")
        dst_filepath = f'{DST_PATH}/{dst_filename}'

        self.state = WriterState(
            0,
            "",
            dst_filepath,
            open(dst_filepath, "w", encoding='UTF-8')
        )

        self.state.writer.write(
            'id,effective_date,hour,usable_count\n')

        return True

    def finish_file(self, headers: int, rows: int):
        """Callback for when processing is complete"""
        self.state.writer.close()

        dst_renamed = self.state.filepath.replace('.partial.csv', '.csv')
        os.rename(self.state.filepath, dst_renamed)

        loaded = headers - self.state.filtered

        print(f" Read {headers} headers, {rows} lines. Filtered {self.state.filtered}. " +
              f"Wrote {loaded} records.")

    def parse_header(self, header: olieigra.HeaderModel) -> bool:
        """Write the header portion of the line"""
        effective_date = datetime(header.year, header.month, header.day)

        if effective_date < self.min_effective_date:
            self.state.filtered += 1
            return False

        self.state.hout = f'{header.id},{effective_date:%Y-%m-%d},{header.hour}'

        return True

    def parse_body(self, body: list[olieigra.BodyModel]):
        """Perform some analytics"""
        usable_count = 0
        surface_nan = 1

        for item in body:
            if item.type[0] == '3':
                continue

            if item.gph > 10000:
                continue

            if math.isnan(item.dpdp) | math.isnan(item.rh) | math.isnan(item.temp) | \
                    math.isnan(item.wdir) | math.isnan(item.wspd) | math.isnan(item.gph):
                continue

            if item.type == '21':
                surface_nan = 0

            usable_count += 1

        self.state.writer.write(
            f'{self.state.hout},{surface_nan},{usable_count}\n')


if __name__ == '__main__':
    callbacks = QualityAnalysis(datetime(2000, 1, 1))
    reader = olieigra.Reader(callbacks=callbacks)
    crawler = olieigra.Crawler(reader=reader)

    crawler.crawl(SRC_PATH)
