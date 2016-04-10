import os
import json

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
	try:
		for dirname in os.listdir(directory):
			if dirname[-10:] == ".dist-info" and os.path.isdir(os.path.join(directory, dirname)):
				packages.append(get_package_info(directory, dirname))
	except:
		packages = []
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
