__all__ = ["Sources", "get_packages"]
import os
from .package_json import get_dependencies
from .python_modules import get_packages as p_get_packages
from ..package import Packages

class Sources:
	required = 1
	installed = 2

def get_packages(sources):
	to_merge = []
	if Sources.required in sources:
		to_merge.append(get_dependencies())
	if Sources.installed in sources:
		to_merge.append(p_get_packages(os.path.join(os.getcwd(), "python_modules")))
	if len(to_merge) == 1:
		return to_merge[0]
	else:
		merged = Packages()
		for stream in to_merge:
			for item in stream:
				if merged.get_by_name(item.name):
					merged.get_by_name(item.name).merge(item)
				else:
					merged.append(item)
		return merged
