import os
import sys
import argparse

command_names = [
	"init",
	"install",
	"list",
	"outdated",
	"path",
	"prune",
	"remove",
	"run",
	"update",
]

def import_command(command_name):
	from importlib import import_module
	try:
		module = import_module('.commands.'+command_name, __package__)
		return module.Command
	except:
		return None

def main():
	parser = argparse.ArgumentParser(description=("Python Package Manager"))
	if len(sys.argv) == 1:
		pass
	elif not sys.argv[1] in command_names:
		pass
	else:
		command = import_command(sys.argv[1])
		subparsers = parser.add_subparsers(dest='subcommand')
		subparser = subparsers.add_parser(command.name)
		command.decorate_subparser(subparser)
		args = parser.parse_args()
		command.run(args)

if __name__ == '__main__':
	sys.exit(main())

