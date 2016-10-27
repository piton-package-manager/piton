import os
from ..utils.command import BaseCommand
from ..utils import python_modules, package_json

class Node():
	# Use fields: metadata, children
	def __init__(self, metadata = None):
		self.metadata = metadata
		self.children = []
	def build_tree_level(self, installed_package_metadatas):
		if self.metadata:
			for dependency in self.metadata.dependencies:
				for scanning_installed in installed_package_metadatas:
					if scanning_installed.name == dependency:
						new_node = Node(scanning_installed)
						self.children.append(new_node)
						scanning_installed.needed = True
						new_node.build_tree_level(installed_package_metadatas)
	def __repr__(self, level = 0):
		return_string = ""
		if level != 0:
			if len(self.children) == 0:
				return_string += "─"
			else:
				return_string += "┬"
		if self.metadata:
			return_string += self.metadata.name+"@"+self.metadata.version+"\n"
		for i, child in enumerate(self.children):
			return_string += "│ "*level
			if i == len(self.children)-1:
				return_string += "└─"
			else:
				return_string += "├─"
			return_string += child.__repr__(level+1)
		return return_string

class Command(BaseCommand):
	name = "list"
	@classmethod
	def run(cls, args):
		cls._run()
	@staticmethod
	def _run():
		print(os.getcwd())
		installed_packages = python_modules.get_packages(os.path.join(os.getcwd(), "python_modules"))
		dependencies = package_json.get_dependencies()
		tree = Node()
		unwanted = []
		for package in installed_packages:
			package.needed = False
			if dependencies.get_by_name(package.name):
				tree.children.append(Node(package))
				package.needed = True
		for node in tree.children:
			node.build_tree_level(installed_packages)
		for package in installed_packages:
			if package.needed == False:
				unwanted.append(package)
		print(tree)
		if len(unwanted) > 0:
			print("Unwanted:")
			print(list(map(lambda p: p.name, unwanted)))
