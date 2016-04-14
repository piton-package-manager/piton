import os
import json
import re
from collections import OrderedDict

def exists(package_file_path = os.path.join(os.getcwd(), 'requirements.txt')):
	return os.path.exists(package_file_path)

def get_dependencies(package_file_path = os.path.join(os.getcwd(), 'requirements.txt')):
	dependencies = OrderedDict()
	try:
		with open(package_file_path, 'r') as infile:
			for line in infile:
				split = re.compile("[>|<|=]=").split(line)
				dependencies[split[0]] = split[1].strip()
	except:
		print("unable to read package.json")
		return {}
	return dependencies

def write_dependencies(package_dict, package_file_path = os.path.join(os.getcwd(), 'requirements.txt')):
	package_dict = OrderedDict(sorted(package_dict.items()))
	try:
		if not os.path.exists(package_file_path):
			open(package_file_path, 'w').close()
		with open(package_file_path, 'r+') as file:
			file.seek(0)
			for package_name, package_version in package_dict.items():
				print(package_name+"=="+package_version)
				if "^" in package_version or "~" in package_version:
					package_version = package_version[1:]
				file.write(package_name+"=="+package_version+"\n")
			file.truncate()
	except:
		print("unable to write requirements.txt")
		return

