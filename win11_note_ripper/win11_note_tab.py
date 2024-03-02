from pathlib import Path
from loguru import logger

from .win11_note_tab_parser import Win11NoteTabParser


class Win11NoteTab:
    """
    A class representing a single Windows 11 Notepad tab.

    This class encapsulates the logic for managing individual Notepad tab files,
    including initialization, file handling, and parsing.

    Attributes:
        magic_files (List[str]): List of special file formats to be considered as magic files.
        root_tab_name (str | None): The root name of the Notepad tab.
        tab_files (List[str] | None): A list of file formats associated with the Notepad tab.
        parsed (Win11NoteTabParser | None): An instance of Win11NoteTabParser containing parsed data of the tab.

    Args:
        dir (Path): The directory where the Notepad tab files are located.
        root_tab_name (str): The root name of the Notepad tab to be processed.
    """
    magic_files = ['.0.bin', '.1.bin']
    root_tab_name: str | None = None
    tab_files: list | None = None
    parsed: Win11NoteTabParser | None = None

    def __init__(self, dir: Path, root_tab_name: str) -> None:
        """
        Initializes the Win11NoteTab instance with a directory and the root name of the tab.

        Args:
            dir (Path): The directory where the Notepad tab files are located.
            root_tab_name (str): The root name of the Notepad tab to be processed.
        """
        self.dir = dir
        self.root_tab_name = root_tab_name
        self.tab_files = []

        logger.debug(f"'{self.root_tab_name}' initalized.")

    def _set_file(self, file_format):
        """
        Adds a file format to the tab files list.

        Args:
            file_format (str): The file format to be added.
        """
        logger.debug(f"'{self.root_tab_name}' {file_format = }' added.")
        self.tab_files.append(file_format)

    def _parse(self) -> None:
        """
        Parses the tab files associated with this tab, except for the magic files.
        """
        for file_format in self.tab_files:
            # Skip Magic files for now, since i dont know what those do.
            if file_format in self.magic_files:
                continue

            file_path = self.dir / f"{self.root_tab_name}{file_format}"
            self.parsed = Win11NoteTabParser(file_path)

    def __repr__(self) -> str:
        """
        Returns a string representation of the object.

        Returns:
            str: A string representing the list of file formats associated with the tab.
        """
        return str([
            f"{self.root_tab_name}{file_format}"
            for file_format in self.tab_files
        ])
