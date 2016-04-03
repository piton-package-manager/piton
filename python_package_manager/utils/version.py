import python_package_manager.utils.semver
import functools
import re

semver = python_package_manager.utils.semver

def get_major_version(version):
	return int(version.split(".")[0])

def get_minor_version(version):
	return int(version.split(".")[1])

def strip_version(version):
	if version[0]=="~" or version[0]=="^":
		return version[1:]
	return version

def cheat_semver(version):
	# Need to change 0.1 to 0.1.0 to appease semver
	if version.count(".") == 1:
		version = version+".0"
	# Stupid python versioning has "1.9rc2.0"
	if re.search('[a-zA-Z]', version.split(".")[1]):
		split = version.split(".")
		version = split[0]+"."+re.compile('[a-zA-Z]').split(split[1])[0]+"."+split[2]
	return version

def sort_versions(versions):
	def compare(version1, version2):
		return semver.compare(cheat_semver(version1), cheat_semver(version2))
	return sorted(versions, key=functools.cmp_to_key(compare))

def filter_versions(version, available_versions):
	return list(filter(lambda available_version: semver.match(cheat_semver(available_version), cheat_semver(version)), available_versions))

def wanted_version(version, available_versions):
	version_without_symbol = strip_version(version)
	if version[0] == "^":
		available_versions = list(filter(lambda available_version: get_major_version(available_version)==get_major_version(version_without_symbol), available_versions))
		semver_to_match = ">=" + version_without_symbol
	elif version[0] == "~":
		available_versions = list(filter(lambda available_version: get_major_version(available_version)==get_major_version(version_without_symbol), available_versions))
		available_versions = list(filter(lambda available_version: get_minor_version(available_version)==get_minor_version(version_without_symbol), available_versions))
		semver_to_match = ">=" + version_without_symbol
	else:
		semver_to_match = version_without_symbol
	valid_versions = filter_versions(semver_to_match, available_versions)
	if len(valid_versions) == 0:
		return None
	else:
		return sort_versions(valid_versions)[-1:][0]
