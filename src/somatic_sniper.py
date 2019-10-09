# !/usr/bin/env python
# title           :somatic_sniper.py
# description     :Somatic Sniper variant caller framework
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


class Sniper:
    def __init__(self, normal_bam, tumor_bam, filename, result_directory, input_directory, reference_directory, flag,
                 json_arg_file=None):
        """
        Class Constructor
        :param normal_bam: normal BAM file
        :param tumor_bam: tumor BAM file
        :param filename: Sample ID
        :param result_directory: Output file path
        :param input_directory: BAM files input directory
        :param reference_directory: Fasta files input directory
        """
        self.normal_bam = normal_bam
        self.tumor_bam = tumor_bam
        self.filename = filename
        self.result_directory = result_directory + "vcf/somatic_sniper_output/"
        self.input_directory = input_directory
        self.reference_directory = reference_directory
        self.flag = flag
        if self.flag == 1:
            with open(json_arg_file, 'r') as json_file:
                data = json.load(json_file)
                self.custom_mutect_dict = {i: j for i, j in data[0]['bam_somatic_sniper'].items()}

        self.sniper_dict = {

            "qualityFilter": ["-q", "1"],
            "omitVariantsLOH": ["-L", "-G"],
            "SomaticSnvQuality": ["-Q", "15"],
            "priorProbSomatic": ["-s", "0.01"],
            "thetaMaqConsensus": ["-T", "0.85"],
            "numHalotypes": ["-N", "2"],
            "priorDifHalotypes": ["-r", "0.001"],
            "normalID": ["-n", "NORMAL"],
            "tumorID": ["-t", "TUMOR"],
            "outputFormat": ["-F", "vcf"],
            "reference": ["-f", "./referenceFiles/Homo_sapiens_assembly38.fasta"],
            "tumor_bam": ["hcc1143_T_subset50K.bam"],
            "normal_bam": ["hcc1143_N_subset50K.bam"],
            "output": ["./sniper_output/"]
        }
        self.file_header = "1i #SomaticSniper"
        self.sniper = ["bam-somaticsniper"]
        self.variant_caller_output = ""
        self.variant_caller_snv_output = None
        self.variant_caller_id = "sniper"
        self.generate_dir()
        self.bind_inputs()

    def run_variant_caller(self):
        """
        Execute Variant Caller Workflow
        """
        for i in self.sniper_dict.values():
            for j in i:
                self.sniper.append(j)

        print("Somatic Sniper: Calling Variants -> " + self.filename)
        call(self.sniper, stdout=DEVNULL, stderr=DEVNULL)
        print("Somatic Sniper: Calling Variants Complete -> " + self.filename)

    def generate_dir(self):
        """
        Generates Output Subdirectory to store VCF results
        """
        os.mkdir(self.result_directory)

    def bind_inputs(self):
        """
        Update Dictionaries with relevant input needed to process workflow
        Update Output file paths needed to process Annotation Workflow
        Updates Input & Reference File paths
        """
        if self.flag == 0:
            self.sniper_dict["tumor_bam"][0] = self.input_directory + self.tumor_bam
            self.sniper_dict["normal_bam"][0] = self.input_directory + self.normal_bam
            self.sniper_dict["output"][0] = self.result_directory + self.filename + ".vcf"
            self.variant_caller_output += self.sniper_dict["output"][0]

            # Update Reference file path

            self.sniper_dict["reference"][1] = self.reference_directory + "Homo_sapiens_assembly38.fasta"

        if self.flag == 1:

            for i, j in self.custom_mutect_dict.items():
                self.sniper.append(i)
                self.sniper.append(j)

            self.sniper.append("-f")
            self.sniper.append(self.reference_directory + "Homo_sapiens_assembly38.fasta")
            self.sniper.append(self.input_directory + self.tumor_bam)
            self.sniper.append(self.input_directory + self.normal_bam)
            self.sniper.append(self.result_directory + self.filename + ".vcf")

            self.variant_caller_output += self.result_directory + self.filename + ".vcf"

