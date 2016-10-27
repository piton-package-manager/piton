import os
from ..utils.command import BaseCommand
from ..utils import python_modules, package_json, pypi_api, installer
from ..utils.version import wanted_version, sort_versions
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
		installed_package_metadatas = python_modules.get_packages(os.path.join(os.getcwd(), "python_modules"))
		installed_package_names = list(map(lambda md: md.name, installed_package_metadatas))
		dependencies = package_json.get_dependencies()
		install_queue = []
		for dependency in dependencies:
			if not dependency.name in installed_package_names:
				install_queue.append(dependency)
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
			for installed in install_queue:
				package_json.add_dependency(installed.name, installed.version)
	@classmethod
	def install(cls, packages):
		for package in packages:
			cls.install_single(package)
	@classmethod
	def install_single(cls, package):
		if not package.wanted_version:
			result = cls.install_latest(package)
			return result
		else:
			versions = list(map(lambda md: md["version"], pypi_api.get_avaliable_versions(package.name)))
			if not versions:
				return False
			wanted = wanted_version(package.version, versions)
			if not wanted:
				print("No suitable version for "+package.name)
				return False
			result = installer.install(package.name, wanted)
			package.version = package.wanted_version
			package.installed = True
			return True
	@classmethod
	def install_latest(cls, package):
		avaliable_versions = pypi_api.get_avaliable_versions(package.name)
		if avaliable_versions == None:
			print("Unable to find package "+package.name)
			return False
		if len(avaliable_versions) == 0:
			print("Unable to find releases for package "+package.name)
			return False
		versions = list(map(lambda version: version["version"], avaliable_versions))
		latest_version = sort_versions(versions)[-1:][0]
		installer.install(package.name, latest_version, True)
		package.version = latest_version
		package.wanted_version = latest_version
		package.installed = True
		return True
