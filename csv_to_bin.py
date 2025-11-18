from dataclasses import dataclass
from typing import Callable, Any, List, Optional, TextIO
import struct  # Used to turn each CSV row into a fixed-size binary record
import csv


@dataclass  # auto-generate __init__, __repr__, etc., for simple “data holder” classes, so you don’t write boilerplate.
class FieldSpec:
  name: str  # logical name (for your reference)
  format: str  # struct format char, e.g. "q", "i", "d", "b"
  parser: Callable[[str], Any]  # A function that takes the CSV cell string and returns a parsed Python value (usually int or float)


# Function that takes a list of FieldSpec and returns a compiled struct.Struct
# Compiling a Struct once is faster than calling struct.pack with a format string every time in the loop
def build_struct(fields: List[FieldSpec]) -> struct.Struct:
  # Builds a binary format string, e.g. "<dqib":
  # "<" = little-endian (least-significant byte first)
  # Then concatenates each FieldSpec.format, e.g. "d" "q" "i" "b"
  format = "<" + "".join(f.format for f in fields)
  # Precompiling the format improves performance in tight loops where you pack millions of rows.
  return struct.Struct(format)


# Creates a csv.reader object for a given file
def make_reader(file_in: TextIO, has_header: bool, delimiter: Optional[str]) -> csv.reader:
  if delimiter is None:
    # Reads the first 1024 bytes of the file into memory
    # csv.Sniffer needs a sample string to guess the delimiter and quoting rules. You don’t need the whole file, just enough rows.
    sample = file_in.read(1024)
    # After reading 1024 bytes, the file is “advanced”; you must rewind so the actual CSV reading starts from the very beginning.
    file_in.seek(0)
    # Asks csv.Sniffer to analyze sample and return a dialect object (delimiter, quotechar, etc.).
    dialect = csv.Sniffer().sniff(sample)
    reader = csv.reader(file_in, dialect)
  else:
    reader = csv.reader(file_in, delimiter=delimiter)
  
  if has_header:
    # Skip one row from the reader if the CSV has a header. You don’t want the header line to be treated as data.
    next(reader, None)
  
  return reader


def csv_to_bin(
    csv_path: str,
    bin_path: str,
    fields: List[FieldSpec],
    delimiter: Optional[str] = None,
    has_header: Optional[bool] = False,
) -> None:
  # For each row, you’ll pack all parsed values using this object. Doing this once outside the loop is more efficient.
  record_struct = build_struct(fields)
  # The number of CSV columns you expect (one per FieldSpec). Used for validation inside the loop to catch malformed rows.
  expected_columns = len(fields)

  # Opens the CSV file for reading text ("r") and the binary file for writing ("wb"), using a context manager.
  with open(csv_path, "r", newline="", encoding="utf-8") as file_in, open(bin_path, "wb") as file_out:
    # Calls your make_reader helper to get a csv.reader configured
    reader = make_reader(file_in, has_header, delimiter)

    # Loops over each row from the CSV reader, giving you.
    # line_num is used in error messages so you can pinpoint where something went wrong
    for line_num, row in enumerate(reader, start=1):
      # Skip completely empty or whitespace-only rows. Real-world CSVs often have blank lines; ignoring them avoids spurious errors.
      if not row or all(not cell.strip() for cell in row):
        continue

      # If the row has fewer cells than your schema expects, raise an error.
      # Protects you from silently packing wrong data (e.g. malformed rows).
      # !r means “use repr(row)” – shows a more raw representation, good for debugging.
      if len(row) < expected_columns:
        raise ValueError(f"{csv_path}:{line_num}: expected at least {expected_columns} columns, got {len(row)}: {row!r}")
      
      try:
        # Builds a list of parsed values. Converts raw CSV text into the correct Python types according to your schema, in a nice compact form.
        # zip(fields, row) pairs each FieldSpec with the corresponding string cell.
        # For each pair, calls field.parser(val) (e.g., int("123") → 123).
        values = [field.parser(val) for field, val in zip(fields, row)]
      except Exception as e:
        raise ValueError(f"{csv_path}:{line_num}: error parsing row {row!r}: {e}") from e
      
      try:
        # Packs all parsed values into a bytes object using the compiled Struct. This creates your fixed-size binary row, ideal for memory-mapped, sequential replay later.
        # *values unpacks the list so it becomes positional arguments.
        packed = record_struct.pack(*values)
      except struct.error as e:
        raise ValueError(f"{csv_path}:{line_num}: stuck.pack failed for values {values!r}: {e}") from e
      
      # Writes the packed bytes to the output file. Appends the record to the binary file. Each row in the CSV becomes one binary record.
      file_out.write(packed)


if __name__ == "__main__":
  # example
  lobster_fields = [
    FieldSpec("time",         "d", float),  # float64, C double (8-byte float) in struct format.
    FieldSpec("event_type",   "b", int),    # int8, signed char (1-byte integer).
    FieldSpec("order_id",     "q", int),    # int64, 8-byte signed integer: 64-bit
    FieldSpec("size",         "i", int),    # int32, 4-byte signed integer, 32-bit
    FieldSpec("price",        "i", int),    # int32, 4-byte signed integer, 32-bit
    FieldSpec("direction",    "b", int),    # int8  (1 = buy, -1 = sell), signed byte
  ]
  csv_to_bin(
    "lobster_messages.csv",
    "lobster_messages.bin",
    lobster_fields,
  )
