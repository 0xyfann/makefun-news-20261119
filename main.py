"""Write the pre-rendered front page without third-party dependencies."""

import os
import shutil
from pathlib import Path


def main() -> None:
    source = Path(__file__).resolve().with_name("entry.png")
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, output_dir / source.name)


if __name__ == "__main__":
    main()
