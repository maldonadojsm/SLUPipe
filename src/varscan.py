# !/usr/bin/env python
# title           :varscan.py
# description     :Varscan variant caller framework
# author          :Juan Maldonado
# date            :6/13/19
# version         :0.4
# usage           :
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.6.5
# conda_version   :4.6.14
# =================================================================================================================

from subprocess import call, DEVNULL
import os


class Varscan:
    def __init__(self, normal_bam, tumor_bam, filename, result_directory):
        self.normal_bam = normal_bam
        self.tumor_bam = tumor_bam
        self.filename = filename
        self.result_directory = result_directory
        self.samtools_dict = {
            "mpileup": ["samtools", "mpileup"],
            "reference": ["-f", "./referenceFiles/Homo_sapiens_assembly38.fasta"],
            "skipAlign": ["-q", "1"],
            "bamFiles": ["-B", "hcc1143_N_subset50K.bam", "hcc1143_T_subset50K.bam"],
            "output": ["-o", "./varscan_output/"]
        }

        self.varscan_somatic_dict = {
            "somatic": ["varscan", "somatic"],
            "input|output": ["input_pileup_filepath", "vcf_output_filepath"],
            "mpileup": ["--mpileup", "1"],
            "minCoverage": ["--min-coverage", "8"],
            "minCovNorm": ["--min-coverage-normal", "8"],
            "minCovTum": ["--min-coverage-tumor", "6"],
            "minVarFreq": ["--min-var-freq", "0.10"],
            "minFreqHom": ["--min-freq-for-hom", "0.75"],
            "normPurity": ["--normal-purity", "1.0"],
            "tumPurity": ["--tumor-purity", "1.00"],
            "pValue": ["--p-value", "0.99"],
            "somPValue": ["--somatic-p-value", "0.05"],
            "strandFilter": ["--strand-filter", "0"],
            "outputFormat": ["--output-vcf"]

        }
        self.process_dict = {
            "processSomatic": ["varscan", "processSomatic"],
            "output": ["./varscan_output/"],
            "minTumFreq": ["--min-tumor-freq", "0.10"],
            "maxNormFreq": ["--max-normal-freq", "0.05"],
            "pValue": ["--p-value", "0.07"]
        }

        self.file_header = "1i #Varscan Indels"
        self.file_header_snp = "1i #Varscan SNPs"
        self.samtools = []
        self.varscan = []
        self.process_indel = []
        self.process_snv = []
        self.variant_caller_id = "varscan"
        self.variant_caller_output = ""
        self.variant_caller_snv_output = ""
        self.generate_dir()
        self.bind_inputs()

    def run_variant_caller(self):
        """
        Execute Variant Caller Workflow
        """
        # Samtools
        for i in self.samtools_dict.values():
            for j in i:
                self.samtools.append(j)
        # Varscan Somatic
        for i in self.varscan_somatic_dict.values():
            for j in i:
                self.varscan.append(j)
        # Process Indel
        for i in self.process_dict.values():
            for j in i:
                self.process_indel.append(j)

        print("Varscan: Calling Variants -> " + self.filename)
        # Samtools
        call(self.samtools, stdout=DEVNULL, stderr=DEVNULL)
        # Varscan Somatic
        call(self.varscan, stdout=DEVNULL, stderr=DEVNULL)
        # Process Indels

        call(self.process_indel,  stdout=DEVNULL, stderr=DEVNULL)

        # Process SNV

        self.process_dict["output"][0] = "./output/" + self.filename + "/vcf/varscan_output/" + self.filename + ".snv.vcf"
        self.variant_caller_snv_output += self.process_dict["output"][0]

        print("Varscan: Calling Variants Complete -> " + self.filename)

    def generate_dir(self):
        """
        Generates Output Subdirectory to store VCF results
        """
        os.mkdir(self.result_directory + "vcf/varscan_output/")

    def bind_inputs(self):

        """
        Update Dictionaries with relevant input needed to process workflow
        Update Output file paths needed to process Annotation Worflow
        """

        # samtools User Specific Arguments
        self.samtools_dict["bamFiles"][1] = "./input/normal_mode/" + self.normal_bam
        self.samtools_dict["bamFiles"][2] = "./input/normal_mode/" + self.tumor_bam
        self.samtools_dict["output"][1] = "./output/" + self.filename + "/vcf/varscan_output/" + self.filename + ".pileup"

        # varscan User Specific Arguments
        self.varscan_somatic_dict["input|output"][0] = self.samtools_dict["output"][1]
        self.varscan_somatic_dict["input|output"][1] = "./output/" + self.filename + "/vcf/varscan_output/" + self.filename
        # processIndel
        self.process_dict["output"][0] = "./output/" + self.filename + "/vcf/varscan_output/" + self.filename + ".indel.vcf"
        self.variant_caller_output += self.process_dict["output"][0]


