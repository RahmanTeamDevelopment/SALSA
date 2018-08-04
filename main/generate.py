
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
			elif key == "ensembl":
				write_file.write("@"+key+" = "+ini_dict["transcript_db"]+"\n")
			elif key == "reference":
				write_file.write("@"+key+" = "+ref_with_path+"\n")
			else:
				write_file.write(line+"\n")
		else:
			write_file.write(line+"\n")
	read_file.close()
	write_file.close()
	

##########################################
# Function to generate the CoverView configuration file
##########################################
def coverview_configuration(out, ini_dict):
	out_file = open(out,'w')
	out_file.write("{\n")
	out_file.write("\t\"count_duplicate_reads\": "+ini_dict["coverview.count_duplicate_reads"]+" },\n")
	out_file.write("\t\"outputs\": { \"regions\": "+ini_dict["coverview.outputs_regions"]+", \"profiles\": "+ini_dict["coverview.outputs_profiles"]+" },\n")
	out_file.write("\t\"low_bq\": "+ini_dict["coverview.low_bq"]+",\n")
	out_file.write("\t\"low_mq\": "+ini_dict["coverview.low_mq"]+",\n")
	out_file.write("\t\"pass\": { \"MINQCOV_MIN\": "+ini_dict["coverview.pass_minqcov_min"]+", \"MAXFLMQ_MAX\": "+ini_dict["coverview.pass_maxflmq_max"]+", \"MAXFLBQ_MAX\": "+ini_dict["coverview.pass_maxflbq_max"]+" },\n")
	out_file.write("\t\"transcript\": { \"regions\": "+ini_dict["coverview.transcript_regions"]+", \"profiles\": "+ini_dict["coverview.transcript_profiles"]+", \"poor\": "+ini_dict["coverview.transcript_poor"]+" },\n")
	out_file.write("}\n")

