"""Read an Igra2 file"""
from .body_model import BodyModel
from .callbacks import Callbacks
from .header_model import HeaderModel


class Reader:
    """Read an Igra2 file"""

    def __init__(self, callbacks=Callbacks()):
        self.callbacks = callbacks

    def parse_header(self, header_line: str) -> HeaderModel:
        """Parse an Igra2 header row"""
        if header_line[0:1] != "#":
            raise ValueError(f"This line isn't a header row: {header_line}")

        return HeaderModel(
            header_line[1:12],              # id
            int(header_line[13:17]),        # year
            int(header_line[18:20]),        # month
            int(header_line[21:23]),        # day
            int(header_line[24:26]),        # hour
            int(header_line[27:31]),        # reltime
            int(header_line[32:36]),        # numlev
            header_line[37:45].strip(),     # p_src
            header_line[46:54].strip(),     # np_src
            int(header_line[55:62]),        # lat
            int(header_line[63:71])         # lon
        )

    def read_from_stream(self, reader) -> tuple[int, int]:
        """Read Igra2 file from stream"""
        header_count = 0
        line_count = 0

        while True:
            line = str(reader.readline(), encoding='UTF-8')

            if line == "":
                break

            header = self.parse_header(line)
            if self.callbacks.parsed_header(header):
                body = self.parse_body(reader, header.numlev)
                self.callbacks.parsed_body(body)
            else:
                self.skip_body(reader, header.numlev)

            header_count += 1
            line_count += header.numlev + 1

        return header_count, line_count

    def skip_body(self, reader, records: int):
        """Read a body without processing it"""
        for _ in range(records):
            reader.readline()

    def parse_body(self, reader, records: int) -> list[BodyModel]:
        """Read a body with processing"""
        result = []

        for _ in range(records):
            line = str(reader.readline(), encoding='UTF-8')
            result.append(self.parse_body_line(line))

        return result

    def parse_body_line(self, line: str) -> BodyModel:
        """Parse a line from a body section"""
        return BodyModel(
            line[0:2],                      # type
            int(line[9:15]),                # pres
            self.parse_float(line[16:21]),  # gph
            self.parse_float(line[22:27]),  # temp
            self.parse_float(line[28:33]),  # rh
            self.parse_float(line[34:39]),  # dpdp
            self.parse_float(line[40:45]),  # wder
            self.parse_float(line[46:51])   # wspd
        )

    def parse_float(self, my_slice: str) -> float:
        """Parse value, returning NaN for invalid/missing data"""
        result = int(my_slice)

        if result in (-8888, -9999):
            return float("NaN")

        return float(result)
