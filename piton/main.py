import os
import sys
import argparse
from .commands import CommandInit, CommandOutdated, CommandList, CommandRemove, CommandInstall, CommandPrune

def main():
	subcommands = [
		CommandOutdated,
		CommandInstall,
		CommandRemove,
		CommandList,
		CommandPrune,
		CommandInit
	]

	parser = argparse.ArgumentParser(description=("Python Package Manager"))
	subparsers = parser.add_subparsers(dest='subcommand')

	for subcommand in subcommands:
		subparser = subparsers.add_parser(subcommand.name)
		subcommand.decorate_subparser(subparser)

	args = parser.parse_args()

	for subcommand in subcommands:
		if args.subcommand == subcommand.name:
			subcommand.run(args)

if __name__ == '__main__':
	sys.exit(main())

