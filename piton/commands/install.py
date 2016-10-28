from ..utils.command import BaseCommand
from ..utils import package_json
from ..utils.version import wanted_version, sort_versions
from ..utils.info import get_packages, Sources
from ..package import Package

class Command(BaseCommand):
	name = "install"
	@classmethod
	def decorate_subparser(cls, subparser):
		subparser.add_argument('programs', type=str, nargs='*')
		subparser.add_argument("-s", "--save", action='store_true')
	@classmethod
	def run(cls, args):
		if not args.programs:
			cls.install_all_required()
		else:
			cls.install_by_name(args.programs, save=args.save)
	@classmethod
	def install_all_required(cls):
		packages = get_packages((Sources.required, Sources.installed))
		install_queue = list(filter(lambda p: not p.installed and p.wanted_rule, packages))
		cls.install(install_queue)
	@classmethod
	def install_by_name(cls, names, **kwargs):
		install_queue = []
		for name in names:
			if "@" in name:
				split = name.split("@")
				install_queue.append(Package(name=split[0], wanted_version=split[1]))
			else:
				install_queue.append(Package(name=name))
		cls.install(install_queue)
		if "save" in kwargs and kwargs["save"]:
			for package in install_queue:
				if package.installed:
					package_json.add_dependency(package.name, package.version)
	@classmethod
	def install(cls, packages):
		for package in packages:
			cls.install_single(package)
	@classmethod
	def install_single(cls, package):
		if not package.wanted_version:
			package.get_wanted_version()
		result = package.install()
		if result:
			package.version = package.wanted_version
			package.installed = True
		return result
