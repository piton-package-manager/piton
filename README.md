#Python Package Manager

A python package manager modelled after npm, the ONE TRUE PACKAGE MANAGER.

[![PyPI version](https://badge.fury.io/py/python_package_manager.svg)](https://badge.fury.io/py/python_package_manager)
![](https://img.shields.io/badge/type-shitpost-brightgreen.svg)
![](https://img.shields.io/packagist/l/doctrine/orm.svg)
![](https://img.shields.io/badge/python-3.4%2C%203.5-blue.svg)

Let's face it, python package management is a failure. 

- Support for project-specific packages is non-existent
- Virtualenv is a disaster
- Keeping track of requirements.txt is impossible
- No nested dependencies.

PPM will fix this by doing the following:

- Install packages locally at `python_modules` folder

- Track dependencies in `package.json` the with NodeJS-like semantic versioning

		{
			"pythonDependencies": {
				"djangorestframework": "^3.3.3",
				"django": "^1.9.1"
			},
			"pythonDevDependencies": {
				"django-debug-toolbar": "1.0.0"
			}
		}

- Automatic management of nested dependencies. Packages that are installed via nested dependency are removed automatically once packages requiring it are removed

- Simplify unreasonably verbose pip commands such as `install --upgrade <package> >> requirements.txt` and `list --outdated` to more human friendly npm-like commands. `update`, `outdated`, `install --save`, etc

PPM is also a strong proponent for microlibraries. Reusing productive code like what the Node community has done with Left-Pad is what python needs to move forward in the webscale era.

## Installation

	pip install python_package_manager

## Use

	ppm <command>

## Typical use case

	ppm init //creates a package.json
	ppm install django --save
	ppm install django-debug-toolbar --save

IMPORTANT: ADD python_modules as a python path

- Method 1:

	Add `.python_modules` to `PYTHONPATH` in `.bash_profile`

- Method 2 (more explicit):

	Use the following code at each application entry point:

		def setup_path():
			import sys
			import os
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #OR where the python_modules folder is at
			sys.path.append(os.path.join(BASE_DIR, "python_modules"))
		setup_path()

## Features

| Command       | Status        |
| ------------- |:-------------:|
| init          | working       |
| outdated      | working       |
| install       | working       |
| remove        | working       |
| update        | in-progress   |
| list          | working       |
| prune         | working       |

## PPM Limitations

PPM is all about making package management local. It is not meant to be a repalcement for setuptools or pip. PPM continues to use pip, setuptools, and PYPI in the background.
