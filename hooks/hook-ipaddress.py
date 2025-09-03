from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Ensure all submodules of ipaddress are included
hiddenimports = collect_submodules('ipaddress')

# Include any data files from the ipaddress package
datas = collect_data_files('ipaddress')
