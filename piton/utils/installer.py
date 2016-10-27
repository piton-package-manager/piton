import os
import pip
import shutil
from . import sneak_config, python_modules

def install(package, version=None, upgrade=False):
	sneak_config.sneak_config_setup()
	if version:
		install_item = package+"=="+version
	else:
		install_item = package
	print(install_item)
	command = ['install', install_item, "--upgrade", "--target="+os.path.join(os.getcwd(), "python_modules")]
	if upgrade:
		command.append("--upgrade")
	pip.main(command)
	sneak_config.sneak_config_remove()

def remove(package):
	metadata = python_modules.get_package(os.path.join(os.getcwd(), "python_modules"), package)
	if not metadata:
		return False
	pending_removals = []
	pending_removals += metadata.top_level_packs
	pending_removals.append(metadata.dist_info)
	for pending_removal in pending_removals:
		try:
			path = os.path.join("python_modules", pending_removal)
			if os.path.isdir(path):
				shutil.rmtree(os.path.join("python_modules", pending_removal))
		except:
			raise("cannot remove")
	return True
