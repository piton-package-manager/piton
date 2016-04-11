import os
from ..utils.command import BaseCommand
from ..utils import python_modules, package_json, pypi_api, installer
from ..utils.version import wanted_version, sort_versions

class Command(BaseCommand):
	name = "install"
	@classmethod
	def decorate_subparser(cls, subparser):
		subparser.add_argument('programs', type=str, nargs='*')
		subparser.add_argument("-s", "--save", action='store_true')
	@classmethod
	def run(cls, args):
		if not args.programs:
			installed_package_metadatas = python_modules.get_packages(os.path.join(os.getcwd(), "python_modules"))
			installed_package_names = list(map(lambda md: md["name"], installed_package_metadatas))
			dependencies = package_json.get_dependencies()
			install_queue = []
			for dependency in dependencies:
				if not dependency in installed_package_names:
					install_queue.append({
						"name": dependency,
						"version": dependencies[dependency]
					})
			cls.install(install_queue, args.save)
			return
		else:
			install_queue = []
			for program in args.programs:
				if "@" in program:
					split = program.split("@")
					install_queue.append({
						"name": split[0],
						"version": split[1]
					})
				else:
					install_queue.append({
						"name": program,
						"version": ""
					})
			cls.install(install_queue, args.save)
	@classmethod
	def install(cls, packages, save):
		def package_json_if_save(save, package_name, version_markup):
			if save:
				package_json.add_dependency(package_name, version_markup)
		for package in packages:
			if not package["version"]:
				result = cls.install_latest(package["name"])
				if not result:
					continue
				package_json_if_save(save, package["name"], "^"+result)
			else:
				versions = list(map(lambda md: md["version"], pypi_api.get_avaliable_versions(package["name"])))
				if not versions:
					continue
				wanted = wanted_version(package["version"], versions)
				if not wanted:
					print("No suitable version for "+package["name"])
					continue
				result = installer.install(package["name"], wanted)
				package_json_if_save(save, package["name"], package["version"])
	@classmethod
	def install_latest(cls, package):
		avaliable_versions = pypi_api.get_avaliable_versions(package)
		if avaliable_versions == None:
			print("Unable to find package "+package)
			return None
		if len(avaliable_versions) == 0:
			print("Unable to find releases for package "+package)
			return None
		versions = list(map(lambda version: version["version"], avaliable_versions))
		latest_version = sort_versions(versions)[-1:][0]
		installer.install(package, latest_version, True)
		return latest_version

