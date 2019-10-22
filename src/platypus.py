# !/usr/bin/env python
# title           :platypus.py
# description     :Platypus Variant Caller Framework
# author          :Juan Maldonado
# date            :6/28/19
# version         :0.5
# usage           :
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.5.3
# conda_version   :4.6.14
# =================================================================================================================

from subprocess import call, DEVNULL
import os
import json


class Platypus:
    def __init__(self, tumor_bam, filename, result_directory, input_directory, reference_directory, json_arg_file):
        """
         Class Constructor
         :param tumor_bam: tumor BAM file
         :param filename: Sample ID
         :param result_directory: Output file path
         :param input_directory: BAM files input directory
         :param reference_directory: Fasta files input directory
         """
        self.tumor_bam = tumor_bam
        self.filename = filename
        self.result_directory = result_directory + "vcf/platypus_output/"
        self.input_directory = input_directory
        self.reference_directory = reference_directory
        with open(json_arg_file, 'r') as json_file:
            data = json.load(json_file)
            self.custom_platypus_dict = {i: j for i, j in data[0]['call_Variants'].items()}

        self.platypus = ["platypus", "callVariants"]
        self.file_header = "li #Platypus"
        self.variant_caller_id = "platypus"
        self.variant_caller_output = ""
        self.variant_caller_snv_output = None
        self.generate_dir()
        self.bind_inputs()

    def generate_dir(self):
        """
        Execute Variant Caller Workflow
        """
        os.mkdir(self.result_directory)

    def run_variant_caller(self):

        print("Platypus: Calling Variants -> " + self.filename)
        variant_caller_log = open(self.result_directory + "variant_caller_logs.txt", "w")

        call(self.platypus, stdout=variant_caller_log, stderr=DEVNULL)
        print("Platypus: Calling Variants Complete -> " + self.filename)
        variant_caller_log.close()

    def bind_inputs(self):
        """
        Update Dictionaries with relevant input needed to process workflow
        Update Output file paths needed to process Annotation Workflow
        """

        """
        Prepare callVariant
        """
        # Add Tumor File
        self.platypus.append("--bamFiles=" + self.input_directory + self.tumor_bam)

        # Add Reference File

        self.platypus.append("--refFile=" + self.reference_directory + "Homo_sapiens_assembly38.fasta")

        # Add Custom Arguments

        for i, j in self.custom_platypus_dict.items():
            self.platypus.append(i+j)

        # Add Output

        self.platypus.append("--output=" + self.result_directory + self.filename + ".vcf")

        self.variant_caller_output = self.result_directory + self.filename + ".vcf"
