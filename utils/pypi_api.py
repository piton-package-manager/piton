try:
	# For Python 3.0 and later
	from urllib.request import urlopen
except ImportError:
	# Fall back to Python 2's urllib2
	from urllib2 import urlopen

import json

def get_avaliable_versions(package):
	try:
		with urlopen("https://pypi.python.org/pypi/"+package+"/json") as response:
			result = json.loads(response.read().decode('utf-8'))
			versions = []
			for release, data in result["releases"].items():
				if len(data) > 0:
					info = data[-1:][0]
					info["version"] = release
					versions.append(info)
			return versions
	except:
		return None
