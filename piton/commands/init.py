import os
import json

class CommandInit():
	name = "init"
	@staticmethod
	def decorate_subparser(subparser):
		pass
	@classmethod
	def run(cls, args):
		cls._run()
	@staticmethod
	def _run():
		package_file_path = os.path.join(os.getcwd(), 'package.json')
		if os.path.isfile(package_file_path):
			print("package.json already exists")
			return
		with open(package_file_path, 'w') as outfile:
			file_content = {
				"pythonDevDependencies": {},
				"pythonDependencies": {}
			}
			json.dump(file_content, outfile, indent=2)
