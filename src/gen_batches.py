import json
import os

# 1. Read Input Directory (Must only read Normal/Tumar BAM Files,Count Normal + Bam Pairs as One Sample)
# 2. Dump Normal & Tumor Files into a Python Structre and then dump that structure into a list
# 3. Based on number of nodes/batches, divide workload into new JSON. 
# 4. Two Batches -> Send Half to First JSON config file (Push those structures outside list) and then dump the remaining into the other JSON file

class sample_struct:
        def __init__(self, tumor_bam,normal_bam=None):
                self.tumor_bam = tumor_bam
                self.normal_bam = normal_bam


sample_counter = 0
master_list = []
with open('config.json', 'r') as json_file:
	data = json.load(json_file)
	directory_listing = os.listdir(data[0]["Input_Directory"])
	nodes = int(data[0]["nodes"])
	if data[0]["Pipeline_Mode"] == "-N":
		for item in directory_listing:
			if "_N" and ".bam" in item:
				for item2 in directory_listing:
					if "_T" and ".bam" in item2:
						normal_bam_file = os.path.splitext(os.path.basename(item))[0].replace("_N", "")
						tumor_bam_file = os.path.splitext(os.path.basename(item2))[0].replace("_T", "")
						if normal_bam_file == tumor_bam_file:
							master_list.append(sample_struct(item, item2))
							sample_counter += 1

	if data[0]["Pipeline_Mode"] == "-T":
		for item in directory_listing:
			if "_T" and ".bam" in item:
				tumor_bam_file = os.path.basename(item)
				if "_T" in tumor_bam_file:
					master_list.append(sample_struct(item))
					sample_counter += 1


	samples_per_batch = sample_counter // nodes
	remainder = sample_counter % nodes	
	while(sample_counter > 0):
		for i in range(nodes):
			file = "JSON_" + str(i+1) + ".json" #JSON_1
			framework = data #JSON Config.json framework		
			with open(file, 'w') as export_json:
			
					
				if sample_counter == samples_per_batch + remainder :
					for i in range(samples_per_batch + remainder):
						object = master_list.pop()
						if framework[0]["Pipeline_Mode"] == "-N":
							framework[0]["node_samples"].append(object.tumor_bam)
							framework[0]["node_samples"].append(object.normal_bam)
							sample_counter -= 1
						if framework[0]["Pipeline_Mode"] == "-T":
							framework[0]["node_samples"].append(object.tumor_bam)
							sample_counter -= 1
				else:
					for i in range(samples_per_batch): 
						object = master_list.pop()
						if framework[0]["Pipeline_Mode"] == "-N":
							framework[0]["node_samples"].append(object.tumor_bam)
							framework[0]["node_samples"].append(object.normal_bam)
							sample_counter -= 1
						if framework[0]["Pipeline_Mode"] == "-T":
							framework[0]["node_samples"].append(object.tumor_bam)
							sample_counter -= 1

				json.dump(framework, export_json, indent = 4) #JSON_1.json -> Demo 10 to 6
		
			framework[0]["node_samples"].clear()

	"""
	for i in range(len(master_list)):
		data[0]["node_samples"].append(master_list[i].tumor_bam)
		data[0]["node_samples"].append(master_list[i].normal_bam)
	"""
