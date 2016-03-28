import utils.semver
import functools

semver = utils.semver

def get_major_version(version):
	return int(version.split(".")[0])

def get_minor_version(version):
	return int(version.split(".")[1])

def strip_version(version):
	if version[0]=="~" or version[0]=="^":
		return version[1:]
	return version

def sort_versions(versions):
	def compare(version1, version2):
		return semver.compare(version1, version2)
	return sorted(versions, key=functools.cmp_to_key(compare))

def filter_versions(version, available_versions):
	return list(filter(lambda available_version: semver.match(available_version, version), available_versions))

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

# test = [
# 	"1.0.0",
# 	"1.0.1",
# 	"1.0.2",
# 	"0.0.1",
# 	"0.0.3",
# 	"1.2.4",
# 	"1.1.3"
# ]

# print(wanted_version("~1.1.0", test))

