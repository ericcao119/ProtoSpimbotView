import binascii
import os
import string
from pathlib import Path

# Run 'python generate_images.py' from the SpimBOT folder.
# This script will take the images cpp and h templates and
# append all pngs and gifs from the SpimBOT/images folder
# as extern QImage variables named filename_ext.
# e.g. background.gif can be accessed as background_gif.
# Use #include "images.h" to use these QImage variables.

# Using gif over png is recommended, gif is smaller.
# And libpng on ews machines throws warnings
# on some non-standard pngs and confuses students
# (e.g. some Photoshop png settings cause this).

OUT_FILE = Path(__file__).parent / "images.py"
IMG_DIR = Path(__file__).parent / "../res/"


def sanitize_filename(file_path: str) -> str:
    """
    >>> sanitize_filename("blue_grenade.png")
    ... blue_grenade_png
    """
    file_name = file_path.lower().replace(" ", "_").replace(".", "_")
    file_name = "".join(
        [
            i if i in (string.ascii_letters + string.digits + "_") else ""
            for i in file_name
        ]
    )
    return file_name


def valid_format(file_path: str) -> bool:
    accepted_types = {".png", ".gif"}
    return any(file_path.lower().endswith(t) for t in accepted_types)


with OUT_FILE.open("w") as out:

    out.write("from PyQt5.QtGui import QColor, QPainter, QBrush, QPen, QImage\n\n")

    for file_path in os.listdir(IMG_DIR):
        if valid_format(file_path):
            file_name = sanitize_filename(file_path)

            out.write(f'{file_name} = QImage("{IMG_DIR/file_path}")\n')
