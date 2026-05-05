#!/usr/bin/env python
# © Deltablot 2026
# License: MIT

"""
This script localizes image paths in Jupyter notebooks for a target language.

Workflow:
- English notebooks under notebooks/en/ are the source of truth
- Other language notebooks (e.g. notebooks/jp/) are generated/copied from EN
- Image assets are stored per language under images/<lang>/

What this script does:
- Takes a language code as a command-line argument (e.g. "jp")
- Scans only notebooks under notebooks/<lang>/
- Updates Markdown cells only (code cells are never modified)
- Rewrites image paths so that:
    ../../images/en/ → ../../images/<lang>/
This way, I can copy/paste notebooks/en to other languages, and the images path will be handled by the script. As we're
 performing this workshop in english, I did not see usage for the internationalization plugins that translates the whole
 document. Maybe we'll see later if some institutes want to have the whole workshop traduced, in which case we'll try it.

What this script does NOT do:
- It does NOT touch notebooks/en/
- It does NOT modify assets or images on disk
- It does NOT affect any other language folders

The script is safe to run multiple times (idempotent) and only applies changes where necessary.
"""
"""
Example usage and output:
Argument passed here is "jp":
uv run scripts/update_image_path.py jp
✔ Updated: notebooks/jp/part1-intro.ipynb
✔ Updated: notebooks/jp/part2-curl.ipynb
✔ Updated: notebooks/jp/part3-python.ipynb
✔ Updated: notebooks/jp/.ipynb_checkpoints/part1-intro-checkpoint.ipynb
✔ Updated: notebooks/jp/.ipynb_checkpoints/part2-curl-checkpoint.ipynb
✔ Updated: notebooks/jp/.ipynb_checkpoints/part3-python-checkpoint.ipynb

Now all images in notebooks/jp have images path as: "../../images/jp/" :)
"""

import sys
import nbformat
from pathlib import Path

SOURCE_PREFIX = "../../images/en/"
IMAGES_BASE = "../../images"

def update_notebook_image_paths(nb_path: Path, lang: str) -> bool:
    nb = nbformat.read(nb_path, as_version=4)
    modified = False
    target_prefix = f"{IMAGES_BASE}/{lang}/"

    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue

        if SOURCE_PREFIX in cell.source:
            cell.source = cell.source.replace(SOURCE_PREFIX, target_prefix)
            modified = True

    if modified:
        nbformat.write(nb, nb_path)

    return modified


def process_language(lang: str):
    notebooks_dir = Path("notebooks") / lang

    if not notebooks_dir.exists():
        raise FileNotFoundError(f"{notebooks_dir} does not exist")

    for nb_path in notebooks_dir.rglob("*.ipynb"):
        changed = update_notebook_image_paths(nb_path, lang)
        if changed:
            print(f"✔ Updated: {nb_path}")
        else:
            print(f"– No change: {nb_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_image_path.py <language>")
        print("Example: python update_image_path.py jp")
        sys.exit(1)

    language = sys.argv[1]
    process_language(language)
