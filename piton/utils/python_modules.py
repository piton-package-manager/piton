import os
import json
from ..package import Package, Packages

def get_package_info(directory, package_name):
	def interpret_dependencies(messy_requirements):
		dependencies = []
		for messy_requirement in messy_requirements:
			for wtf in messy_requirement.get("requires", []):
				wtf = wtf.split(" ")[0]
				dependencies.append(wtf.lower())
		return dependencies
	package = Package(installed=True)
	package.dist_info = package_name
	with open(os.path.join(directory, package_name, "top_level.txt"),'r') as top_level:
		for line in top_level:
			if line.strip():
				package.top_level_packs.append(line.strip())
	with open(os.path.join(directory, package_name, "metadata.json"),'r') as metadata_file:
		metadata = json.load(metadata_file)
		package.version = metadata.get("version", "")
		package.name = metadata["name"].lower()
		package.dependencies = interpret_dependencies(metadata.get("run_requires", []))
	return package

def get_packages(directory):
	if not os.path.isdir(directory):
		return Packages()
	packages = Packages()
	for dirname in os.listdir(directory):
		if dirname[-10:] == ".dist-info" and os.path.isdir(os.path.join(directory, dirname)):
			packages.append(get_package_info(directory, dirname))
	return packages

def get_package(directory, package):
	packages = get_packages(os.path.join(os.getcwd(), "python_modules"))
	possible_package = list(filter(lambda p: p.name == package, packages))
	if len(possible_package) == 0:
		return None
	return possible_package[-1:][0]

def get_package_metadata(packages, name):
	lookup = list(filter(lambda package: package.name==name, packages))
	if len(lookup) == 0:
		return {
			"name": name,
			"installed": False
		}
	else:
		lookup[0]["installed"] = True
		return lookup[0]
