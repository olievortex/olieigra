"""Unit tests for module reader"""
import math
import unittest
from unittest.mock import MagicMock
from src import olieigra


class ReaderTests(unittest.TestCase):
    """Unit tests for class Reader"""

    def test_parsefloat_float_success(self):
        """Try parsing a number"""
        # arrange
        reader = olieigra.Reader()

        # act
        value = reader.parse_float('1234')

        # assert
        self.assertEqual(1234, value)

    def test_parsefloat_nan_invalid(self):
        """When -8888, should return NaN"""
        # arrange
        reader = olieigra.Reader()

        # act
        value = reader.parse_float('-8888')

        # assert
        self.assertTrue(math.isnan(value))

    def test_parsefloat_nan_missing(self):
        """When -9999, should return NaN"""
        # arrange
        reader = olieigra.Reader()

        # act
        value = reader.parse_float('-9999')

        # assert
        self.assertTrue(math.isnan(value))

    def test_parsebodyline_correctbody_success(self):
        """Parse a valid line"""
        # arrange
        line = "20 10305    747 33064B -542B-9999 -9999   286   298 \n"
        reader = olieigra.Reader()

        # act
        value = reader.parse_body_line(line)

        # assert
        self.assertEqual('20', value.type)
        self.assertEqual(747, value.pres)
        self.assertEqual(33064, value.gph)
        self.assertEqual(-542, value.temp)
        self.assertTrue(math.isnan(value.rh))
        self.assertTrue(math.isnan(value.dpdp))
        self.assertEqual(286, value.wdir)
        self.assertEqual(298, value.wspd)

    def test_skipbody_reads_success(self):
        """When skipping the body, just read the lines"""
        # arrange
        reader = olieigra.Reader()
        reader.readline = MagicMock(side_effect=["a\n", "b\n", "c\n"])

        # act
        reader.skip_body(reader, 2)

        # assert
        self.assertEqual(2, reader.readline.call_count)

    def test_parsebody_correctlist_success(self):
        """When parsing the body, get a list of records"""
        # arrange
        reader = olieigra.Reader()
        reader.readline = MagicMock(side_effect=[
            b"20  9219   1433 28939B -587B   11   291   336   121 \n",
            b"20  9447   1229 29905B -581B   11   291   285    44 \n",
            b"20  9528   1177 30177B -578B   11   293   270    72 \n"])

        # act
        result = reader.parse_body(reader, 2)

        # assert
        self.assertEqual(2, reader.readline.call_count)
        self.assertEqual(2, len(result))
        self.assertEqual(1433, result[0].pres)
        self.assertEqual(1229, result[1].pres)

    def test_parseheader_throws_failure(self):
        """An invalid header should throw an exception"""
        # arrange
        line = '22  5614   9147 16780B -594B   14   277   281   190 \n'
        reader = olieigra.Reader()

        # act, assert
        self.assertRaises(ValueError, reader.parse_header, line)

    def test_parseheader_correctheader_success(self):
        """Ensure the header is parsed correctly"""
        # arrange
        line = "#USM00072649 2023 11 18 12 1101   91 ncdc-nws           448497  -935647\n"
        reader = olieigra.Reader()

        # act
        value = reader.parse_header(line)

        # assert
        self.assertEqual('USM00072649', value.id)
        self.assertEqual(2023, value.year)
        self.assertEqual(11, value.month)
        self.assertEqual(18, value.day)
        self.assertEqual(12, value.hour)
        self.assertEqual(1101, value.reltime)
        self.assertEqual(91, value.numlev)
        self.assertEqual("ncdc-nws", value.p_src)
        self.assertEqual("", value.np_src)
        self.assertEqual(448497, value.lat)
        self.assertEqual(-935647, value.lon)

    def test_readfromstream_correctcounts_success(self):
        """Make sure the header and row counts are accurate"""
        # arrange
        reader = olieigra.Reader()
        reader.readline = MagicMock(side_effect=self.sample_file())

        # act
        headers, rows = reader.read_from_stream(reader)

        # assert
        self.assertEqual(2, headers)
        self.assertEqual(7, rows)

    def test_readfromstream_shortcircuits_callbackfalse(self):
        """Make sure a False return value from header callback causes short circuit"""
        # arrange
        callbacks = olieigra.Callbacks()
        callbacks.parsed_header = MagicMock(side_effect=[True, False])
        callbacks.parsed_body = MagicMock()
        reader = olieigra.Reader(callbacks=callbacks)
        reader.readline = MagicMock(side_effect=self.sample_file_headers())
        reader.skip_body = MagicMock()
        reader.parse_body = MagicMock(return_value='dillon')

        # act
        _, _ = reader.read_from_stream(reader)

        # assert
        self.assertEqual(2, reader.callbacks.parsed_header.call_count)
        reader.callbacks.parsed_body.assert_called_once_with('dillon')
        reader.skip_body.assert_called_once_with(reader, 3)
        reader.parse_body.assert_called_once_with(reader, 2)

    def sample_file(self) -> list[str]:
        """Simple sample test case igra2 file"""
        return [
            b"#USM00072649 2023 11 18 12 1101    2 ncdc-nws           448497  -935647\n",
            b"21     0  98022B  290    -9B  810    28   360     0 \n",
            b"20     4  97717   316B   -1B  771    35   275    26 \n",
            b"#USM00072649 2023 11 18 00 2303    3 ncdc-nws           448497  -935647\n",
            b"21     0  98107B  290    65B  350   143   360     0 \n",
            b"20     7  97609   332B   66B  339   147   208    45 \n",
            b"20    33  95916   476B   60B  325   152   224    73 \n",
            b""
        ]

    def sample_file_headers(self) -> list[str]:
        """Simple sample test case igra2 file"""
        return [
            b"#USM00072649 2023 11 18 12 1101    2 ncdc-nws           448497  -935647\n",
            b"#USM00072649 2023 11 18 00 2303    3 ncdc-nws           448497  -935647\n",
            b""
        ]
