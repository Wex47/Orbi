from pathlib import Path

files = [p.name for p in Path(".").iterdir() if p.is_file()]
print(files)