# !/usr/bin/env python
# title           :varscan.py
# description     :Varscan variant caller framework
# author          :Juan Maldonado
# date            :6/28/19
# version         :0.1
# usage           :
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.5.3
# conda_version   :4.6.14
# =================================================================================================================

from subprocess import call, DEVNULL
import os
import json


class Varscan:
    def __init__(self, normal_bam, tumor_bam, filename, result_directory, input_directory, reference_directory, flag, json_arg_file=None ):
        self.normal_bam = normal_bam
        self.tumor_bam = tumor_bam
        self.filename = filename
        self.result_directory = result_directory + "vcf/varscan_output/"
        self.input_directory = input_directory
        self.reference_directory = reference_directory
        self.flag = flag
        if self.flag == 1:
            with open(json_arg_file, 'r') as json_file:
                data = json.load(json_file)
                self.custom_somatic_dict = {i: j for i, j in data[0]['varscan_somatic'].items()}
                self.custom_process_dict = {i: j for i, j in data[0]['varscan_processSomatic'].items()}
                self.custom_process_snv_dict = {i: j for i, j in data[0]['varscan_processSomatic'].items()}
        self.samtools_dict = {
            "reference": ["-f", "./referenceFiles/Homo_sapiens_assembly38.fasta"],
            "skipAlign": ["-q", "1"],
            "bamFiles": ["-B", "hcc1143_N_subset50K.bam", "hcc1143_T_subset50K.bam"],
            "output": ["-o", "./varscan_output/"]
        }

        self.varscan_somatic_dict = {
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
            "output": ["./varscan_output/"],
            "minTumFreq": ["--min-tumor-freq", "0.10"],
            "maxNormFreq": ["--max-normal-freq", "0.05"],
            "pValue": ["--p-value", "0.07"]
        }

        self.file_header = "1i #Varscan Indels"
        self.file_header_snp = "1i #Varscan SNPs"
        self.samtools = ["samtools", "mpileup"]
        self.varscan = ["varscan", "somatic"]
        self.process_indel = ["varscan", "processSomatic"]
        self.process_snv = ["varscan", "processSomatic"]
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
        if self.flag == 0:
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

            self.process_dict["output"][0] = self.result_directory + self.filename + ".snv.vcf"
            self.variant_caller_snv_output += self.process_dict["output"][0]

        print("Varscan: Calling Variants -> " + self.filename)
        # Samtools
        call(self.samtools, stdout=DEVNULL, stderr=DEVNULL)
        # Varscan Somatic
        call(self.varscan, stdout=DEVNULL, stderr=DEVNULL)
        # Process Indels

        call(self.process_indel, stdout=DEVNULL, stderr=DEVNULL)

        # Process SNV

        print("Varscan: Calling Variants Complete -> " + self.filename)

    def generate_dir(self):
        """
        Generates Output Subdirectory to store VCF results
        """
        os.mkdir(self.result_directory)

    def bind_inputs(self):

        """
        Update Dictionaries with relevant input needed to process workflow
        Update Output file paths needed to process Annotation Worflow
        Updates Input & Reference File paths
        """

        # samtools User Specific Arguments
        self.samtools_dict["bamFiles"][1] = self.input_directory + self.normal_bam
        self.samtools_dict["bamFiles"][2] = self.input_directory + self.tumor_bam
        self.samtools_dict["output"][1] = self.result_directory + self.filename + ".pileup"
        self.samtools_dict["reference"][1] = self.reference_directory + "Homo_sapiens_assembly38.fasta"

        if self.flag == 0:

            # varscan User Specific Arguments
            self.varscan_somatic_dict["input|output"][0] = self.samtools_dict["output"][1]
            self.varscan_somatic_dict["input|output"][1] = self.result_directory + self.filename
            # processIndel
            self.process_dict["output"][0] = self.result_directory + self.filename + ".indel.vcf"
            self.variant_caller_output += self.process_dict["output"][0]

        if self.flag == 1:

            # Prepare Varscan Somatic

            # Bind Input/Output Varscan Somatic
            self.varscan.append(self.samtools_dict["output"][1])
            self.varscan.append(self.result_directory + self.filename)

            # Prepare Varscan Somatic
            for i, j in self.custom_somatic_dict.items():
                self.varscan.append(i)
                self.varscan.append(j)

            self.varscan.append("--output-vcf")

            # Prepare Process Indel
            self.process_indel.append(self.result_directory + self.filename + ".indel.vcf")
            for i, j in self.custom_process_dict.items():
                self.process_indel.append(i)
                self.process_indel.append(j)

            # Prepare Process Snv
            self.process_snv.append(self.result_directory + self.filename + ".snv.vcf")
            for i, j in self.custom_process_snv_dict.items():
                self.process_snv.append(i)
                self.process_snv.append(j)

            self.variant_caller_output = "./varscan_output/" + self.result_directory + self.filename + ".indel.vcf"
            self.variant_caller_snv_output = "./varscan_output/" + self.result_directory + self.filename + ".snv.vcf"


