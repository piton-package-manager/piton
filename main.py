import os
import json
from utils.pypi_api import get_avaliable_versions
from utils.version import wanted_version, sort_versions

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

def get_dependencies():
	with open(os.path.join('package.json'), 'r') as f:
		package_dict = json.load(f)
		dependencies = package_dict.get("pythonDependencies", [])
		dependencies_dev = package_dict.get("pythonDevDependencies", [])
	return dependencies

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

def command_outdated():
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

command_outdated()

