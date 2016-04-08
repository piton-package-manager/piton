import os
from ..utils import python_modules, package_json

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
		def package_json_if_save(save):
			if save:
				dependencies = package_json.get_dependencies()
				dependencies.pop(package, None)
				package_json.write_dependencies(dependencies)
		import shutil
		metadata = python_modules.get_package(os.path.join(os.getcwd(), "python_modules"), package)
		if not metadata:
			print("package "+package+" is not installed")
			package_json_if_save(save)
			return
		pending_removals = []
		pending_removals += metadata["top_level"]
		pending_removals.append(metadata["dist_info"])
		for pending_removal in pending_removals:
			try:
				shutil.rmtree(os.path.join("python_modules", pending_removal))
			except:
				try:
					os.remove(os.path.join("python_modules", pending_removal+".py"))
				except:
					pass
		package_json_if_save(save)
	@classmethod
	def execute(cls, package):
		# Code interface
		cls._run(package, False)
