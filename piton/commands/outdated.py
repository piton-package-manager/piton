from ..utils.command import BaseCommand
from ..utils.tabulate import tabulate
from ..utils.info import get_packages, Sources

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
		packages = get_packages((Sources.required, Sources.installed))
		packages = list(filter(lambda p: p.wanted_rule, packages)) # filter out ones with no wanted version (not in package.json)
		packages_to_display = []
		for package in packages:
			package.get_wanted_version()
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
				Colors.OKGREEN+(package.wanted_version or "n/a")+Colors.ENDC,
				Colors.PURPLE+(package.latest_version or "n/a")+Colors.ENDC
			])
		print(tabulate(table, headings, tablefmt="plain"))
