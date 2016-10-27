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
			cls.update_single(package, dependencies, installed_package_metadatas, install_queue)
		for item in install_queue:
			installer.remove(item["name"])
			installer.install(item["name"], item["version"])
	@classmethod
	def update_single(cls, package_name, dependencies, installed_package_metadatas, install_queue):
		found = False
		for dependency in dependencies:
			if dependency.name == package_name:
				found = True
				wanted_version = dependency.wanted_version
				break
		get_latest = not found
		versions_metadata = pypi_api.get_avaliable_versions(package_name)
		if not versions_metadata:
			return False
		avaliable_versions = list(map(lambda version: version["version"], versions_metadata))
		if get_latest:
			wanted_version = avaliable_versions[-1:][0]
		else:
			wanted_version = version.wanted_version(dependency.wanted_version, avaliable_versions)
		for metadata in installed_package_metadatas:
			if metadata.name == package_name and metadata.version == wanted_version:
				continue
		install_queue.append({
			"name": package_name,
			"version": wanted_version
		})
