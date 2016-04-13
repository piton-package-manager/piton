ascii_art = """      (_)_
 ____  _| |_  ___  ____
|  _ \| |  _)/ _ \|  _ \ 
| | | | | |_| |_| | | | |
| ||_/|_|\___)___/|_| |_|
|_|"""

slogan = "Package Management should be simple."

usage = """Usage: piton <command>
"""

future = """
npm <cmd> -h     quick help on <cmd>
npm -l           display full usage info
npm help <term>  search for help on <term>
npm help npm     involved overview
"""

def show_main_help():
	print(ascii_art)
	print(slogan)
	print("")
	print(usage)
