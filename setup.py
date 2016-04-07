from distutils.core import setup
setup(
	name = 'python_package_manager',
	license='LICENSE',
	packages = ['python_package_manager', 'python_package_manager/utils'], # this must be the same as the name above
	version = '0.0.3',
	description = 'A local python package manager',
	author = 'Looklikeapro',
	url = 'https://github.com/lookLikeAPro/ppm', # use the URL to the github repo
	keywords = ['package', 'manager', 'local'], # arbitrary keywords
	classifiers = [
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
	],
	entry_points = {
		'console_scripts': [
			'ppm = python_package_manager.main:main'
		]
	}
)
