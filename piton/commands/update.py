import os
from ..utils.command import BaseCommand
from ..utils import python_modules, package_json, pypi_api, installer, version

class Command(BaseCommand):
	name = "update"
	@classmethod
	def decorate_subparser(cls, subparser):
		subparser.add_argument('programs', type=str, nargs='*')
	@classmethod
	def run(cls, args):
		if not args.programs:
			dependencies = package_json.get_dependencies()
			cls.update(list(dependencies.keys()))
		else:
			cls.update(args.programs)
	@classmethod
	def update(cls, packages):
		installed_package_metadatas = python_modules.get_packages(os.path.join(os.getcwd(), "python_modules"))
		dependencies = package_json.get_dependencies()
		install_queue = []
		for package in packages:
			if not package in dependencies:
				continue
			package_json_version = dependencies[package]
			versions_metadata = pypi_api.get_avaliable_versions(package)
			if not versions_metadata:
				continue
			avaliable_versions = list(map(lambda version: version["version"], versions_metadata))
			wanted_version = version.wanted_version(package_json_version, avaliable_versions)
			for metadata in installed_package_metadatas:
				if metadata["name"] == package and metadata["version"] == wanted_version:
					continue
			install_queue.append({
				"name": package,
				"version": wanted_version
			})
		for item in install_queue:
			installer.remove(package)
			installer.install(package, wanted_version)
