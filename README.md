# piton

[![PyPI version](https://badge.fury.io/py/piton.svg)](https://badge.fury.io/py/piton)
![](https://img.shields.io/badge/python-3.4%2C%203.5-blue.svg)

Piton is a python package manager modelled after NPM. Piton makes it easier for Python developers to share and reuse code. It makes package management simple by doing the following:

- Install packages locally at `python_modules` folder

- Track dependencies in `package.json` with NodeJS-like semantic versioning

	```
	{
		"pythonDependencies": {
			"djangorestframework": "^3.3.3",
			"django": "^1.9.1"
		},
		"pythonDevDependencies": {
			"django-debug-toolbar": "1.0.0"
		}
	}
	```

- Automatic management of nested dependencies. Packages that are installed via nested dependency are removed automatically once packages requiring it are removed

- Simplify unreasonably verbose pip commands such as `install --upgrade <package> >> requirements.txt` and `list --outdated` to more human friendly npm-like commands. `update`, `outdated`, `install --save`, etc

[screenshots](/assets/screenshots)

## Future Plans

Our plans are implement all the features mentioned in the [docs](https://github.com/piton-package-manager/docs) repo.

## Installation
```
pip install piton
```
## Use
```
piton <command>
```

## Typical use case

```
piton init //creates a package.json
piton install django --save
piton install django-debug-toolbar --save
```

**IMPORTANT**: ADD python_modules as a python path

- Method 1:

	Add `.python_modules` to `PYTHONPATH` in `.bash_profile`

	Or use `piton path --save` to do it automatically.

- Method 2 (more explicit):

	Use the following code at each application entry point:

		def setup_path():
			import sys
			import os
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #OR where the python_modules folder is at
			sys.path.append(os.path.join(BASE_DIR, "python_modules"))
		setup_path()

- Method 3 (recommended):

	Use piton as a task runner:

	1. Define application entry points in `package.json` under `scripts`

		```
		{
			"scripts": {
				"develop": "python3 manage.py runserver"
			},
			"pythonDependencies": {
				...
			}
		}
		```

	2. Run task with `piton run <task>`

## Progress

| Command       | Status        |
| ------------- |:-------------:|
| init          | working       |
| outdated      | working       |
| install       | working       |
| remove        | working       |
| update        | working       |
| bugs tracker  | planned       |
| run           | working       |
| list          | working       |
| prune         | working       |
| path          | working       |

## Piton Limitations

Piton is all about making package management local. It is not meant to be a repalcement for setuptools or pip. Piton continues to use pip, setuptools, and PYPI in the background.
