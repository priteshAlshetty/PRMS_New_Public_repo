from cx_Freeze import setup, Executable
import sys
import os
# Dependencies are automatically detected, but some modules need help.
build_exe_options = {
    "packages": ["os","flask","mysql.connector","openpyxl"],
    "excludes": ["tkinter"],
    "include_files": [
        os.path.join('BKT_project\\templates',"")]  # Include templates and static files
}

# Base set to None for console application.
base = None

# If your application uses GUI, use "Win32GUI" instead of None
# base = "Win32GUI"

setup(
    name = "MyFlaskApp",
    version = "0.1",
    description = "My Flask Application!",
    options = {"build_exe": build_exe_options},
    executables = [Executable("BKT_project\\server.py", base=base)]
)