"""Default callback implementation"""
from .body_model import BodyModel
from .header_model import HeaderModel


class Callbacks:
    """Default callbacks"""

    def __init__(self):
        self.warn_body = False

    def found_zipfile(self, filename: str) -> bool:
        """Decide if the passed zipfile should be processed"""
        print(f"Default callback: Skipping {filename}.")
        return False

    def found_file(self, filename: str) -> bool:
        """Decide if the passed file should be processed"""
        print(f"Default callback: Skipping {filename}.")
        return False

    def finished_file(self, headers: int, rows: int):
        """The file processing is complete"""
        print(f"Default callback: Read {headers} headers and {rows} rows.")

    def parsed_header(self, header: HeaderModel) -> bool:
        """Decide if the body should be parsed"""
        print(f"Default callback: Ignoring header ({header.id}).")
        return False

    def parsed_body(self, body: list[BodyModel]) -> bool:
        """Process the list of body records"""
        if not self.warn_body:
            self.warn_body = True
            print(">>>Please override callback_body<<< ", end="")
            print(len(body))

        return False
