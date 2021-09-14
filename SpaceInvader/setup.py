import sys
from cx_Freeze import setup, Executable

include_files = ['autorun.inf']
base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(name="SpaceInvader",
      version="0.1",
      description="Simple video game",
      options={'build_exe': {'include_files': include_files}},
      executables=[Executable("Main.py", base=base)])