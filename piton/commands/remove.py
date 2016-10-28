from ..utils.command import BaseCommand
from ..utils import package_json
from ..utils.info import get_packages, Sources

class Command(BaseCommand):
	name = "remove"
	@classmethod
	def decorate_subparser(cls, subparser):
		subparser.add_argument('programs', type=str, nargs='*')
		subparser.add_argument("-s", "--save", action='store_true')
	@classmethod
	def run(cls, args):
		if not args.programs:
			return
		installed = get_packages((Sources.installed,))
		for p_name in args.programs:
			package = installed.get_by_name(p_name)
			if package:
				removed = package.remove()
			if args.save:
				package_json.remove_dependency(p_name)
