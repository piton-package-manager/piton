
def setup_path():
	import sys
	import os
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sys.path.append(os.path.join(BASE_DIR, "python_modules"))

setup_path()
