def delete_trash(cmd,dictionary):
	for x in dictionary:
		cmd = cmd.replace(x,"").strip()
	return cmd

def delete_text_before_command(cmd,dictionary):
	for x in dictionary:
		temp_str = ''
		temp_str2 = ''
		for y in cmd:
			if y != ' ' :
				temp_str2 = temp_str2 + y
				temp_str = temp_str + y
			else:
				temp_str2 = temp_str2 + y
				if x == temp_str:
					cmd = cmd.replace(temp_str2,"").strip()
					return cmd
				else:
					temp_str = ''
def recognize_cmd(cmd,dictionary):
	RC = {'cmd':'', 'percent':0}
	from fuzzywuzzy import fuzz
	temp_str = ''
	for x in cmd+" ":
		if x != ' ':
			temp_str += x
		else:
			for c,v in dictionary.items():
				for y in v:
					vrt=fuzz.ratio(temp_str,y)
					if vrt > RC['percent']:
						RC['cmd'] = c
						RC['percent'] = vrt
						if RC['percent'] > 70:
							return RC
			temp_str = ''
	RC['cmd'] = ''
	return RC
