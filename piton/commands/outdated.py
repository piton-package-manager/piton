import os
from ..utils import python_modules, package_json, pypi_api
from ..utils.version import wanted_version, sort_versions
from ..utils.tabulate import tabulate

class CommandOutdated():
	name = "outdated"
	@staticmethod
	def decorate_subparser(subparser):
		pass
	@classmethod
	def run(cls, args):
		cls._run()
	@classmethod
	def _run(cls):
		packages = python_modules.get_packages(os.path.join(os.getcwd(), "python_modules"))
		dependencies = package_json.get_dependencies()
		package_metadatas = []
		for dependency, version in dependencies.items():
			package_metadata = python_modules.get_package_metadata(packages, dependency)
			package_metadata["version_markup"] = version
			versions_metadata = pypi_api.get_avaliable_versions(dependency)
			# package_metadata["avaliable_versions_metadata"] = versions_metadata
			package_metadata["avaliable_versions"] = list(map(lambda version: version["version"], versions_metadata))
			package_metadata["latest"] = sort_versions(package_metadata["avaliable_versions"])[-1:][0]
			package_metadata["wanted_version"] = wanted_version(version, package_metadata["avaliable_versions"])
			if not "version" in package_metadata or (
				package_metadata["version"] != package_metadata["latest"] or
				package_metadata["version"] != package_metadata["wanted_version"]):
				package_metadatas.append(package_metadata)
		cls.display_outdated(package_metadatas)
	@staticmethod
	def display_outdated(metadatas):
		class Colors:
			PURPLE = '\033[95m'
			OKBLUE = '\033[94m'
			OKGREEN = '\033[92m'
			WARNING = '\033[93m'
			FAIL = '\033[91m'
			UNDERLINE = '\033[4m'
			ENDC = '\033[0m'

		headings = ["Package", "current", "wanted", "latest"]
		headings = list(map(lambda heading: Colors.UNDERLINE+heading+Colors.ENDC, headings))
		table = []
		metadatas = sorted(metadatas, key=lambda metadata: metadata["name"])
		for metadata in metadatas:
			if "version" in metadata:
				current_version = metadata["version"]
			else:
				current_version = "n/a"
			table.append([
				Colors.OKGREEN+metadata["name"]+Colors.ENDC,
				current_version,
				Colors.OKGREEN+metadata["wanted_version"]+Colors.ENDC,
				Colors.PURPLE+metadata["latest"]+Colors.ENDC
			])
		print(tabulate(table, headings, tablefmt="plain"))