#Python Package Manager

A python package manager modelled after npm, the ONE TRUE PACKAGE MANAGER.

![](https://img.shields.io/badge/type-shitpost-brightgreen.svg)
![](https://img.shields.io/badge/maintained-yes-brightgreen.svg)
![](https://img.shields.io/packagist/l/doctrine/orm.svg)
![](https://img.shields.io/badge/python-3.4%2C%203.5-blue.svg)
![](https://img.shields.io/badge/downloads-9000%2B%2Ftotal-green.svg)

Let's face it, python package management is a failure. 

- Support for project-specific packages is non-existent
- Virtualenv is a disaster
- Keeping track of requirements.txt is impossible
- No nested dependencies.

PPM will fix this by doing the following:

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

This project is not complete

## Features

| Command       | Status        |
| ------------- |:-------------:|
| outdated      | working       |
| install       | working       |
| remove        | working       |
| update        | in-progress   |
| list          | working       |
| prune         | working       |

## PPM Limitations

PPM is all about making package management local. It is not meant to be a repalcement for setuptools or pip. PPM continues to use pip, setuptools, and PYPI in the background.
