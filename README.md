> **Warning** The content of this repo is a proof of concept and is for educational purposes only, use it only on your own Devices!

# Py WIN11 Note Ripper

|           |                |
| :-------- | -------------: |
| Author    | Philipp Reuter |
| Version   |    Alpha 0.0.1 |
| Tested OS |     Windows 11 |
| Discord   |        mpb.rip |
| Python    | 3.11+ (tested) |

# Features

- [x] Load all notepad tab binary files.
- [x] Parse saved or unsaved changes of all tabs.
- [x] Export all data including bytes data to quickly compare changes in different versions.
- [ ] Parse the cache of changes while notepad is still open.

# Installation

1. Download this repo with git or as a zip.
2. Run `print.py` to print all the information to the console or use `rip.py` to export it to `/rip` in the same folder as `.json`.

# Know Errors

`ERROR    ㉿ Error decoding UTF-16 data: 'utf-16-le' codec can't decode byte 0x00 in position n: truncated data`

> I am not sure how to fix this yet, but that is why I am including the raw bytes as well in the export.
