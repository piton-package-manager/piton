import os
import json
from collections import OrderedDict
from ..package import Package, Packages

def exists(package_file_path = os.path.join(os.getcwd(), 'package.json')):
	return os.path.exists(package_file_path)

def get_dependencies():
	package_file_path = os.path.join(os.getcwd(), 'package.json')
	try:
		with open(package_file_path, 'r') as infile:
			package_dict = json.load(infile)
			dependencies = package_dict.get("pythonDependencies", {})
			dependencies_dev = package_dict.get("pythonDevDependencies", {})
	except:
		raise("unable to read package.json")
	dependencies.update(dependencies_dev)
	packages = Packages()
	for dependency in dependencies:
		packages.append(Package(name=dependency, wanted_rule=dependencies[dependency]))
	return packages

def remove_dependency(dependency_key):
	package_file_path = os.path.join(os.getcwd(), 'package.json')
	try:
		with open(package_file_path, 'r+') as file:
			package_dict = json.load(file, object_pairs_hook=OrderedDict)
			package_dict["pythonDependencies"].pop(dependency_key, None)
			file.seek(0)
			file.write(json.dumps(package_dict, indent=2))
			file.truncate()
	except:
		raise("unable to write package.json")

def add_dependency(dependency_key, dependency_content):
	package_file_path = os.path.join(os.getcwd(), 'package.json')
	try:
		with open(package_file_path, 'r+') as file:
			package_dict = json.load(file, object_pairs_hook=OrderedDict)
			package_dict["pythonDependencies"][dependency_key] = dependency_content
			file.seek(0)
			file.write(json.dumps(package_dict, indent=2))
			file.truncate()
	except:
		print("unable to write package.json")
		return

def get_scripts():
	package_file_path = os.path.join(os.getcwd(), 'package.json')
	try:
		with open(package_file_path, 'r') as infile:
			package_dict = json.load(infile)
			scripts = package_dict.get("scripts", {})
	except:
		print("unable to read package.json")
		return {}
	return scripts

def get_script(script):
	scripts = get_scripts()
	for script_name, script_content in scripts.items():
		if script_name == script:
			return script_content
	return None
