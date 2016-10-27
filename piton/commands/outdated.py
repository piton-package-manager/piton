import os
from ..utils.command import BaseCommand
from ..utils import python_modules, package_json, pypi_api
from ..utils.version import wanted_version, sort_versions
from ..utils.tabulate import tabulate

def merge(packages_1, packages_2):
	name_map = {}
	for package in packages_1 + packages_2:
		if not package.name in name_map:
			name_map[package.name] = package
		else:
			name_map[package.name].merge(package)
	arr = []
	for name in name_map:
		arr.append(name_map[name])
	return arr

class Colors:
	PURPLE = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	UNDERLINE = '\033[4m'
	ENDC = '\033[0m'

class Command(BaseCommand):
	name = "outdated"
	@classmethod
	def run(cls, args):
		cls._run()
	@classmethod
	def _run(cls):
		packages = python_modules.get_packages(os.path.join(os.getcwd(), "python_modules"))
		dependencies = package_json.get_dependencies()
		packages = merge(packages, dependencies)
		packages = list(filter(lambda p: p.wanted_version, packages)) # filter out ones with no wanted version (not in package.json)
		packages_to_display = []
		for package in packages:
			versions_metadata = pypi_api.get_avaliable_versions(package.name)
			package.avaliable_versions = list(map(lambda version: version["version"], versions_metadata))
			package.latest_version = sort_versions(package.avaliable_versions)[-1:][0]
			if len(package.avaliable_versions):
				package.wanted_version = wanted_version(package.wanted_version, package.avaliable_versions)
			if not package.version or (
				package.version != package.latest_version or
				package.version != package.wanted_version):
				packages_to_display.append(package)
		cls.display_outdated(packages_to_display)
	@staticmethod
	def display_outdated(packages):
		if len(packages) == 0:
			return
		headings = ["package", "current", "wanted", "latest"]
		headings = list(map(lambda heading: Colors.UNDERLINE+heading+Colors.ENDC, headings))
		table = []
		packages = sorted(packages, key=lambda package: package.name)
		for package in packages:
			table.append([
				Colors.OKGREEN+package.name+Colors.ENDC,
				package.version or "n/a",
				Colors.OKGREEN+package.wanted_version or "n/a"+Colors.ENDC,
				Colors.PURPLE+package.latest_version or "n/a"+Colors.ENDC
			])
		print(tabulate(table, headings, tablefmt="plain"))
