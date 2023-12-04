"""Crawl a directory to search for Igra2 files within archives and process them."""
from zipfile import ZipFile

from .io_wrapper import IOWrapper
from .reader import Reader


class Crawler:
    """Crawl a directory to search for Igra2 files within archives and process them."""

    def __init__(self, reader=Reader(), io=IOWrapper()):
        self.io = io
        self.reader = reader
        self.callbacks = reader.callbacks

    def crawl(self, path: str):
        """Crawl a directory to search for Igra2 files within archives and process them."""
        for filename in self.io.list_dir(path):
            self.process_file(path, filename)

    def process_file(self, path: str, filename: str):
        """Figure out what to do with the file based on type"""
        if filename.endswith('.zip'):
            self.crawl_archive(path, filename)
        else:
            if self.callbacks.start_file(filename):
                self.process_igra2_file(path, filename)

    def crawl_archive(self, path: str, archive_filename: str):
        """Crawl through a zip file"""
        archive = self.io.open_archive(f'{path}/{archive_filename}')

        for file in archive.filelist:
            if self.callbacks.start_file(file.filename):
                self.process_igra2_archive_file(archive, file.filename)

        archive.close()

    def process_igra2_archive_file(self, archive: ZipFile, filename: str):
        """Read an igra2 file from a zip file"""
        reader = self.io.open_archive_file(archive, filename)
        headers, rows = self.reader.read_from_stream(reader)
        reader.close()

        self.callbacks.finish_file(headers, rows)

    def process_igra2_file(self, path: str, filename: str):
        """Read an igra2 file"""
        reader = self.io.open_file(f'{path}/{filename}')
        headers, rows = self.reader.read_from_stream(reader)
        reader.close()

        self.callbacks.finish_file(headers, rows)
