# read_excel_helper.py
import os
import pandas as pd
import tempfile

def _get_ext_from_input(path_or_buf):
    # path-like string
    if isinstance(path_or_buf, (str, os.PathLike)):
        return os.path.splitext(str(path_or_buf))[1].lower()
    # uploaded file from Flask (has .filename)
    if hasattr(path_or_buf, "filename"):
        return os.path.splitext(path_or_buf.filename)[1].lower()
    return None

def read_any_excel(path_or_buffer):
    """
    Read an Excel-like file (path or file-like object). Tries to pick the correct engine
    based on extension; falls back to trying common engines if extension unknown.
    Returns a pandas.DataFrame.
    """
    ext = _get_ext_from_input(path_or_buffer)
    engine_map = {
        ".xlsx": "openpyxl",
        ".xls": "xlrd",
        ".xlsb": "pyxlsb",
        ".ods": "odf",
    }

    # If we have a recommended engine for the extension, try it first
    if ext in engine_map:
        engine = engine_map[ext]
        try:
            return pd.read_excel(path_or_buffer, engine=engine)
        except Exception as e:
            # continue to fallback below
            last_exc = e
    else:
        last_exc = None

    # Fallback: try common engines in order
    for engine in ("openpyxl", "xlrd", "pyxlsb"):
        try:
            return pd.read_excel(path_or_buffer, engine=engine)
        except Exception as e:
            last_exc = e
            continue

    # Final attempt: let pandas try to infer (no engine)
    try:
        return pd.read_excel(path_or_buffer)
    except Exception as e:
        # Provide helpful error message
        raise RuntimeError(
            "Unable to read the Excel file. Tried engines openpyxl, xlrd, pyxlsb. "
            "If file extension is non-standard (like .xlsh), rename it to .xlsx/.xls and try again. "
            f"Last engine error: {last_exc}"
        ) from last_exc

# Quick CLI test
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python read_excel_helper.py <path-to-excel-file>")
        sys.exit(1)
    fn = sys.argv[1]
    df = read_any_excel(fn)
    print(df.head().to_string(index=False))
