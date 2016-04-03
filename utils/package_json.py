import os
import json

def get_dependencies():
	package_file_path = os.path.join(os.getcwd(), 'package.json')
	with open(package_file_path, 'r') as infile:
		package_dict = json.load(infile)
		dependencies = package_dict.get("pythonDependencies", [])
		dependencies_dev = package_dict.get("pythonDevDependencies", [])
	return dependencies

def write_dependencies(dependencies):
	package_file_path = os.path.join(os.getcwd(), 'package.json')
	with open(package_file_path, 'r') as infile:
		package_dict = json.load(infile)
		package_dict["pythonDependencies"] = dependencies
	with open(package_file_path, 'w') as outfile:
		json.dump(package_dict, outfile, indent=2)
