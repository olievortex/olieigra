"""Unit tests for module igra2_body_crawler"""
import unittest
from unittest.mock import MagicMock
from zipfile import ZipInfo
from src import olieigra
from src.olieigra.io_wrapper import IOWrapper


class CrawlerTests(unittest.TestCase):
    """Unit tests for module igra2_body_crawler"""

    def test_crawl_iterates_success(self):
        """Confirm crawl iterates over a list of filenames"""
        # arrange
        wrapper = IOWrapper()
        wrapper.list_dir = MagicMock(return_value=['a', 'b', 'c'])
        crawler = olieigra.Crawler(io=wrapper)
        crawler.process_file = MagicMock()

        # act
        crawler.crawl('')

        # assert
        wrapper.list_dir.assert_called_once()
        self.assertEqual(3, crawler.process_file.call_count)

    def test_crawl_nop_empty(self):
        """Confirm crawl exits gracefully if no files"""
        # arrange
        wrapper = IOWrapper()
        wrapper.list_dir = MagicMock(return_value=[])
        crawler = olieigra.Crawler(io=wrapper)
        crawler.process_file = MagicMock()

        # act
        crawler.crawl('')

        # assert
        wrapper.list_dir.assert_called_once()
        crawler.process_file.assert_not_called()

    def test_processfile_processesfile_callbacktrue(self):
        """Process a file if the callback returns true"""
        # arrange
        callbacks = olieigra.Callbacks()
        callbacks.start_file = MagicMock(return_value=True)
        reader = olieigra.Reader(callbacks=callbacks)
        crawler = olieigra.Crawler(reader=reader)
        crawler.process_igra2_file = MagicMock()

        # act
        crawler.process_file('/some/random/path', 'dillon.txt')

        # assert
        callbacks.start_file.assert_called_once_with("dillon.txt")
        crawler.process_igra2_file.assert_called_once()

    def test_processfile_skipsfile_callbackfalse(self):
        """Skip a file if the callback returns false"""
        # arrange
        callbacks = olieigra.Callbacks()
        callbacks.start_file = MagicMock(return_value=False)
        reader = olieigra.Reader(callbacks=callbacks)
        crawler = olieigra.Crawler(reader=reader)
        crawler.process_igra2_file = MagicMock()

        # act
        crawler.process_file('/some/random/path', 'dillon.txt')

        # assert
        callbacks.start_file.assert_called_once_with("dillon.txt")
        crawler.process_igra2_file.assert_not_called()

    def test_processfile_processeszip_filenameendswithzip(self):
        """"Process a zip file if the filename ends with .zip"""
        # arrange
        crawler = olieigra.Crawler()
        crawler.crawl_archive = MagicMock()

        # act
        crawler.process_file('/some/random/path', 'dillon-data.txt.zip')

        # assert
        crawler.crawl_archive.assert_called_once()

    def test_crawlarchive_nop_empty(self):
        """Confirm crawl exits gracefully if no files"""
        # arrange
        wrapper = IOWrapper()
        wrapper.close = MagicMock()
        wrapper.filelist = []
        wrapper.open_archive = MagicMock(return_value=wrapper)
        callbacks = olieigra.Callbacks()
        callbacks.start_file = MagicMock(return_value=False)
        reader = olieigra.Reader(callbacks=callbacks)
        crawler = olieigra.Crawler(io=wrapper, reader=reader)
        crawler.process_igra2_archive_file = MagicMock()

        # act
        crawler.crawl_archive('/some/random/path', 'dillon.zip')

        # assert
        wrapper.open_archive.assert_called_once()
        wrapper.close.assert_called_once()
        crawler.process_igra2_archive_file.assert_not_called()
        callbacks.start_file.assert_not_called()

    def test_crawlarchive_iterates_success(self):
        """Confirm crawl iterates over a list of filenames"""
        # arrange
        wrapper = IOWrapper()
        wrapper.close = MagicMock()
        wrapper.filelist = [ZipInfo('a'), ZipInfo('b'), ZipInfo('c')]
        wrapper.open_archive = MagicMock(return_value=wrapper)
        callbacks = olieigra.Callbacks()
        callbacks.start_file = MagicMock(return_value=True)
        reader = olieigra.Reader(callbacks=callbacks)
        crawler = olieigra.Crawler(io=wrapper, reader=reader)
        crawler.process_igra2_archive_file = MagicMock()

        # act
        crawler.crawl_archive('/some/random/path', 'dillon.zip')

        # assert
        wrapper.open_archive.assert_called_once()
        wrapper.close.assert_called_once()
        self.assertEqual(3, callbacks.start_file.call_count)
        self.assertEqual(3, crawler.process_igra2_archive_file.call_count)

    def test_crawlarchive_skips_callbackfalse(self):
        """Iterate through files but skip because callback False"""
        # arrange
        wrapper = IOWrapper()
        wrapper.close = MagicMock()
        wrapper.filelist = [ZipInfo('a'), ZipInfo('b'), ZipInfo('c')]
        wrapper.open_archive = MagicMock(return_value=wrapper)
        callbacks = olieigra.Callbacks()
        callbacks.start_file = MagicMock(return_value=False)
        reader = olieigra.Reader(callbacks=callbacks)
        crawler = olieigra.Crawler(io=wrapper, reader=reader)
        crawler.process_igra2_archive_file = MagicMock()

        # act
        crawler.crawl_archive('/some/random/path', 'dillon.zip')

        # assert
        wrapper.open_archive.assert_called_once()
        wrapper.close.assert_called_once()
        self.assertEqual(3, callbacks.start_file.call_count)
        self.assertEqual(0, crawler.process_igra2_archive_file.call_count)

    def test_processigrafile_callback_success(self):
        """It should attempt to read the igra2 file and make a callback"""
        # arrange
        callbacks = olieigra.Callbacks()
        callbacks.finish_file = MagicMock()
        reader = olieigra.Reader(callbacks=callbacks)
        reader.read_from_stream = MagicMock(return_value=(10, 20))
        io = IOWrapper()
        io.open_file = MagicMock(return_value=io)
        io.close = MagicMock()
        crawler = olieigra.Crawler(reader=reader, io=io)

        # act
        crawler.process_igra2_file('some/random/path', 'dillon.txt')

        # assert
        reader.read_from_stream.assert_called_once()
        io.open_file.assert_called_once()
        io.close.assert_called_once()
        callbacks.finish_file.assert_called_once_with(10, 20)

    def test_processigraarchivefile_callback_success(self):
        """It should attempt to read the igra2 file from archive and make a callback"""
        # arrange
        callbacks = olieigra.Callbacks()
        callbacks.finish_file = MagicMock()
        reader = olieigra.Reader(callbacks=callbacks)
        reader.read_from_stream = MagicMock(return_value=(10, 20))
        io = IOWrapper()
        io.open_archive_file = MagicMock(return_value=io)
        io.read_as_text = MagicMock(return_value=io)
        io.close = MagicMock()
        crawler = olieigra.Crawler(reader=reader, io=io)

        # act
        crawler.process_igra2_archive_file(None, 'dillon.txt')

        # assert
        reader.read_from_stream.assert_called_once()
        io.open_archive_file.assert_called_once()
        self.assertEqual(2, io.close.call_count)
        callbacks.finish_file.assert_called_once_with(10, 20)
