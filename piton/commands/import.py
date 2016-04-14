import os
from ..utils.command import BaseCommand
from ..utils import package_json, requirements_txt

class Command(BaseCommand):
	name = "import"
	@classmethod
	def decorate_subparser(cls, subparser):
		subparser.add_argument('path', type=str, nargs='?')
	@classmethod
	def run(cls, args):
		if args.path and not requirements_txt.exists(args.path):
			print("requirements file does not exist")
			return
		if not requirements_txt.exists():
			print("requirements file does not exist")
			return
		if not package_json.exists():
			print("package.json does not exist")
			return
		if not args.path:
			dependencies = requirements_txt.get_dependencies()
		else:
			dependencies = requirements_txt.get_dependencies(args.path)			
		for dependency_name, dependency_val in dependencies.items():
			package_json.add_dependency(dependency_name, dependency_val)
