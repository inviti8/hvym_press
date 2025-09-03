from PyInstaller.utils.hooks import collect_submodules

# This ensures all submodules of ipaddress are included
hiddenimports = collect_submodules('ipaddress')
