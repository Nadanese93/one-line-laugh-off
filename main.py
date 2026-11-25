#!/usr/bin/env python3
"""One-Line Laugh-Off entry: writes a single joke to /output/entry.txt."""

import os
import tempfile

ENTRY = "My dentist asked if I floss. I said 'emotionally, yes' \u2014 he charged me extra for the honesty."

MAX_CHARS = 200


def main():
    if not ENTRY or not ENTRY.strip():
        raise ValueError("entry must be 1-200 characters and not only whitespace")
    if len(ENTRY) > MAX_CHARS:
        raise ValueError("entry exceeds 200 characters")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")

    data = ENTRY.encode("utf-8")
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, target)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise

    # Read-back verification: the file on disk must be byte-identical to
    # what we intended to write; a mismatch means the write did not land.
    with open(target, "rb") as f:
        written = f.read()
    if written != data:
        raise IOError("entry.txt verification failed: written bytes differ from entry")


if __name__ == "__main__":
    main()
