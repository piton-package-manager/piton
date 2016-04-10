import os
from subprocess import call
from ..utils import package_json

class CommandRun():
	name = "run"
	@staticmethod
	def decorate_subparser(subparser):
		subparser.add_argument('script', type=str)
	@classmethod
	def run(cls, args):
		cls._run(args.script)
	@staticmethod
	def _run(script):
		script_content = package_json.get_script(script)
		if not script_content:
			print("Unable to find script "+script)
			return
		call("export PYTHONPATH=./python_modules:$PYTHONPATH;"+" "+script_content, shell=True)
