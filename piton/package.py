__all__ = ["Package", "Packages"]
from .utils import pypi_api
from .utils.version import wanted_version, sort_versions
from .utils.exception import OperationException

def version_xor(v1, v2):
	if v1 != "" and v2 != "":
		raise("package info conflict")
	return v1 or v2

class Package():
	name = ""
	version = ""
	wanted_version = ""
	wanted_rule = ""
	latest_version = ""
	avaliable_versions = []
	installed = False
	dependencies = []
	top_level_packs = []
	dist_info = ""
	def __init__(self, **kwargs):
		self.name = kwargs.get("name", "")
		self.version = kwargs.get("version", "")
		self.wanted_version = kwargs.get("wanted_version", "")
		self.wanted_rule = kwargs.get("wanted_rule", "")
		self.installed = kwargs.get("installed", False)
		self.top_level_packs = kwargs.get("top_level_packs", [])
		self.avaliable_versions = kwargs.get("avaliable_versions", [])
	def __repr__(self):
		return '\n'.join([
			"---------------------------",
			"name: {}".format(self.name),
			"version: {}".format(self.version),
			"wanted_version: {}".format(self.wanted_version),
			"installed: {}".format(self.installed)
		])
	def merge(self, other):
		self.version = version_xor(self.version, other.version)
		self.wanted_version = version_xor(self.wanted_version, other.wanted_version)
		self.wanted_rule = version_xor(self.wanted_rule, other.wanted_rule)
		self.installed = self.installed or other.installed
		self.dependencies = self.dependencies or other.dependencies
		self.top_level_packs = self.top_level_packs or other.top_level_packs
		self.dist_info = self.dist_info or other.dist_info
	def get_wanted_version(self):
		versions_metadata = pypi_api.get_avaliable_versions(self.name)
		self.avaliable_versions = list(map(lambda version: version["version"], versions_metadata))
		self.latest_version = sort_versions(self.avaliable_versions)[-1:][0]
		if len(self.avaliable_versions):
			self.wanted_version = wanted_version(self.wanted_rule, self.avaliable_versions)
	def install(self):
		from .utils import installer
		if not self.name or not self.wanted_version:
			raise OperationException
		return installer.install(self.name, self.wanted_version)
	def remove(self):
		from .utils import installer
		return installer.remove(self.name)

class Packages(list):
	def get_by_name(self, package_name):
		for package in self:
			if package.name == package_name:
				return package
		return None
