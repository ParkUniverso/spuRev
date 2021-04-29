#executar esse comando no powershell ou cmd para compilar o codigo: python setup.py bdist_msi
from cx_Freeze import setup, Executable
includefiles = [('ico/spu.ico','ico/spu.ico')]
includes = []
excludes = []
packages = []
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "SPU",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]main.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]
msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data}
setup(
    name = "SPU",
    version = "6.8",
    description = "Sistema de provisionamento unificado (Ísis)",
options = {"bdist_msi": bdist_msi_options,'build_exe': {'includes':includes,'excludes':excludes,'packages':packages,'include_files':includefiles,'include_msvcr': True}},
    executables = [Executable("main.py", base = "Win32GUI",
    icon="ico/spu.ico")]
    )