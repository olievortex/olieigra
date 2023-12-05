"""CLI for performing qa analysis on Igra2 files"""
import math
import os
from datetime import datetime
import olieigra


class QualityAnalysis(olieigra.Callbacks):
    """Contain the callback states"""

    def __init__(self, dst_path: str, min_effective_date: datetime):
        super().__init__()
        self.min_effective_date = min_effective_date
        self.dst_path = dst_path
        self.filename = ""
        self.filtered = 0
        self.writer = None

    def start_file(self, filename: str) -> bool:
        """Decide if we want to process the file. If so, reset state and start writing to a
        temporary file."""

        # An IGRA2 file should end with -data.txt
        if not filename.endswith('-data.txt'):
            print(f'Skipping {filename}. Not sure what to do with it.')
            return False

        # Set the desired destination filename
        dst_filename = f'{self.dst_path}/{filename}'
        dst_filename = dst_filename.replace("-data.txt", "-data-qa.csv")

        # Skip this file if it has already been processed
        if os.path.exists(dst_filename):
            print(f'Skipping {filename}. Destination file already exists.')
            return False

        # If we got here, we are going to process the file
        print(f'Processing {filename}.')

        # Write to a temp file
        self.filename = dst_filename.replace('-data-qa.csv', '-data-qa.partial.csv')
        self.writer = open(self.filename, 'w', encoding='UTF-8')

        # Reset the filtered record count
        self.filtered = 0

        # Write the header row
        self.writer.write('id,effective_date,hour,has_surface,usable_count\n')

        # Tell olieigra to continue processing
        return True

    def finish_file(self, headers: int, rows: int):
        """File processing is complete. Clean up and provide user feedback."""

        # Close the temporary file
        self.writer.close()

        # Rename the temporary file
        dst_renamed = self.filename.replace('.partial.csv', '.csv')
        os.rename(self.filename, dst_renamed)

        # Calculate the number of records written
        loaded = headers - self.filtered

        # Provide feedback to the user
        print(f" Read {headers} headers, {rows} lines. Filtered {self.filtered}. " +
              f"Wrote {loaded} records.")

    def parse_header(self, header: olieigra.HeaderModel) -> bool:
        """Transform the header record and start writing a record"""

        # Combine the separate fields into a date
        effective_date = datetime(header.year, header.month, header.day)

        # Skip the record if it is too old
        if effective_date < self.min_effective_date:
            self.filtered += 1
            return False

        # Start writing a line to the temp file
        self.writer.write(f'{header.id},{effective_date:%Y-%m-%d},{header.hour},')

        # Tell olieigra to process the body associated with this header
        return True

    def parse_body(self, body: list[olieigra.BodyModel]):
        """Perform some analytics and finish writing a record"""

        # Initialize
        usable_count = 0
        surface_nan = 1

        # Iterate through each record in the body
        for item in body:
            # We don't care about non-pressure records
            if item.type[0] == '3':
                continue

            # We don't care about records higher than 10km
            if item.gph > 10000:
                continue

            # We don't care about records that contain a NaN value
            if math.isnan(item.dpdp) | math.isnan(item.rh) | math.isnan(item.temp) | \
                    math.isnan(item.wdir) | math.isnan(item.wspd) | math.isnan(item.gph):
                continue

            # Flag when we find a surface record
            if item.type == '21':
                surface_nan = 0

            # If we got here, the record is usable
            usable_count += 1

        # Finish writing the record in the temporary file
        self.writer.write(f'{surface_nan},{usable_count}\n')


if __name__ == '__main__':
    # Constants to our source and destination folders
    SRC_PATH = 'C:/Users/oliev/Downloads'
    DST_PATH = 'C:/Users/oliev/Downloads/silver'

    # Set up for processing
    callbacks = QualityAnalysis(DST_PATH, datetime(2000, 1, 1))
    reader = olieigra.Reader(callbacks=callbacks)
    crawler = olieigra.Crawler(reader=reader)

    # Crawl and process files
    crawler.crawl(SRC_PATH)
