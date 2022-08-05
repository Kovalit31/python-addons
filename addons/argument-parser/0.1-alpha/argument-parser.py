import sys

def return_default_list():
    return [[["help"], {"help": {"require": False,"help": "Help for {0}","shorts": ["h", "?"],"longs": ["help"],"default": True,"need_arg": False}}],[],[],"Usage: {0} ...\nFor help, run {0} -?"]

def _help():
    pass

def _std():
    pass

def _one():
    pass

def _two():
    pass

def _arg():
    pass

def _opt():
    pass

def _flag():
    pass

def _parse(parse_info: list):
    args = sys.argv[1:]
    _opts = []
    _flags = []
    _args = []
    for x in range(len(args)):
        for y in range(len(parse_info)):
            pass

