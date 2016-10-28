from ..utils.command import BaseCommand
from ..utils import pypi_api, installer, version
from ..utils.info import get_packages, Sources

class Command(BaseCommand):
	name = "update"
	@classmethod
	def decorate_subparser(cls, subparser):
		subparser.add_argument('programs', type=str, nargs='*')
	@classmethod
	def run(cls, args):
		if not args.programs:
			cls.update_all()
		else:
			cls.update_some(args.programs)
	@classmethod
	def update_some(cls, program_names):
		packages = get_packages((Sources.required, Sources.installed))
		packages = list(filter(lambda p: p.name in program_names, packages))
		install_queue = []
		for package in packages:
			cls.update_single(package, install_queue)
		for item in install_queue:
			installer.remove(item["name"])
			installer.install(item["name"], item["version"])
	@classmethod
	def update_all(cls):
		packages = get_packages((Sources.required, Sources.installed))
		install_queue = []
		for package in packages:
			cls.update_single(package, install_queue)
		for item in install_queue:
			installer.remove(item["name"])
			installer.install(item["name"], item["version"])
	@classmethod
	def update_single(cls, package, install_queue):
		package.get_wanted_version()
		if not package.installed or package.version != package.wanted_version:
			install_queue.append({
				"name": package.name,
				"version": package.wanted_version
			})
