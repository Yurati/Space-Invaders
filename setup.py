import os

import cx_Freeze

os.environ['TCL_LIBRARY'] = r'C:\Users\Lukasz\AppData\Local\Programs\Python\Python37\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r':\Users\Lukasz\AppData\Local\Programs\Python\Python37\tcl\tk8.6'

executables = [cx_Freeze.Executable("Space.py")]
cx_Freeze.setup(
    name="Space Invaders",
    version="1.0",
    author="Lukasz Dudek",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":['Images/', 'Font/', 'sounds/']}},
    executables=executables
)
