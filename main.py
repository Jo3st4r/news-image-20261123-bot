"""Entry program for news-image-20261123.

Writes the pre-rendered front page poster.png to /output/entry.png.
Standard library only; no network; deterministic — both graded runs
produce the same bytes.
"""

import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "poster.png"
OUTPUT = Path("/output/entry.png")


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)


if __name__ == "__main__":
    main()
