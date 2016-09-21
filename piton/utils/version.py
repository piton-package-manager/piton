import functools
from pkg_resources import parse_version

def get_major_version(version):
	return int(version.split(".")[0])

def get_minor_version(version):
	return int(version.split(".")[1])

def strip_version(version):
	if not version:
		return version
	if version[0]=="~" or version[0]=="^":
		return version[1:]
	return version

def sort_versions(versions):
	return sorted(versions, key=lambda version: parse_version(version))

def filter_versions(version, available_versions):
	def compare(version1, version2):
		return parse_version(version1) <= parse_version(version2)
	return list(filter(lambda available_version: compare(version, available_version), available_versions))

def find_exact_version(version, available_versions):
	return list(filter(lambda available_version: parse_version(version) == parse_version(available_version), available_versions))

def wanted_version(version, available_versions):
	version_without_symbol = strip_version(version)
	if not version:
		return sort_versions(available_versions)[-1:][0]
	if version[0] == "^":
		available_versions = list(filter(lambda available_version: get_major_version(available_version)==get_major_version(version_without_symbol), available_versions))
		valid_versions = filter_versions(version_without_symbol, available_versions)
	elif version[0] == "~":
		available_versions = list(filter(lambda available_version: get_major_version(available_version)==get_major_version(version_without_symbol), available_versions))
		available_versions = list(filter(lambda available_version: get_minor_version(available_version)==get_minor_version(version_without_symbol), available_versions))
		valid_versions = filter_versions(version_without_symbol, available_versions)
	else:
		semver_to_match = version_without_symbol
		valid_versions = find_exact_version(version_without_symbol, available_versions)
	if len(valid_versions) == 0:
		return None
	else:
		return sort_versions(valid_versions)[-1:][0]
