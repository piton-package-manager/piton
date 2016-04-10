import os
from ..utils import installer, package_json

class CommandRemove():
	name = "remove"
	@staticmethod
	def decorate_subparser(subparser):
		subparser.add_argument('program', type=str, nargs='?')
		subparser.add_argument("-s", "--save", action='store_true')
	@classmethod
	def run(cls, args):
		cls._run(args.program, args.save)
	@staticmethod
	def _run(package, save):
		removed = installer.remove(package)
		if not removed:
			print("package "+package+" is not installed")
		if save:
			dependencies = package_json.get_dependencies()
			dependencies.pop(package, None)
			package_json.write_dependencies(dependencies)
	@classmethod
	def execute(cls, package):
		# Code interface
		cls._run(package, False)
