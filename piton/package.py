__all__ = ["Package"]

def version_xor(v1, v2):
	if v1 != "" and v2 != "":
		raise("package info conflict")
	return v1 or v2

class Package():
	name = ""
	version = ""
	wanted_version = ""
	latest_version = ""
	avaliable_versions = []
	installed = False
	dependencies = []
	top_level_packs = []
	dist_info = ""
	def __init__(self, **kwargs):
		if "name" in kwargs:
			self.name = kwargs["name"]
		if "version" in kwargs:
			self.version = kwargs["version"]
		if "wanted_version" in kwargs:
			self.wanted_version = kwargs["wanted_version"]
		if "installed" in kwargs:
			self.installed = kwargs["installed"]
	def merge(self, other):
		self.version = version_xor(self.version, other.version)
		self.wanted_version = version_xor(self.wanted_version, other.wanted_version)
		self.installed = self.installed or other.installed
		self.dependencies = self.dependencies or other.dependencies
		self.top_level_packs = self.top_level_packs or other.top_level_packs
		self.dist_info = self.dist_info or other.dist_info
