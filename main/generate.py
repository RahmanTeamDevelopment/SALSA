
import sys

##########################################
# Function to generate the CAVA configuration file
##########################################
def cava_configuration(template, out, ref_with_path, ini_dict):
	read_file = open(template, 'r')
	write_file = open(out, 'w')
	for line in read_file:
		line = line.rstrip()
		if line.startswith("@"):
			(key, val) = line.split(" = ")
			key = key[1:]
			if "cava."+key in ini_dict:
				write_file.write("@"+key+" = "+ini_dict["cava."+key]+"\n")
				print "HERE1"
			elif key == "ensembl":
				write_file.write("@"+key+" = "+ini_dict["transcript_db"]+"\n")
				print "HERE2"
			elif key == "reference":
				write_file.write("@"+key+" = "+ref_with_path+"\n")
				print "HERE3"
			else:
				print "HERE4"
				write_file.write(line+"\n")
		else:
			write_file.write(line+"\n")
	read_file.close()
	write_file.close()
	
