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
    def __init__(self, normal_bam, tumor_bam, filename, result_directory, input_directory, reference_directory,
                 json_arg_file=None):
        self.normal_bam = normal_bam
        self.tumor_bam = tumor_bam
        self.filename = filename
        self.result_directory = result_directory + "vcf/varscan_output/"
        self.input_directory = input_directory
        self.reference_directory = reference_directory

        with open(json_arg_file, 'r') as json_file:
            data = json.load(json_file)
            self.custom_samtools_dict = {i: j for i, j in data[0]['samtools'].items()}
            self.custom_somatic_dict = {i: j for i, j in data[0]['varscan_somatic'].items()}
            self.custom_process_dict = {i: j for i, j in data[0]['varscan_processSomatic'].items()}
            self.custom_process_snv_dict = {i: j for i, j in data[0]['varscan_processSomatic'].items()}

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

        """
        Prepare Samtools
        """
        # Add Reference
        self.samtools.append("-f")
        self.samtools.append(self.reference_directory + "Homo_sapiens_assembly38.fasta")

        # Add Custom Arguments:
        for i, j in self.custom_samtools_dict.items():
            self.samtools.append(i)
            self.samtools.append(j)

        # Add Input Flag
        self.samtools.append("-B")
        # Add Normal
        self.samtools.append(self.input_directory + self.normal_bam)
        # Add Tumor
        self.samtools.append(self.input_directory + self.tumor_bam)

        # Set Output
        self.samtools.append("-o")
        self.samtools.append(self.result_directory + self.filename + ".pileup")

        """
        Prepare Varscan Somatic
        """

        # Bind Input/Output Varscan Somatic
        self.varscan.append(self.result_directory + self.filename + ".pileup")
        self.varscan.append(self.result_directory + self.filename)

        # Prepare Varscan Somatic
        for i, j in self.custom_somatic_dict.items():
            self.varscan.append(i)
            self.varscan.append(j)

        self.varscan.append("--output-vcf")

        """
        Prepare Varscan ProcessSomatic
        """
        self.process_indel.append(self.result_directory + self.filename + ".indel.vcf")
        for i, j in self.custom_process_dict.items():
            self.process_indel.append(i)
            self.process_indel.append(j)

        # Prepare Process Snv
        self.process_snv.append(self.result_directory + self.filename + ".snv.vcf")
        for i, j in self.custom_process_snv_dict.items():
            self.process_snv.append(i)
            self.process_snv.append(j)

        self.variant_caller_output += self.result_directory + self.filename + ".indel.vcf"
        self.variant_caller_snv_output += self.result_directory + self.filename + ".snv.vcf"


