import datetime
import json
from pathlib import Path
import os
from loguru import logger

from .windows11 import Windows11
from .win11_note_tabs import Win11NoteTabs


class PyWin11NoteRipper:
    """
    A class for ripping Windows 11 Notepad tabs and saving them as JSON.

    This class handles the extraction of Notepad tab information from Windows 11 systems and saves the extracted
    information in a structured JSON format.

    Methods:
        get_tabs: Retrieves Notepad tab information.
        rip: Extracts Notepad tabs and saves them as a JSON file.
    """
    def __init__(self) -> None:
        """
        Initializes the PyWin11NoteRipper instance.

        Checks for Windows 11 compatibility and sets up the Notepad tabs iterator.
        If the OS is incompatible or necessary environment variables are missing, the script will terminate.
        """
        if not Windows11.check():
            logger.error("Incompatible OS or missing environment variable.")
            quit()

        self.notepad_tabs_iterator = Windows11.NOTEPAD_TABS_DIR.glob('*.bin')

    def get_tabs(self) -> Win11NoteTabs:
        """
        Retrieves Notepad tabs as a Win11NoteTabs instance.

        Returns:
            Win11NoteTabs: An instance of Win11NoteTabs containing the parsed Notepad tabs.
        """
        return Win11NoteTabs(Windows11.NOTEPAD_TABS_DIR, self.notepad_tabs_iterator)

    def print(self) -> Win11NoteTabs:
        """
        Retrieves Notepad tabs, logs the count, and prints their JSON representation.

        This method fetches the Notepad tabs using the get_tabs method, logs the number of tabs found,
        and prints a JSON representation of these tabs to the logger. The JSON output is formatted with
        an indentation for better readability.

        Returns:
            Win11NoteTabs: An instance of Win11NoteTabs containing the parsed Notepad tabs.
        """
        tabs = self.get_tabs()
        logger.info(f"Found {len(tabs._tabs)} tabs.")
        json_tabs = json.dumps(dict(tabs), indent=4)
        logger.info(f"tabs._tabs = '{json_tabs}'")

    def rip(self) -> None:
        """
        Extracts Notepad tabs and saves them as a JSON file in a designated directory.

        The JSON file is named based on the current UTC time. The method creates a directory if it doesn't exist,
        extracts Notepad tabs, and saves them in a structured JSON format.
        """
        _dir = Path(__file__).resolve().parent.parent
        rip_dir = _dir / 'rip'
        os.makedirs(rip_dir, exist_ok=True)

        # Format the current UTC time as YYYY-MM-DD_HH-MM
        filetime = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'{filetime}.json'

        logger.debug(rip_dir / filename)
        tabs = Win11NoteTabs(Windows11.NOTEPAD_TABS_DIR,
                             self.notepad_tabs_iterator)
        dict_tabs = dict(tabs)
        json_tabs = json.dumps(dict_tabs, indent=4)

        with open(rip_dir / filename, 'w') as f:
            f.write(json_tabs)
