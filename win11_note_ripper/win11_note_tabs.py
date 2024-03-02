from pathlib import Path

from .win11_note_tab import Win11NoteTab


class Win11NoteTabs:
    """
    A class for managing and parsing multiple Windows 11 Notepad tab files.

    This class is responsible for initializing and parsing multiple Win11NoteTab instances
    based on a directory of tab files.

    Attributes:
        _tab_dir (Path): The directory containing Notepad tab files.
        _tabs (dict[str, Win11NoteTab]): A dictionary mapping root tab names to Win11NoteTab instances.

    Args:
        tab_dir (Path): The directory containing Notepad tab files.
        file_path_iterator (Iterator[Path]): An iterator over Paths of individual Notepad tab files.
    """
    _tab_dir = Path
    _tabs: dict[str, Win11NoteTab] = {}

    def __init__(self, tab_dir, file_path_iterator: Path) -> None:
        """
        Initializes the Win11NoteTabs instance with a directory and file path iterator.

        Args:
            tab_dir (Path): The directory containing Notepad tab files.
            file_path_iterator (Iterator[Path]): An iterator over Paths of individual Notepad tab files.
        """
        self._tab_dir = tab_dir

        tab_path: Path
        for tab_path in file_path_iterator:
            file_name = tab_path.name
            if file_name.endswith('.0.bin'):
                file_format = '.0.bin'
            elif file_name.endswith('.1.bin'):
                file_format = '.1.bin'
            else:
                file_format = '.bin'

            root_tab_name = file_name.replace(file_format, '')

            if not root_tab_name in self._tabs:
                self._tabs[root_tab_name] = Win11NoteTab(
                    self._tab_dir, root_tab_name)

            self._tabs[root_tab_name]._set_file(file_format)

        for note_tab in self._tabs.values():
            note_tab._parse()

    def __iter__(self):
        """
        Allows iteration over the parsed Notepad tabs.

        Yields:
            tuple: A tuple containing the tab name with '.bin' appended and its parsed contents as a dictionary.
        """
        for attr, value in self._tabs.items():
            if not attr.startswith('_'):
                yield f'{attr}.bin', dict(value.parsed)
