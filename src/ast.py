# AST for Rhea

from codegen import *
import parser

class Void:
	pass
	
class Int:
	pass

class Args:
	def __init__(self, args_array):
		self.args = args_array
		
	def __str__(self):
		q = ''
		for i in self.args:
			print(str(i))
			q += str(i)
		return q
		
class Lookup:
	def __init__(self, name):
		self.name = name
		self.type = parser.index[name].type
		
	def __str__(self):
		return self.name
		
	def eval(self):
		gen_lookup(self.name)

class Function:
	def __init__(self, arguments, body, ret=None): # Body is array of instructions
		self.arguments = arguments
		self.body = body
		if ret is None:
			self.return_type = self.find_ret_type(body)
			self.__ret = True
		else:
			self.return_type = ret
			self.__ret = False
		self.type = 'Function' # 'Function' type
		
	def find_ret_type(self, body):
		try:
			ret_type = body[-1].type
		except:
			ret_type = 'void'
		return ret_type
		# TODO expand
		
	def append(self, statement):
		self.body.append(statement)
		if self.__ret:
			self.return_type = self.find_ret_type(self.body)
		return self
		
	def eval(self):
		gen_block(self.body)
		
class Definition:
	def __init__(self, name, value):
		self.name = name
		self.value = value
		self.type = value.type
		parser.index[name] = value
		
	def eval(self):
		gen_define(self.name, self.value)
		
class Assignment:
	def __init__(self, name, value):
		self.name = name
		self.value = value
		self.type = value.type
		
	def eval(self):
		gen_assign(self.name, self.value)
		
class LiteralInt:
	def __init__(self, value):
		self.value = value
		self.type = 'Int'
		
	def eval(self):
		gen_literal(self.value)
		
class LiteralFloat:
	def __init__(self, value):
		self.value = value
		self.type = 'Float'
		
	def eval(self):
		gen_literal(self.value)
		
class Call:
	def __init__(self, subject, callee, args):
		self.callee = callee
		self.subject = subject
		self.args = args
		nsubject = subject
		if not subject[0].isupper():
			if(parser.isnumber(nsubject)):
				try:
					int(nsubject)
					nsubject = 'Int'
				except:
					nsubject = 'Float'
			else:
				nsubject = parser.index[nsubject].type
		self.type = parser.rets[nsubject + ' ' + callee]
		
	def eval(self):
		gen_call(self.subject, self.callee, self.args)
	
class Program: # Top level
	def __init__(self, array_of_instructions):
		self.body = array_of_instructions
		
	def append(self, statement):
		self.body.append(statement)
		return self
		
	def __getitem__(self, index):
		return self.body[index]
		
	def eval(self, repl=False):
		gen_init(repl)
		for i in self.body:
			i.eval()
			if(i.value.type != 'Function'):
				gen_end()
		gen_close()
