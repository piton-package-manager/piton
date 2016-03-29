import os

distutil_path = os.path.join(os.path.expanduser('~'), '.pydistutils.cfg')
distutil_path_temp = os.path.join(os.path.expanduser('~'), '.pydistutils.cfg.tmp')

def sneak_config_setup():
	if os.path.isfile(distutil_path):
		os.rename(distutil_path, distutil_path_temp)
	distutil_file = open(distutil_path, 'w')
	distutil_file.write('[install]\nprefix=\n')
	distutil_file.close()

def sneak_config_remove():
	os.remove(distutil_path)
	if os.path.isfile(distutil_path_temp):
		os.rename(distutil_path_temp, distutil_path)
