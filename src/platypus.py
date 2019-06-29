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


class Platypus:
    def __init__(self, tumor_bam, filename, result_directory, input_directory, reference_directory):
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
        self.platypusDict = {
            "Exe": ["platypus", "callVariants"],
            "tumor_bam": ["--bamFiles="],
            "reference": ["--refFile="],
            "output": ["--output="]
        }
        self.platypus = []
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

        for i in self.platypusDict.values():
            for j in i:
                self.platypus.append(j)

        print("Platypus: Calling Variants -> " + self.filename)
        call(self.platypus, stdout=DEVNULL, stderr=DEVNULL)
        print("Platypus: Calling Variants Complete -> " + self.filename)

    def bind_inputs(self):
        """
        Update Dictionaries with relevant input needed to process workflow
        Update Output file paths needed to process Annotation Workflow
        """
        self.platypusDict["tumor_bam"][0] += self.input_directory + self.tumor_bam
        self.platypusDict["output"][0] += self.result_directory + self.filename + ".vcf"
        self.variant_caller_output = self.result_directory + self.filename + ".vcf"

        self.platypusDict["reference"][0] = self.reference_directory

