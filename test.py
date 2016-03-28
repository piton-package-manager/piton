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


