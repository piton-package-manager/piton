import json
import os
import pip

distutil_path = os.path.join(os.path.expanduser('~'), '.pydistutils.cfg')
distutil_path_temp = os.path.join(os.path.expanduser('~'), '.pydistutils.cfg.tmp')

def sneak_config_setup():
	if os.path.isfile(distutil_path):
		os.rename(distutil_path, distutil_path_temp)
	distutil_file = open(distutil_path, 'w')
	distutil_file.write('[install]\nprefix=\n')
	distutil_file.close()

def sneak_config_remove():
	os.remove(distutil_path)
	if os.path.isfile(distutil_path_temp):
		os.rename(distutil_path_temp, distutil_path)

def install(package):
	pip.main(['install', package, "--target=python_modules", "--install-option='--prefix='"])

def run():
	sneak_config_setup()
	with open(os.path.join('package.json'), 'r') as f:
		package_dict = json.load(f)
		dependencies = package_dict.get("pythonDependencies", [])
		dependencies_dev = package_dict.get("pythonDevDependencies", [])
		print(dependencies)
		print(dependencies_dev)
	
	
	sneak_config_remove()
		
run()


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
			print()
			packages.append(get_package_info(directory, dirname))
	return packages


print(get_packages("python_modules"))




