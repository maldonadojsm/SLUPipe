# !/usr/bin/env python
# title           :muse.py
# description     :MuSE Variant Caller Framework
# author          :Juan Maldonado
# date            :6/13/19
# version         :0.5
# usage           :
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.6.5
# conda_version   :4.6.14
# =================================================================================================================

import os
from subprocess import call, DEVNULL


class Muse:
    def __init__(self, normal_bam, tumor_bam, filename, result_directory, chromosome_range):
        """
        Class Constructor
        :param normal_bam: normal BAM file
        :param tumor_bam: tumor BAM file
        :param filename: Sample ID
        :param result_directory: Output file path
        :param chromosome_range: Chromosome Range indicated for analysis
        """
        self.normal_bam = normal_bam
        self.tumor_bam = tumor_bam
        self.filename = filename
        self.result_directory = result_directory
        self.chromosome_range = chromosome_range

        self.muse_call_dict = {
            "Exe": ["MuSE", "call"],
            "reference": ["-f", "./referenceFiles/Homo_sapiens_assembly38.fasta"],
            "chromosome_range": ["-r", "chr1:16,000,000-215,000,000"],
            "tumor_bam": ["hcc1143_T_subset50K.bam"],
            "normal_bam": ["hcc1143_N_subset50K.bam"],
            "output": ["-O", "./muse_output/"]
        }

        self.muse_sump_dict = {
            "Exe": ["MuSE", "sump"],
            "input": ["-I", "./muse_output/muse_call.MuSE.txt"],
            "DBSNP": ["-E", "-D", "./referenceFiles/dbSNP142_GRCh38_subset50k.vcf.gz"],
            "output": ["-O", "./muse_output/"]
        }

        self.file_header = "1i #MuSE"
        self.muse_call = []
        self.muse_sump = []
        self.variant_caller_output = ""
        self.variant_caller_snv_output = None
        self.variant_caller_id = "muse"
        self.generate_dir()
        self.bind_inputs()

    def run_variant_caller(self):
        """
        Execute Variant Caller Workflow
        """
        for i in self.muse_call_dict.values():
            for j in i:
                self.muse_call.append(j)
        for i in self.muse_sump_dict.values():
            for j in i:
                self.muse_sump.append(j)
        print("MuSE: Calling Variants -> " + self.filename)
        call(self.muse_call, stdout=DEVNULL, stderr=DEVNULL)
        call(self.muse_sump, stdout=DEVNULL, stderr=DEVNULL)
        print("MuSE: Calling Variants Complete -> " + self.filename)

    def generate_dir(self):
        """
        Generates Output Subdirectory to store VCF results
        """
        os.mkdir(self.result_directory + "vcf/muse_output/")


    def bind_inputs(self):
        """
        Update Dictionaries with relevant input needed to process workflow
        Update Output file paths needed to process Annotation Worflow
        """
        # MuSE Call User Specific Arguments
        self.muse_call_dict["tumor_bam"][0] = "./input/normal_mode/" + self.tumor_bam
        self.muse_call_dict["normal_bam"][0] = "./input/normal_mode/" + self.normal_bam
        self.muse_call_dict["output"][1] = "./output/" + self.filename + "/vcf/muse_output/" + self.filename

        # MuSE Sump User Specific Arguments
        self.muse_sump_dict["input"][1] = self.muse_call_dict["output"][1] + ".MuSE" + ".txt"
        self.muse_sump_dict["output"][1] = "./output/" + self.filename + "/vcf/muse_output/" + self.filename + ".vcf"
        self.variant_caller_output += self.muse_sump_dict["output"][1]

        # Bind Chrome Range

        self.muse_call_dict["chromosome_range"][1] = self.chromosome_range

