# Parser for Rhea

import ast
import re

loc = 0
index = {}
vals = {}
rets = {'System print': 'void', 'Float -': 'Float', 'Float *': 'Float', 'Float +': 'Float', 'Float /': 'Float', 'Int -': 'Int', 'Int *': 'Int', 'Int +': 'Int', 'Int /': 'Int'}
tree = ast.Program([ast.Definition('$main', ast.Function(ast.Args([]), [], ret='int'), True)])
funcIndex = 0
buff = '' # For names and values

def parse(source):
	while True:
		try:
			q = parse_top_level(source)
			#raise_error(source)
			tree[funcIndex].value.append(q)
		except ValueError:
			break
	return tree

def get(string, index, default):
	try:
		return string[index]
	except:
		return default

def skip_whitespace(source, iloc, n = False):
	q = ' '
	if not n:
		while (q == '\t' or q == ' '):
			q = get(source, iloc, 'null')
			iloc += 1
	else:
		while (q == '\t' or q == ' ' or q == '\n'):
			q = get(source, iloc, 'null')
			iloc += 1
	return iloc - 1

def isnumber(value):
	try:
		float(value)
	except ValueError:
		return False
	else:
		return True

def isname(value):
	return re.match(r'[^#\t\n \$0-9]+', value)

def tok(source):
	global loc
	global buff
	iloc = loc
	name = ''
#	print(':' + source[iloc])
	iloc = skip_whitespace(source, iloc)
#	print(':' + source[iloc])
	while True:
		try:
			name += source[iloc]
		except:
			name += ' '
		iloc += 1
		if name[0] == '#':
			while source[iloc] != '\n':
				iloc += 1
			iloc += 1
			try:
				iloc = skip_whitespace(source, iloc, True)
				source[iloc]
			except:
				return 'nothing'
			name = ''
		elif name == 'var':
			q = get(source, iloc, ' ')
			if (q != '\t' and q != ' ' and q != '\n'):
				continue
			loc = skip_whitespace(source, iloc)
			return 'var'
		elif name == 'val':
			q = get(source, iloc, ' ')
			if (q != '\t' and q != ' ' and q != '\n'):
				continue
			loc = skip_whitespace(source, iloc)
			return 'val'
		elif name == 'fun':
			q = get(source, iloc, ' ')
			if (q != '\t' and q != ' ' and q != '\n'):
				continue
			loc = skip_whitespace(source, iloc)
			return 'fun'
		elif isnumber(name):
			q = get(source, iloc, ' ')
			if (q != '\t' and q != ' ' and q != '\n'):
				continue
			loc = skip_whitespace(source, iloc)
			buff = name.strip()
			return 'number'
		elif isname(name):
			q = get(source, iloc, ' ')
			if (q != '\t' and q != ' ' and q != '\n'):
				continue
			loc = skip_whitespace(source, iloc)
			buff = name.strip()
			return 'name'
		elif name.strip() != name:
			return 'error'

def raise_error(source):
	try:
		source[loc]
	except:
		raise ValueError('hi')
	else:
		raise RuntimeError('Error at location ' + str(loc) + ':\n\t' + source[loc:loc+10])

def parse_definition(source, val = False):
	global loc
	iloc = loc
	name = source[iloc]
	while(isname(name)):
		iloc += 1
		name += source[iloc]
		if(name.strip() != name):
			iloc = skip_whitespace(source, iloc)
			break

	loc = iloc
#	if(name.strip() == name):
#		raise_error(source)

	name = name.strip()

	if (source[loc] != '='):
		raise_error(source)
	loc += 1

	return ast.Definition(name, parse_expr(source), val)
#	tree[funcIndex].value.append(ast.Definition('bob', ast.LiteralFloat('2.4')))

def parse_name_expr(source):
	global loc
	if (source[loc] == '='): # Whitespace already skipped
		loc += 1
		name = buff
		return ast.Assignment(name, parse_expr(source))
	elif not isname(source[loc]): # Variable
		return ast.Lookup(buff)
	else: # So it's a call
		name = buff
		q = tok(source)
		assert q == 'name'
		name2 = buff
#		try:
		return ast.Call(name, name2, [parse_expr(source)])
#		except:
#			return ast.Call(name, name2, [])

def parse_number_expr(source):
	if isname(source[loc]): # Call, probably
		name = buff
		q = tok(source)
		assert q == 'name'
		name2 = buff
		return ast.Call(name, name2, [parse_expr(source)])
	try:
		int(buff)
		return ast.LiteralInt(buff)
	except:
		return ast.LiteralFloat(buff)

def parse_function(source):
	pass

def do_nothing(source):
	return None

def parse_top_level(source):
	global loc
	loc = skip_whitespace(source, loc, True)
	return parse_expr(source)

def parse_val(source):
	return parse_definition(source, True)

def parse_expr(source):
	options = {
		'var' 		:	parse_definition,
		'val'		:	parse_val,
		'name' 		:	parse_name_expr,
		'number'	:	parse_number_expr,
		'fun'		:	parse_function,
		'nothing'	:	do_nothing,
		'error'		:	raise_error,
	}
	q = tok(source)
	return options[q](source)
