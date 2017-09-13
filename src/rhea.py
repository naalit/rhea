#!/bin/python
# Rhea dispatcher, sort of

import sys
import parser
import ast
import codegen
from subprocess import call
import os

codegen.path = os.path.dirname(os.path.realpath(__file__))

verbose = False
run = True
args = sys.argv[1:]
parserizer = parser.Parser()
try:
	if(args[0] == '-v'):
		verbose = True
		args = args[1:]
	if(args[0] == '--version'):
		print('Rhea version 0.0.0.0.0.1 alpha')
		sys.exit(0)
	if(args[0] == 'build'):
		run = False
		args = args[1:]
	if(args[0] == 'run'):
		args = args[1:]
except IndexError:
	print('Welcome to the Rhea REPL!')
	print r'''____/\\\\\\\\\______/\\\________/\\\__/\\\\\\\\\\\\\\\_____/\\\\\\\\\____
 __/\\\///////\\\___\/\\\_______\/\\\_\/\\\///////////____/\\\\\\\\\\\\\__
  _\/\\\_____\/\\\___\/\\\_______\/\\\_\/\\\______________/\\\/////////\\\_
   _\/\\\\\\\\\\\/____\/\\\\\\\\\\\\\\\_\/\\\\\\\\\\\_____\/\\\_______\/\\\_
    _\/\\\//////\\\____\/\\\/////////\\\_\/\\\///////______\/\\\\\\\\\\\\\\\_
     _\/\\\____\//\\\___\/\\\_______\/\\\_\/\\\_____________\/\\\/////////\\\_
      _\/\\\_____\//\\\__\/\\\_______\/\\\_\/\\\_____________\/\\\_______\/\\\_
       _\/\\\______\//\\\_\/\\\_______\/\\\_\/\\\\\\\\\\\\\\\_\/\\\_______\/\\\_
        _\///________\///__\///________\///__\///////////////__\///________\///__
        '''
	tree = ast.Initialization(True, '$main', ast.Function(ast.Args([]), [], ret='int'))
	while True:
		sys.stdout.write('rhea> ')
		line = sys.stdin.readline()
		if line == '':
			print('\nGoodbye!')
			sys.exit(0)
		line = line[:-1] + ' \n'
		parserizer.loc = 0
		parserizer.source = line
		tmptree = parserizer.parse_expr()
		old = tree.value.get_last()
		if isinstance(old, ast.Send):
			if isinstance(old.args[0], ast.IntLiteral) or isinstance(old.args[0], ast.FloatLiteral) or isinstance(old.args[0], ast.Lookup):
				tree.value.remove_last()
			else:
				tree.value.set_last(old.args[0])
		if isinstance(tmptree, ast.Initialization):
			tree.value.append(tmptree)
		elif tmptree is None:
			continue
		else:
			if tmptree.type == 'void':
				tree.value.append(tmptree)
			else:
				tree.value.append(ast.Send('System', 'print', [tmptree]))
		codegen.gen_init(False)
		tree.eval()
		codegen.gen_close()
		error_code = call(['clang', '-o', 'result', 'tmp.c'])
		if error_code != 0:
			raise RuntimeError("C compilation finished with error code")
		#call(['rm', 'tmp.c'])
		call(['./result'])

source = ''
for infile in args:
	source += open(infile, 'r').read()

if verbose:
	print('Rhea source:')
	print(source)
	print('Parsing...')
tree = parserizer.parse(source)
if verbose:
	print('Running codegen...')
tree.eval()

if verbose:
	print('\nGenerated C code:')
	print(open('tmp.c', 'r').read())

call(['clang', '-o', 'result', 'tmp.c'])
#call(['rm', 'tmp.c'])

if run:
	call(['./result'])
