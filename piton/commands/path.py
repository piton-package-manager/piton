import os
from ..utils.command import BaseCommand

class Command(BaseCommand):
	name = "path"
	@classmethod
	def decorate_subparser(cls, subparser):
		subparser.add_argument("-s", "--save", action='store_true')
	@classmethod
	def run(cls, args):
		cls._run(args.save)
	@staticmethod
	def _run(save):
		if save:
			with open(os.path.join(os.path.expanduser("~"), ".bash_profile"), "a") as bash_profile:
				bash_profile.write("export PYTHONPATH=./python_modules:$PYTHONPATH")
