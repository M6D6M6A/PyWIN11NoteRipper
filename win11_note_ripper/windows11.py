import os
from pathlib import Path
import platform
from loguru import logger


class Windows11:
    """
    A class to check compatibility with Windows 11 and locate specific directories.

    This class is designed to identify if the current operating system is Windows 11 
    and to locate certain directories specific to Windows 11, such as the Notepad tabs directory.

    Attributes:
        SYSTEM (str): The operating system name. Default is 'Windows'.
        RELEASE (str): The release version, which corresponds to Windows 11. Default is '10'.
        MIN_VERSION (str): The minimum version number for Windows 11. Default is '10.0.22000'.
        LOCALAPPDATA_DIR (Path | None): Path to the local app data directory. None if not set.
        NOTEPAD_TABS_DIR (Path | None): Path to the Windows 11 Notepad tabs directory. None if not set.
    """
    SYSTEM: str = 'Windows'
    RELEASE: str = '10'  # Windows 11
    MIN_VERSION: str = '10.0.22000'

    LOCALAPPDATA_DIR: Path | None = None
    NOTEPAD_TABS_DIR: Path | None = None

    @classmethod
    def check(cls) -> bool:
        """
        Checks if the current operating system is Windows 11 and sets relevant directories.

        This method checks the system, release, and version against predefined Windows 11 values.
        If the check passes, it sets the LOCALAPPDATA_DIR and NOTEPAD_TABS_DIR class attributes.

        Returns:
            bool: True if the operating system is Windows 11 and necessary directories are found, False otherwise.
        """
        if (
                platform.system() == cls.SYSTEM
                and platform.release() == cls.RELEASE
                and platform.version() >= cls.MIN_VERSION
        ):
            localappdata_env = os.environ.get('LOCALAPPDATA')
            if localappdata_env:
                cls.LOCALAPPDATA_DIR = Path(localappdata_env)
                cls.NOTEPAD_TABS_DIR = cls.LOCALAPPDATA_DIR / \
                    'Packages' / 'Microsoft.WindowsNotepad_8wekyb3d8bbwe' / \
                    'LocalState' / 'TabState'
                logger.debug(f"NOTEPAD_TABS_DIR: '{cls.NOTEPAD_TABS_DIR}'")
                return cls.NOTEPAD_TABS_DIR.is_dir()
            else:
                logger.error("LOCALAPPDATA environment variable not found.")
        else:
            logger.error("This script requires Windows 11.")
        return False
