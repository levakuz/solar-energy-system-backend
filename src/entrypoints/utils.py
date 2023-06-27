import os
from pathlib import Path


def create_static_dirs():
    static_files_dirs = [
        Path('./src/staticfiles'),
        Path('./src/staticfiles/device_types_photos'),
        Path('./src/staticfiles/report_charts'),
    ]
    for static_files_dir in static_files_dirs:
        if not static_files_dir.is_dir():
            os.mkdir(static_files_dir)