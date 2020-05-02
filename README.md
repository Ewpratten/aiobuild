# aiobuild
My All-In-One Python build setup

## What is this?

This project contains a self-contained `setup.py` file that can be dropped into any Python3 project. It provides the following commands

```sh
# Lint code (and auto-fix)
python3 setup.py lint

# Test code
python3 setup.py test

# Run a full project check
python3 setup.py check
```

The checksyle rules (although configurable) are very strict to force you to write very good, clean code.

## Installation

Just copy this project's `setup.py` file into your project, and set your own metadata at the top of the file