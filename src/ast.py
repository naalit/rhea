# AST for Rhea

from codegen import *
import parser

anon_actor_num = 0
index = {}
vals = {}
rets = {'System print': 'void'}

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
		self.type = index[name].type

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

	def get_last(self):
		try:
			return self.body[-1]
		except:
			return None

	def set_last(self, last):
		self.body[-1] = last

	def remove_last(self):
		self.body = self.body[:-1]

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

class Initialization:
	def __init__(self, val, name, value):
		self.name = name
		self.value = value
		self.type = value.type
		self.val = val
		index[name] = value
		vals[name] = val

	def eval(self):
		gen_define(self.name, self.value, self.val)

class Assignment:
	def __init__(self, name, value):
		self.name = name
		self.value = value
		self.type = value.type

	def eval(self):
		gen_assign(self.name, self.value)

class Actor:
	def __init__(self, body=[]):
		global anon_actor_num
		self.body = body
		self.magic_number = anon_actor_num
		anon_actor_num += 1

	def append(self, expr):
		self.body.append(expr)

	def eval(self):
		gen_actor(self.body)

class IntLiteral:
	def __init__(self, value):
		self.value = value
		self.type = 'Int'

	def eval(self):
		gen_literal(self.value)

class FloatLiteral:
	def __init__(self, value):
		self.value = value
		self.type = 'Float'

	def eval(self):
		gen_literal(self.value)

class Send:
	def __init__(self, subject, message, args):
		self.message = message
		self.subject = subject
		self.args = args
		print(subject + '.' + message + '(' + str(args) + ')')
		nsubject = subject
		if not (subject[0].isupper() or subject[0] == '$'):
			if(parser.isnumber(nsubject)):
				try:
					int(nsubject)
					nsubject = 'Int'
				except:
					nsubject = 'Float'
			else:
				nsubject = parser.index[nsubject].type
		self.type = rets[nsubject + ' ' + message]

	def eval(self):
		gen_send(self.subject, self.message, self.args)

class ActorStart: # This is a backend thing only created by the Program class
	def __init__(self, actor):
		self.actor_number = actor.magic_number

	def eval(self):
		gen_send('$z', str(self.actor_number), [])

class Program: # Top level
	def __init__(self, array_of_instructions):
		self.body = array_of_instructions

	def append(self, statement):
		self.body.insert(-1, statement)
		return self

	def __getitem__(self, index):
		return self.body[index]

	def eval(self, repl=False):
		gen_init(repl)
		actors = []
		for i in self.body:
			i.eval()
			if isinstance(i, Actor):
				actors += [i]
			if isinstance(i, Initialization):
				if(i.value.type != 'Function'):
					gen_end()
		main = Function([], [], ret=int)
		for i in actors:
			main.append(ActorStart(i))
		gen_define('$main', main)
		gen_close()
