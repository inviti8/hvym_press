import shutil
import subprocess
from pathlib import Path
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--test", help="copy executable to local install directory", action="store_true")
parser.add_argument("--mac", help="copy executable to mac local install directory", action="store_true")
args = parser.parse_args()

# get current working directory
cwd = Path.cwd()

# source files
file1 = cwd / 'app.py'
file2 = cwd / 'ColorPicker.py'
file3 = cwd / 'HVYM.py'
file4 = cwd / 'IconPicker.py'
file5 = cwd / 'LoadingWindow.py'
file6 = cwd / 'MarkdownHandler.py'
file7 = cwd / 'ServerHandler.py'
file8 = cwd / 'SiteDataHandler.py'
file9 = cwd / 'TreeData.py'
file10 = cwd / 'W3DeployHandler.py'
file11 = cwd / 'requirements.txt'

files = [file1, file2, file3, file4, file5, file6, file7, file8, file9, file10, file11]

# target directories for the build folder and files
#build_dir = cwd.parent / 'hvym'
build_dir = cwd / 'build'
template_dir = cwd / 'templates'
template_copied_dir = build_dir / 'templates'
img_dir = cwd / 'images'
img_copied_dir = build_dir / 'images'
serve_dir = cwd / 'serve'
serve_copied_dir = build_dir / 'serve'
dist_dir = build_dir / 'dist' / 'linux'

if args.mac:
    dist_dir = build_dir / 'dist' / 'mac'


# check if build dir exists, if not create it
if not build_dir.exists():
    build_dir.mkdir()
else: # delete all files inside the directory
    for item in build_dir.iterdir():
        if item.name != '.git' and item.name != 'README.md' and item.name != 'install.sh':
            if item.is_file():
                item.unlink()
            else:
                shutil.rmtree(item)


for file in files:
    # copy source files to build directory
    shutil.copy(file, build_dir)

shutil.copytree(template_dir, build_dir / template_dir.name)
shutil.copytree(img_dir, build_dir / img_dir.name)
shutil.copytree(serve_dir, build_dir / serve_dir.name)

# install dependencies from requirements.txt
subprocess.run(['pip', 'install', '-r', str(build_dir / file11.name)], check=True)

# build the python script into an executable using PyInstaller
subprocess.run(['pyinstaller', str(file1), str(file2), str(file3), str(file4), str(file5), str(file6), str(file7), str(file8), str(file9), str(file10), '--onefile', '--name=hvym_press',  f'--distpath={dist_dir}', '--add-data', 'templates:templates', '--add-data', 'images:images', '--add-data', 'serve:serve'], check=True)
#subprocess.run(['pyinstaller', '--onefile', f'--distpath={dist_dir}', '--add-data', 'templates:templates', '--add-data', 'images:images', '--add-data', 'data:data', '--add-data', 'npm_links:npm_links',  str(build_dir / src_file1.name)], check=True)
# copy built executable to destination directory
# if args.test:
#     test_dir = Path('/home/desktop/.local/share/heavymeta-cli')
#     shutil.copy(str(dist_dir / (file1.stem )), test_dir)
#     subprocess.Popen('chmod +x ./hvym', cwd=test_dir, shell=True, stderr=subprocess.STDOUT)

