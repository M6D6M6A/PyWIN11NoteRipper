> **Warning** The content of this repo is a proof of concept and is for educational purposes only, use it only on your own Devices!

# Py WIN11 Note Ripper

|           |                                                             |
| :-------- | ----------------------------------------------------------: |
| Credits   | [John Hammond](https://www.youtube.com/watch?v=zSSBbv2fc2s) |
| Author    |                                              Philipp Reuter |
| Version   |                                                 Alpha 0.0.1 |
| Tested OS |                                                  Windows 11 |
| Discord   |                                                     mpb.rip |
| Python    |                                              3.11+ (tested) |

# Features

-   [x] Load all notepad tab binary files.
-   [x] Parse saved or unsaved changes of all tabs.
-   [x] Export all data including bytes data to quickly compare changes in different versions.
-   [ ] Parse the cache of changes while notepad is still open.
-   [ ] Parse full header.
-   [ ] Parse body end.
-   [ ] Parse magic files `.0.bin` and `.1.bin`.

# Installation

1. Download this repo with git or as a zip.
2. Run `print.py` to print all the information to the console or use `rip.py` to export it to `/rip` in the same folder as `.json`.

# Settings

1. Navigate to the folder containing `print.py` and `rip.py`.
2. The settings can be changed in `win11_note_ripper/settings.py`, all valid options are listed after the comment.

# Know Errors

`ERROR    ㉿ Error decoding UTF-16 data: 'utf-16-le' codec can't decode byte 0x00 in position n: truncated data`

> I am not sure how to fix this yet, but that is why I am including the raw bytes as well in the export.
