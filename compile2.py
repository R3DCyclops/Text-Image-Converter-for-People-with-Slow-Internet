import subprocess
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

script_path = os.path.join(current_dir, "bnwconvert.py")

output_dir = os.path.join(current_dir, "dist")

icon_path = os.path.join(current_dir, "ico.ico")


additional_files = [
    f'{icon_path};.',
]

command = [
    'pyinstaller',
    '--onefile',
    '--noconsole',
    '--hidden-import=PySide6',
    '--hidden-import=Pillow',
    '--hidden-import=numpy',
    '--icon', icon_path,
    '--distpath', output_dir,
] + ['--add-data', additional_files[0]] + [script_path]

subprocess.run(command)

print(f".exe saved in folder: {output_dir}")