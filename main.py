import os
import json
import sys
import argparse
from utils.pypi_api import get_avaliable_versions
from utils.version import wanted_version, sort_versions
from utils import sneak_config
import pip

def get_package_info(directory, package):
	top_level_packs = []
	with open(os.path.join(directory, package, "top_level.txt"),'r') as top_level:
		for line in top_level:
			top_level_packs.append(line.strip())
	with open(os.path.join(directory, package, "metadata.json"),'r') as metadata_file:
		metadata = json.load(metadata_file)
		version = metadata.get("version", "")
		name = metadata.get("name", "")
	return {
		"dist_info": package,
		"top_level": top_level_packs,
		"version": version,
		"name": name
	}

def get_packages(directory):
	packages = []
	for dirname in os.listdir(directory):
		if dirname[-10:] == ".dist-info" and os.path.isdir(os.path.join(directory, dirname)):
			packages.append(get_package_info(directory, dirname))
	return packages

def get_package(directory, package):
	packages = get_packages("python_modules")
	possible_package = list(filter(lambda p: p["name"] == package, packages))
	if len(possible_package) == 0:
		return None
	return possible_package[-1:][0]

def get_dependencies():
	with open(os.path.join('package.json'), 'r') as infile:
		package_dict = json.load(infile)
		dependencies = package_dict.get("pythonDependencies", [])
		dependencies_dev = package_dict.get("pythonDevDependencies", [])
	return dependencies

def write_dependencies(dependencies):
	with open(os.path.join('package.json'), 'r') as infile:
		package_dict = json.load(infile)
		package_dict["pythonDependencies"] = dependencies
	with open(os.path.join('package.json'), 'w') as outfile:
		json.dump(package_dict, outfile, indent=2)

def display_outdated(metadatas):
	headings = ["current", "wanted", "latest"]
	packages_list = list(map(lambda metadata: metadata["name"], metadatas))
	data = []
	for metadata in metadatas:
		if "version" in metadata:
			current_version = metadata["version"]
		else:
			current_version = "n/a"
		data.append([current_version, metadata["wanted_version"], metadata["latest"]])

	row_format ="{:>15}" * (len(headings) + 1)
	print(row_format.format("", *headings))
	for package, row in zip(packages_list, data):
		print(row_format.format(package, *row))

def get_package_metadata(packages, name):
	lookup = list(filter(lambda package: package["name"]==name, packages))
	if len(lookup) == 0:
		return {
			"name": name,
			"installed": False
		}
	else:
		lookup[0]["installed"] = True
		return lookup[0]

class command_outdated():
	name = "outdated"
	def decorate_subparser(self, subparser):
		pass
	def run(self, args):
		self._run()
	def _run(self):
		packages = get_packages("python_modules")
		dependencies = get_dependencies()
		package_metadatas = []

		for dependency, version in dependencies.items():
			package_metadata = get_package_metadata(packages, dependency)
			package_metadata["version_markup"] = version
			versions_metadata = get_avaliable_versions(dependency)
			# package_metadata["avaliable_versions_metadata"] = versions_metadata
			package_metadata["avaliable_versions"] = list(map(lambda version: version["version"], versions_metadata))
			package_metadata["latest"] = sort_versions(package_metadata["avaliable_versions"])[-1:][0]
			package_metadata["wanted_version"] = wanted_version(version, package_metadata["avaliable_versions"])
			package_metadatas.append(package_metadata)

		display_outdated(package_metadatas)

def perform_install(package, version=None):
	sneak_config.sneak_config_setup()
	if version:
		install_item = package+"=="+version
	else:
		install_item = package
	print(install_item)
	pip.main(['install', install_item, "--target=python_modules"])
	sneak_config.sneak_config_remove()

def install_latest(package):
	avaliable_versions = get_avaliable_versions(package)
	if avaliable_versions == None:
		print("Unable to find package "+package)
		return None
	versions = list(map(lambda version: version["version"], avaliable_versions))
	latest_version = sort_versions(versions)[-1:][0]
	perform_install(package, latest_version)
	return latest_version

class command_remove():
	name = "remove"
	def decorate_subparser(self, subparser):
		subparser.add_argument('program', type=str, nargs='?')
		subparser.add_argument("-s", "--save", action='store_true')
	def run(self, args):
		self._run(args.program, args.save)
	def _run(self, package, save):
		def package_json_if_save(save):
			if save:
				dependencies = get_dependencies()
				dependencies.pop(package, None)
				write_dependencies(dependencies)
		import shutil
		metadata = get_package("python_modules", package)
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

class command_install():
	name = "install"
	def decorate_subparser(self, subparser):
		subparser.add_argument('program', type=str, nargs='?')
		subparser.add_argument("-s", "--save", action='store_true')
	def run(self, args):
		self._run(args.program, args.save)
	def _run(self, package, save):
		def package_json_if_save(save, version_markup):
			if save:
				dependencies = get_dependencies()
				dependencies[package] = version_markup
				write_dependencies(dependencies)
		if not package:
			print(get_dependencies())
		else:
			dependencies = get_dependencies()
			if package in dependencies:
				print("package "+package+" is already a dependency")
				return
			latest_version = install_latest(package)
			if not latest_version:
				return
			package_json_if_save(save, "^"+latest_version)

def main():
	subcommands = [
		command_outdated(),
		command_install(),
		command_remove()
	]

	parser = argparse.ArgumentParser(description=("Python Package Manager"))
	subparsers = parser.add_subparsers(dest='subcommand')

	for subcommand in subcommands:
		subparser = subparsers.add_parser(subcommand.name)
		subcommand.decorate_subparser(subparser)

	args = parser.parse_args()

	for subcommand in subcommands:
		if args.subcommand == subcommand.name:
			subcommand.run(args)

if __name__ == '__main__':
	sys.exit(main())

