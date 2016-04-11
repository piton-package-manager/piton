import os
from ..utils.command import BaseCommand
from ..utils import python_modules, package_json, installer
from ..node import Node

class Command(BaseCommand):
	name = "prune"
	@classmethod
	def run(cls, args):
		cls._run()
	@staticmethod
	def _run():
		installed_package_metadatas = python_modules.get_packages(os.path.join(os.getcwd(), "python_modules"))
		dependencies = package_json.get_dependencies()
		tree = Node()
		unwanted = []
		for metadata in installed_package_metadatas:
			if metadata["name"] in dependencies:
				tree.children.append(Node(metadata))
				metadata["touched"] = True
		for node in tree.children:
			node.build_tree_level(installed_package_metadatas)
		for metadata in installed_package_metadatas:
			if metadata.get("touched", False) == False:
				unwanted.append(metadata)
		for metadata in unwanted:
			installer.remove(metadata["name"])
