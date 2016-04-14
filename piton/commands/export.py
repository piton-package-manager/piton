import os
from ..utils.command import BaseCommand
from ..utils import package_json, requirements_txt

class Command(BaseCommand):
	name = "export"
	@classmethod
	def decorate_subparser(cls, subparser):
		subparser.add_argument('path', type=str, nargs='?')
	@classmethod
	def run(cls, args):
		dependencies = package_json.get_dependencies()
		if not args.path:
			requirements_txt.write_dependencies(dependencies)
		else:
			path = args.path
			requirements_txt.write_dependencies(dependencies, path)
