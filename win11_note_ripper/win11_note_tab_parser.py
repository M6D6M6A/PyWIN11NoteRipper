from loguru import logger
from pathlib import Path

class Win11NoteTabParser:
    """
    A parser class for processing Windows 11 Notepad tab files.

    Attributes:
        file_path (str | None): String of the path to the file.
        magic_bytes (bytes | None): The initial magic bytes of the file.
        is_saved_file (bool | None): Flag indicating if the file is saved.
        filename_len_byte (bytes | None): Byte indicating the length of the filename.
        filename_len_utf_16 (int | None): Length of the filename in UTF-16 encoding.
        filename_bytes (bytes | None): Byte sequence of the filename.
        filename_utf_16 (str | None): Filename decoded in UTF-16.
        body_bytes (bytes | None): Byte sequence of the file body.
        body_utf16 (str | None): File body content decoded in UTF-16.
        body_end_bytes (bytes | None): The last bytes of the file body.

    Methods:
        _parse: Parses the entire file.
        _parse_header: Parses the header part of the file.
        _parse_body: Parses the body part of the file.
        _decode_utf16: Decodes a byte sequence using UTF-16 encoding.
        _find_delimiters: Finds delimiters in the byte sequence.
    """
    file_path: str | None = None
    magic_bytes: bytes | None = None
    is_saved_file: bool | None = None
    filename_len_byte: bytes | None = None
    filename_len_utf_16: str | None = None
    filename_bytes: bytes | None = None
    filename_utf_16: str | None = None
    body_bytes: bytes | None = None
    body_utf16: str | None = None
    body_end_bytes: bytes | None = None

    _file_path: Path | None = None

    _delimiter_start_flag = b'\x00\x01'
    _delimiter_end_flag = b'\x01\x00\x00\x00'
    _saved_file_index = 3
    _filename_len_index = 4
    _filename_start_index = 5
    _body_end_index = -5

    def __init__(self, file_path: Path) -> None:
        """
        Initializes the parser with a file path.

        Args:
            file_path (Path): The path to the file to be parsed.
        """
        self._file_path = file_path
        self.file_path = str(file_path)
        self._parse()

    def _parse(self):
        """
        Parses the file into header and body components.
        Handles different byte sequences and formats in the file.
        """
        try:
            with open(self._file_path, 'rb') as f:
                logger.debug(f"Opened '{self._file_path}' to parse it.")
                f_bytes: bytes = f.read()

            self._parse_header(f_bytes)
            self._parse_body(f_bytes)

        except UnicodeDecodeError as e:
            logger.error(f"UnicodeDecodeError while parsing file {self._file_path}: {e}")
        except ValueError as e:
            logger.error(f"ValueError while parsing file {self._file_path}: {e}")

    def _parse_header(self, data: bytes):
        """
        Parses the header portion of the file.

        Args:
            data (bytes): The byte sequence of the file.
        """
        self.magic_bytes = data[ : self._saved_file_index]
        self.is_saved_file = bool(data[self._saved_file_index])
        logger.debug(f'{self.is_saved_file = }')

        if self.is_saved_file:
            self.filename_len_byte = data[self._filename_len_index]
            self.filename_len_utf_16 = self.filename_len_byte * 2
            logger.debug(f'{self.filename_len_utf_16 = }')

            filename_ending = self._filename_start_index + self.filename_len_utf_16
            self.filename_bytes = data[self._filename_start_index : filename_ending]
            self.filename_utf_16 = self._decode_utf16(self.filename_bytes)
            logger.debug(f'{self.filename_utf_16 = }')

    def _parse_body(self, data: bytes):
        """
        Parses the body portion of the file.

        Args:
            data (bytes): The byte sequence of the file.
        """
        delimiter_start, delimiter_end = self._find_delimiters(data, self.filename_len_utf_16 + 5)
        logger.debug(f'{delimiter_start = }, {delimiter_end = }')

        self.body_bytes = data[delimiter_end + 4 : self._body_end_index]
        self.body_utf16 = self._decode_utf16(self.body_bytes)
        logger.debug(f'{len(self.body_utf16) = }')

        # Save the last bytes of the file body
        self.body_end_bytes = data[self._body_end_index : ]
        logger.debug(f'Body end bytes: {self.body_end_bytes}')

    def _decode_utf16(self, data: bytes) -> str:
        """
        Decodes a byte sequence using UTF-16 encoding.

        Args:
            data (bytes): The byte sequence to decode.

        Returns:
            str: The decoded string.
        """
        try:
            return data.decode('utf-16')
        except UnicodeDecodeError as e:
            logger.error(f"Error decoding UTF-16 data: {e}")
            return ""

    def _find_delimiters(self, data: bytes, start_index: int) -> tuple[int, int]:
        """
        Finds the start and end delimiters in the byte sequence.

        Args:
            data (bytes): The byte sequence of the file.
            start_index (int): The starting index for searching delimiters.

        Returns:
            tuple[int, int]: The start and end indices of the delimiter.
        """
        delimiter_start = data[start_index:].index(self._delimiter_start_flag) + start_index
        delimiter_end = data[delimiter_start + len(self._delimiter_start_flag) : ].index(self._delimiter_end_flag) + delimiter_start
        return delimiter_start, delimiter_end

    def __iter__(self):
        """
        Allows iteration over the public attributes of the instance.

        Yields:
            tuple: A tuple containing the attribute name and value.
        """
        for attr, value in vars(self).items():
            if not attr.startswith('_'):
                if isinstance(value, bytes):
                    yield attr, str(value)
                else:
                    yield attr, value
