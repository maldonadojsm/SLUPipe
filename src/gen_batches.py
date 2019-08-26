# !/usr/bin/env python
# title           :gen_batches.py
# description     :Automates JSON file generation needed for HPC mode
# author          :Juan Maldonado
# date            :8/15/19
# version         :1.0
# usage           :python3 gen_batches.py
# notes           :
# python_version  :3.6.5
# =================================================================================================================

import json
import os

class sample_struct:
        def __init__(self, tumor_bam,normal_bam):
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
							master_list.append(sample_struct(item,item2))				
							sample_counter += 1
	print(sample_counter)
	samples_per_batch = sample_counter // nodes
	remainder = sample_counter % nodes	
	while(sample_counter > 0):
		for i in range(nodes):
			file = "JSON_" + str(i+1) + ".json" 
			framework = data		
			with open(file, 'w') as export_json:
				print(sample_counter)
				print(len(master_list))	
				if sample_counter == samples_per_batch + remainder :
					for i in range(samples_per_batch + remainder):
						object = master_list.pop()
						framework[0]["node_samples"].append(object.tumor_bam)
						framework[0]["node_samples"].append(object.normal_bam)
						sample_counter -= 1
				else:
					for i in range(samples_per_batch): 
						object = master_list.pop()
						framework[0]["node_samples"].append(object.tumor_bam)
						framework[0]["node_samples"].append(object.normal_bam)
						sample_counter -= 1
				json.dump(framework, export_json, indent = 4) 
		
			framework[0]["node_samples"].clear()
