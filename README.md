# piton

Piton is a python package manager modelled after NPM. Piton makes it easier for Python developers to share and reuse code. Piton will do this by doing the following:

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
| bugs tracker  | in-progress   |
| user scripts  | in-progress   |
| list          | working       |
| prune         | working       |

## Piton Limitations

Piton is all about making package management local. It is not meant to be a repalcement for setuptools or pip. Piton continues to use pip, setuptools, and PYPI in the background.
