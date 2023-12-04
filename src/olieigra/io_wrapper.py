"""Wrapper class for IO to make unit tests easier to write"""
import io
import os

from typing import IO
from zipfile import ZipFile


class IOWrapper:
    """Wrapper class for IO to make unit tests easier to write"""

    def list_dir(self, path: str) -> list[str]:
        """Wrapper for os.listdir"""
        return os.listdir(path)

    def open_archive(self, archive: str) -> ZipFile:
        """Open a zip file"""
        return ZipFile(archive, "r")

    def open_archive_file(self, archive: ZipFile, filename: str) -> IO[bytes]:
        """Return a binary stream of a file from an archive"""
        return archive.open(filename, "r")

    def read_as_text(self, stream: IO[bytes]) -> io.TextIOWrapper:
        """Convert a binary stream into a text stream"""
        return io.TextIOWrapper(stream, encoding='UTF-8')

    def open_file(self, filename: str) -> io.TextIOWrapper:
        """Return a text reader for the given file"""
        return open(filename, 'r', encoding='UTF-8')
