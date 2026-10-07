"""Check actual package input bytes against TestForge's maintained text policy."""
from pathlib import Path

BINARY_SUFFIXES = {".zip", ".docx", ".pdf", ".pptx", ".xlsx", ".gif", ".ico", ".jpg", ".jpeg", ".png"}
TEXT_SUFFIXES = {".py", ".md", ".txt", ".json", ".jsonl", ".js", ".css", ".html", ".yaml", ".yml", ".toml", ".xml", ".csv", ".ps1", ".sh", ".command", ".ini", ".cfg", ".cmd", ".bat"}

def assert_text_entries(entries):
    """Reject wrong endings before archive replacement; never normalize on behalf of custody."""
    for name, data in entries:
        path = Path(name)
        if path.suffix.lower() in BINARY_SUFFIXES or name.endswith("/"):
            continue
        known_text = path.suffix.lower() in TEXT_SUFFIXES or path.name in {".gitattributes", ".editorconfig"}
        if b"\x00" in data:
            if known_text:
                raise ValueError(f"text input contains NUL bytes: {name}")
            continue
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as error:
            if known_text:
                raise ValueError(f"text input is not UTF-8: {name}") from error
            continue
        if path.suffix.lower() in {".bat", ".cmd"}:
            remainder = data.replace(b"\r\n", b"")
            if b"\r" in remainder or b"\n" in remainder:
                raise ValueError(f"Windows command input requires CRLF: {name}")
        elif b"\r" in data:
            raise ValueError(f"authored text requires LF before packaging: {name}")

def assert_source_text(paths):
    assert_text_entries((str(path), Path(path).read_bytes()) for path in paths)
