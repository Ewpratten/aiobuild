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
        "path":"testmod", # Module path
        "is_script": False, # If true, this module is a console script
        "entrypoints":[], # Fill this with any entrypoints for console script
        "requirements":[ # Project requirements
            
        ]
    }
}

### Configuration file sections ###

isort_cfg = """
[isort]
multi_line_output=3
include_trailing_comma=True
force_grid_wrap=0
use_parentheses=True
line_length=88
"""

bandit_skips = ["B603"]

mypy_cfg = """
[mypy]
ignore_missing_imports=true
"""

### Build script ###

import distutils.cmd
import distutils.log
import importlib
import os
import subprocess
import sys
from typing import Generator, List

import setuptools.command.build_py
from setuptools import setup


class RequiredModule:
    """Info about required modules"""
    
    package:str
    do_import:bool
    import_name:str
    
    def __init__(self, package:str, do_import:bool, import_name:str=""):
        self.package = package
        self.do_import = do_import
        self.import_name = import_name if import_name != "" else package

class MetaInstall:
    """Tools for installing required packages for the script"""
    
    # Setup requirements
    self_requires:list = [RequiredModule("mypy", True), RequiredModule("pylint", True), 
                          RequiredModule("pytest", True), RequiredModule("pytest-cov", True, "pytest"), 
                          RequiredModule("cython", True), RequiredModule("black", True), 
                          RequiredModule("isort", True), RequiredModule("bandit", True)]
    
    def _check_loadable_packages(self) -> Generator[str, None, None]:
        """Returns a list of packages that are needed, but not installed"""
        for requirement in self.self_requires:
            try:
                mod = importlib.import_module(requirement.import_name)
                setattr(sys.modules[__name__], requirement.import_name, mod)
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

class PylintCommand(distutils.cmd.Command):
    """A custom command to run Pylint on all Python source files."""
    
    description = 'run Pylint on Python source files'
    
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass
    
    def run(self):
        """Run command."""
               
        try:
            subprocess.check_call([sys.executable, "-m", "pylint", project_config["module_info"]["path"]])
        except subprocess.CalledProcessError as e:
            print("Pylint encountered an error. Is the project module real?")

class MyPyCommand(distutils.cmd.Command):
    """A custom command to run mypy on all Python source files."""
    
    description = 'run mypy on Python source files'
    
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass
    
    def run(self):
        """Run command."""
        subprocess.check_call([sys.executable, "-m", "mypy", project_config["module_info"]["path"]])

class BlackCommand(distutils.cmd.Command):
    """A custom command to run black on all Python source files."""
    
    description = 'run black on Python source files'
    
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass
    
    def run(self):
        """Run command."""
        subprocess.check_call([sys.executable, "-m", "black", project_config["module_info"]["path"]])

class IsortCommand(distutils.cmd.Command):
    """A custom command to run isort on all Python source files."""
    
    description = 'run isort on Python source files'
    
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass
    
    def run(self):
        """Run command."""
        subprocess.check_call([sys.executable, "-m", "isort", "-y", "--recursive", project_config["module_info"]["path"]])

class BanditCommand(distutils.cmd.Command):
    """A custom command to run bandit on all Python source files."""
    
    description = 'run bandit on Python source files'
    
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass
    
    def run(self):
        """Run command."""
        subprocess.check_call([sys.executable, "-m", "bandit", "-r", "-s",  ','.join(bandit_skips), project_config["module_info"]["path"]])
        

class LintCommand(setuptools.command.build_py.build_py):
    """Lint all the things"""
    
    description = 'Lint and fix all source files'
    
    def run(self) ->None:
        
        # Exec all steps
        try:
            self.run_command("exec_black")
            self.run_command("exec_isort")
            self.run_command("exec_bandit")
            self.run_command("exec_mypy")
            self.run_command("exec_pylint")
        except subprocess.CalledProcessError as e:
            print("Linting error. Stopped.")
            sys.exit(1)
        
        # Run self
        setuptools.command.build_py.build_py.run(self)


def _setup_self()->None:
    """Set up everything required by the script"""
    
    # Check required packages
    meta_install:MetaInstall = MetaInstall()
    meta_install.self_install_packages()
    print("Loaded packages")
    
    # Set up isort
    SetupCFG("isort",isort_cfg).inject()
    
    
    # Set up mypy
    SetupCFG("mypy", mypy_cfg).inject()
    
        

def main() ->None:
    """Main script"""
    
    _setup_self()
    
    
    # Build setup script
    setup(
        cmdclass={
            "exec_pylint":PylintCommand,
            "exec_mypy":MyPyCommand,
            "exec_black":BlackCommand,
            "exec_isort":IsortCommand,
            "exec_bandit":BanditCommand,
            "lint":LintCommand 
        }
    )
                    

if __name__ == "__main__":
    main()
    sys.exit(0)
