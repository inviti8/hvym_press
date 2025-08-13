import shutil
import subprocess
from pathlib import Path
import argparse
import os
import platform

parser = argparse.ArgumentParser()
parser.add_argument("--test", help="copy executable to local install directory", action="store_true")
parser.add_argument("--mac", help="copy executable to mac local install directory", action="store_true")
args = parser.parse_args()

# get current working directory
cwd = Path.cwd()

def clean_dir(dir):
    for item in dir.iterdir():
        if item.name != '.git' and item.name != 'README.md' and item.name != 'install.sh':
            if item.is_file():
                item.unlink()
            else:
                shutil.rmtree(item)

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
build_dir = cwd / 'build'
template_dir = cwd / 'templates'
template_copied_dir = build_dir / 'templates'
img_dir = cwd / 'images'
img_copied_dir = build_dir / 'images'
serve_dir = cwd / 'serve'
serve_copied_dir = build_dir / 'serve'

# Platform-specific paths
current_platform = platform.system().lower()
if current_platform == "darwin":  # macOS
    dist_dir = build_dir / 'dist' / 'mac'
elif current_platform == "windows":
    dist_dir = build_dir / 'dist' / 'windows'
else:  # Linux and others
    dist_dir = build_dir / 'dist' / 'linux'

# Override with command line argument if specified
if args.mac:
    dist_dir = build_dir / 'dist' / 'mac'

release_dir = cwd / 'release'
release_linux = release_dir / 'linux'

# check if build dir exists, if not create it
if not build_dir.exists():
    build_dir.mkdir()
else: # delete all files inside the directory
    clean_dir(build_dir)

# check if release dir exists, if not create it
if not release_dir.exists():
    release_dir.mkdir()
else: # delete all files inside the directory
    clean_dir(release_dir)

# Create dist subdirectory
dist_dir.mkdir(parents=True, exist_ok=True)

for file in files:
    # copy source files to build directory
    shutil.copy(file, build_dir)

shutil.copytree(template_dir, build_dir / template_dir.name)
shutil.copytree(img_dir, build_dir / img_dir.name)
shutil.copytree(serve_dir, build_dir / serve_dir.name)

# install dependencies from requirements.txt
subprocess.run(['pip', 'install', '-r', str(build_dir / file11.name)], check=True)

# Platform-specific PyInstaller commands
if current_platform == "windows":
    executable_name = "hvym_press.exe"
    add_data_sep = ";"
else:
    executable_name = "hvym_press"
    add_data_sep = ":"

# build the python script into an executable using PyInstaller
subprocess.run(['pyinstaller', str(file1), str(file2), str(file3), str(file4), str(file5), str(file6), str(file7), str(file8), str(file9), str(file10), '--onefile', '--name=hvym_press',  f'--distpath={dist_dir}', '--add-data', f'templates{add_data_sep}templates', '--add-data', f'images{add_data_sep}images', '--add-data', f'serve{add_data_sep}serve'], check=True)

# copy the executable to the release directory
shutil.move(str(dist_dir / executable_name), str(release_dir))

# copy built executable to destination directory
# if args.test:
#     if current_platform == "windows":
#         test_dir = Path(os.path.expanduser('~')) / 'AppData' / 'Local' / 'heavymeta-cli'
#     else:
#         test_dir = Path('/home/desktop/.local/share/heavymeta-cli')
#     shutil.copy(str(dist_dir / executable_name), test_dir)
#     if current_platform != "windows":
#         subprocess.run(['chmod', '+x', str(test_dir / executable_name)], check=True)

