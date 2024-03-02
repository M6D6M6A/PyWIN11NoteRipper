from . import settings
from .windows11 import Windows11
from .win11_note_tabs import Win11NoteTabs
from .win11_note_tab import Win11NoteTab
from .win11_note_tab_parser import Win11NoteTabParser
from .py_win11_note_ripper import PyWin11NoteRipper

from pathlib import Path
import sys
from loguru import logger

_log_path = Path(__file__).resolve().parent / "debug.log"

logger.remove()
logger.add(
    _log_path if settings.LOG_FILE else sys.stderr,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> ㉿ "
        "<level>{message}</level>"
    ),
    level=settings.LOG_LEVEL,
)