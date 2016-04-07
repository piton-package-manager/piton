import os
import json
import sys
import argparse
from .utils.pypi_api import get_avaliable_versions
from .utils.version import wanted_version, sort_versions
from .utils import sneak_config, package_json
import pip
from .node import Node

def get_package_info(directory, package):
	def interpret_dependencies(messy_requirements):
		dependencies = []
		for messy_requirement in messy_requirements:
			for wtf in messy_requirement.get("requires", []):
				wtf = wtf.split(" ")[0]
				dependencies.append(wtf.lower())		
		return dependencies
	top_level_packs = []
	with open(os.path.join(directory, package, "top_level.txt"),'r') as top_level:
		for line in top_level:
			top_level_packs.append(line.strip())
	with open(os.path.join(directory, package, "metadata.json"),'r') as metadata_file:
		metadata = json.load(metadata_file)
		version = metadata.get("version", "")
		name = metadata.get("name", "").lower()
		dependencies = interpret_dependencies(metadata.get("run_requires", []))
	return {
		"dist_info": package,
		"top_level": top_level_packs,
		"dependencies": dependencies,
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
	packages = get_packages(os.path.join(os.getcwd(), "python_modules"))
	possible_package = list(filter(lambda p: p["name"] == package, packages))
	if len(possible_package) == 0:
		return None
	return possible_package[-1:][0]

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
		packages = get_packages(os.path.join(os.getcwd(), "python_modules"))
		dependencies = package_json.get_dependencies()
		if len(dependencies) == 0:
			return
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
		cls.display_outdated(package_metadatas)
	@staticmethod
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

class CommandRemove():
	name = "remove"
	@staticmethod
	def decorate_subparser(subparser):
		subparser.add_argument('program', type=str, nargs='?')
		subparser.add_argument("-s", "--save", action='store_true')
	@classmethod
	def run(cls, args):
		cls._run(args.program, args.save)
	@staticmethod
	def _run(package, save):
		def package_json_if_save(save):
			if save:
				dependencies = package_json.get_dependencies()
				dependencies.pop(package, None)
				package_json.write_dependencies(dependencies)
		import shutil
		metadata = get_package(os.path.join(os.getcwd(), "python_modules"), package)
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
	@classmethod
	def execute(cls, package):
		# Code interface
		cls._run(package, False)

class CommandInstall():
	name = "install"
	@staticmethod
	def decorate_subparser(subparser):
		subparser.add_argument('program', type=str, nargs='?')
		subparser.add_argument("-s", "--save", action='store_true')
	@classmethod
	def run(cls, args):
		cls._run(args.program, args.save)
	@classmethod
	def _run(cls, package, save):
		def package_json_if_save(save, version_markup):
			if save:
				dependencies = package_json.get_dependencies()
				dependencies[package] = version_markup
				package_json.write_dependencies(dependencies)
		if not package:
			installed_package_metadatas = get_packages(os.path.join(os.getcwd(), "python_modules"))
			installed_package_names = list(map(lambda md: md["name"], installed_package_metadatas))
			dependencies = package_json.get_dependencies()
			install_queue = []
			for dependency in dependencies:
				if not dependency in installed_package_names:
					install_queue.append({
						"name": dependency,
						"version": dependencies[dependency]
					})
			for item in install_queue:
				versions = list(map(lambda md: md["version"], get_avaliable_versions(item["name"])))
				wanted = wanted_version(item["version"], versions)
				cls.perform_install(item["name"], wanted)
		else:
			latest_version = cls.install_latest(package)
			if not latest_version:
				return
			package_json_if_save(save, "^"+latest_version)
	@staticmethod
	def perform_install(package, version=None, upgrade=False):
		sneak_config.sneak_config_setup()
		if version:
			install_item = package+"=="+version
		else:
			install_item = package
		print(install_item)
		command = ['install', install_item, "--target="+os.path.join(os.getcwd(), "python_modules")]
		if upgrade:
			command.append("--upgrade")
		pip.main(command)
		sneak_config.sneak_config_remove()
	@classmethod
	def install_latest(cls, package):
		avaliable_versions = get_avaliable_versions(package)
		if avaliable_versions == None:
			print("Unable to find package "+package)
			return None
		versions = list(map(lambda version: version["version"], avaliable_versions))
		latest_version = sort_versions(versions)[-1:][0]
		cls.perform_install(package, latest_version, true)
		return latest_version

class CommandList():
	name = "list"
	@staticmethod
	def decorate_subparser(subparser):
		pass
	@classmethod
	def run(cls, args):
		cls._run()
	@staticmethod
	def _run():
		print(os.getcwd())
		installed_package_metadatas = get_packages(os.path.join(os.getcwd(), "python_modules"))
		dependencies = package_json.get_dependencies()
		tree = Node()
		unwanted = []
		for metadata in installed_package_metadatas:
			if metadata["name"] in dependencies:
				tree.children.append(Node(metadata))
				metadata["touched"] = True
		for node in tree.children:
			node.build_tree_level(installed_package_metadatas)
		for metadata in installed_package_metadatas:
			if metadata.get("touched", False) == False:
				unwanted.append(metadata)
		print(tree)
		if len(unwanted) > 0:
			print("Unwanted:")
			print(list(map(lambda a: a["name"], unwanted)))

class CommandPrune():
	name = "prune"
	@staticmethod
	def decorate_subparser(subparser):
		pass
	@classmethod
	def run(cls, args):
		cls._run()
	@staticmethod
	def _run():
		installed_package_metadatas = get_packages(os.path.join(os.getcwd(), "python_modules"))
		dependencies = package_json.get_dependencies()
		tree = Node()
		unwanted = []
		for metadata in installed_package_metadatas:
			if metadata["name"] in dependencies:
				tree.children.append(Node(metadata))
				metadata["touched"] = True
		for node in tree.children:
			node.build_tree_level(installed_package_metadatas)
		for metadata in installed_package_metadatas:
			if metadata.get("touched", False) == False:
				unwanted.append(metadata)
		for metadata in unwanted:
			CommandRemove.execute(metadata["name"])

class CommandInit():
	name = "init"
	@staticmethod
	def decorate_subparser(subparser):
		pass
	@classmethod
	def run(cls, args):
		cls._run()
	@staticmethod
	def _run():
		package_file_path = os.path.join(os.getcwd(), 'package.json')
		if os.path.isfile(package_file_path):
			print("package.json already exists")
			return
		with open(package_file_path, 'w') as outfile:
			file_content = {
				"pythonDevDependencies": {},
				"pythonDependencies": {}
			}
			json.dump(file_content, outfile, indent=2)

def main():
	subcommands = [
		CommandOutdated,
		CommandInstall,
		CommandRemove,
		CommandList,
		CommandPrune,
		CommandInit
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

