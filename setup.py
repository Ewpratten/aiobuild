# AIOBuild
# By: Evan Pratten <retrylife.ca>
# -------------------------------
# Make sure to define all project-specific settings below

# Project settings
project_config = {
    "meta":{
        "name":"AIOBuild", # Project name
        "description":"My All-In-One Python build setup", # Project description
        "readme_file":"README.md" # Filepath for project README (blank for none)
    },
    "module_info":{
        "is_script": False, # If true, this module is a console script
        "entrypoints":[], # Fill this with any entrypoints for console script
        "requirements":[ # Project requirements
            
        ]
    }
}

### Build script ###

from typing import List, Generator
import importlib
import subprocess
import os
import sys
from setuptools import setup

class MetaInstall:
    """Tools for installing required packages for the script"""
    
    # Setup requirements
    self_requires:list = ["mypy", "pylint", "pytest", "cython", "black", "isort"]
    
    def _check_loadable_packages(self) -> Generator[str, None, None]:
        """Returns a list of packages that are needed, but not installed"""
        for requirement in self.self_requires:
            try:
                mod = importlib.import_module(requirement)
                setattr(sys.modules[__name__], "requirement", mod)
            except:
                yield requirement
    
    def _install_packages(self, packages: List[str]) -> None:
        """Install all packages defined in a list"""
        for package in packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    def self_install_packages(self) -> None:
        """Automatically install all packages needed by this script"""
        
        # Get a list of all (if any) missing packages
        missing_packages:list = list(self._check_loadable_packages())
        
        # If some packages are missing, install them
        if missing_packages:
            print("Some modules needed by AIOBuild are missing. Attempting to auto-install them now")
            self._install_packages(missing_packages)
            
            # Try to load again
            missing_packages = list(self._check_loadable_packages())
            
            # If packages are still missing, abort
            if missing_packages:
                print("AIOBuild was unable to install the following required modules. Please install them manually")
                print(missing_packages)
                sys.exit(1)

class SetupCFG:
    """A tool for writing configurations to setup.cfg"""
    
    section:str
    data:str
    
    def __init__(self, section:str, data:str) ->None:
        self.section = section
        self.data = data
    
    def inject(self)->None:
        """Inject cfg"""
        
        # If no config exists, create one
        if not os.path.exists("setup.cfg"):
            with open("setup.cfg", "w") as f:
                f.write("")
                f.close()

        # Check if we need to write the data
        write_needed:bool = False
        with open("setup.cfg", "r") as f:
            write_needed = not f"[{self.section}]" in f.read()
            f.close()
        
        # If data needs to be written, write it
        if write_needed:
            print(f"{self.section} has not been configured. Injecting configuration")
            with open("setup.cfg", "a") as f:
                f.write(self.data)
                f.close()

        

def main() ->None:
    """Main script"""
    
    # Check required packages
    meta_install:MetaInstall = MetaInstall()
    meta_install.self_install_packages()
    print("Loaded packages")
    
    # Set up isort
    SetupCFG("isort","""
[isort]
multi_line_output=3
include_trailing_comma=True
force_grid_wrap=0
use_parentheses=True
line_length=88
""").inject()
    
    # if not check_isort_setup():
    #     print("Isort has not been configured. Injecting configuration")
    #     inject_isort_config()
    
    # Build setup script
    setup(
        
    )
    
    
                    

if __name__ == "__main__":
    main()
    sys.exit(0)