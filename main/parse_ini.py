###########
# Read in INI files and return a dictionary containing the file's information
###########
def read_in(fn):
	ret = {}
	section = ''
	with open(fn) as infile:
		for line in infile:
			line = line.strip()
			if line == '' or line.startswith('#') or line.startswith(";"): continue
			
			if line[0] == '[' and line[-1] == ']':
				s = line[1:-1]
				if '[' in s or ']' in s or '=' in s: continue
				section = s

			elif line.count('=') == 1:
				key, value = line.split('=')
				key = key.strip()
				value = value.strip()
				if section != '':
					key = '{}.{}'.format(section, key)
				ret[key] = value
	return ret

###########
# TO DO:
#   create a function to check the INI files
###########
def check_ini(dict):
	pass
