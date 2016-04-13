import os
import json
from collections import OrderedDict
from ..utils.command import BaseCommand
import inquirer

_instructions = """This utility will walk you through creating a package.json file.
It only covers the most common items, and tries to guess sensible defaults.

See `piton help json` for definitive documentation on these fields
and exactly what they do.

Use `piton install <pkg> --save` afterwards to install a package and
save it as a dependency in the package.json file.

Press ^C at any time to quit."""

class Command(BaseCommand):
	name = "init"
	@classmethod
	def run(cls, args):
		package_file_path = os.path.join(os.getcwd(), 'package.json')
		if os.path.isfile(package_file_path):
			print("package.json already exists")
			return
		print(_instructions)
		questions = [
			inquirer.Text('name', message="name", default=os.getcwd().split(os.sep)[-1]),
			inquirer.Text('version', message="version", default="1.0.0"),
			inquirer.Text('description', message="description"),
			inquirer.Text('git_repo', message="git repository"),
			inquirer.Text('author', message="author"),
			inquirer.Text('license', message="license"),
		]
		answers = inquirer.prompt(questions)
		file_content = OrderedDict()
		file_content["name"] = answers.get("name")
		file_content["version"] = answers.get("version")
		file_content["description"] = answers.get("description")
		file_content["git_repo"] = answers.get("git_repo")
		file_content["author"] = answers.get("author")
		file_content["license"] = answers.get("license")
		file_content["pythonDependencies"] = {}
		print(json.dumps(file_content, indent=2))
		questions = [inquirer.Text('ok', message="Is this ok?", default="yes"),]
		answers = inquirer.prompt(questions)
		if answers["ok"] == "yes":
			with open(package_file_path, 'w') as outfile:
				json.dump(file_content, outfile, indent=2)
		else:
			print("Aborted.")
