class Node():
	# Use fields: metadata, children
	def __init__(self, metadata = None):
		self.metadata = metadata
		self.children = []
	def build_tree_level(self, installed_package_metadatas):
		if self.metadata:
			for dependency in self.metadata["dependencies"]:
				for scanning_installed in installed_package_metadatas:
					if scanning_installed["name"] == dependency:
						new_node = Node(scanning_installed)
						self.children.append(new_node)
						scanning_installed["touched"] = True
						new_node.build_tree_level(installed_package_metadatas)
	def __repr__(self, level = 0):
		return_string = ""
		if level != 0:
			if len(self.children) == 0:
				return_string += "─"
			else:
				return_string += "┬"
		if self.metadata:
			return_string += self.metadata["name"]+"@"+self.metadata["version"]+"\n"
		for i, child in enumerate(self.children):
			return_string += "│ "*level
			if i == len(self.children)-1:
				return_string += "└─"
			else:
				return_string += "├─"
			return_string += child.__repr__(level+1)
		return return_string
