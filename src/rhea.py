#!/bin/python
# Rhea dispatcher, sort of

import sys
import parser
from subprocess import call

verbose = False
run = True
args = sys.argv[1:]
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
	while True:
		sys.stdout.write('rhea> ')
		line = sys.stdin.readline()
		if line == '':
			print('\nGoodbye!')
			sys.exit(0)
		line = line.strip() + ' \n'
		tree = parser.parse(line)
		tree.eval(True)
		call(['clang', '-o', 'result', 'tmp.c'])
		#call(['rm', 'tmp.c'])
		call(['./result'])

source = ''
for infile in args:
	source += open(infile, 'r').read()
	
if verbose:
	print('Rhea source:')
	print(source)
	print('Parsing...')
tree = parser.parse(source)
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
