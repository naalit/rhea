# C (or possibly C++) code generation for Rhea

import helper
import ast
import parser

c = helper.CFile('tmp.c')
repl = False
path = ''

def line(number, source_file):
	c.line(number, source_file)

def gen_init(is_repl):
	global c
	global repl
	repl = is_repl
	c = helper.CFile('tmp.c')
	if repl:
		c['#include "' + path + '/repl.h"']
	c['#include "' + path + '/runtime.h"']

def gen_assign(name, value):
	c(name + ' = ')
	value.eval()

def mangle(name):
	if(name[0] == '$'):
		return name[1:]
	fun_name = name.replace('.', '$p')
	fun_name = fun_name.replace('*', '$m')
	fun_name = fun_name.replace('/', '$d')
	fun_name = fun_name.replace('+', '$a')
	fun_name = fun_name.replace('-', '$s')
#	fun_name = fun_name.replace('*', '$t')
	return fun_name

def gen_lookup(name):
	c(name)

def gen_define(name, value, val = False):
	if isinstance(value, ast.Function):
		fun_name = mangle(name)
		c[str(value.return_type) + ' ' + fun_name + ' (' + str(value.arguments) + ') ']
		value.eval()
	else:
		if val:
			c('const ')
		c(str(value.type) + ' ' + name + ' = ')
		value.eval()

def gen_literal(value):
	c(value)

def gen_actor(body):
	gen_define('$z' + str(parser.anon_actor_num), ast.Function(ast.Args([]), body, ret = 'void'), True)

def gen_block(body):
	with c.block(''):
		for i in body:
			i.eval()
			gen_end()

def gen_send(subject, name, arguments):
	nsubject = subject
	instance = False
	isubject = None
	if not (subject[0].isupper() or subject[0] == '$'):
		if(parser.isnumber(nsubject)):
			try:
				int(subject)
				isubject = ast.LiteralInt(subject)
				nsubject = 'Int'
			except:
				nsubject = 'Float'
				isubject = ast.LiteralFloat(subject)
		else:
			nsubject = parser.index[nsubject].type
			isubject = subject
		instance = True
	fn_name = ''
	for i in arguments:
		fn_name += i.type + '$_'
	if(subject[0] == '$'):
		fn_name += mangle(nsubject) + mangle(name)
	elif instance:
		fn_name += mangle(nsubject) + '$i' + mangle(name)
	else:
		fn_name += mangle(nsubject) + '$x' + mangle(name)
	c(fn_name + ' (')
	if not instance:
		try:
			arguments[0].eval()
		except:
			pass
		for i in arguments[1:]:
			c(', ')
			i.eval()
	else:
		c(subject)#isubject.eval()
		for i in arguments:
			c(', ')
			i.eval()
	c(')')
def gen_end():
	c[';']

def gen_close():
	c.close()
