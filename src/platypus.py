# !/usr/bin/env python
# title           :platypus.py
# description     :Platypus Variant Caller Framework
# author          :Juan Maldonado
# date            :6/13/19
# version         :0.5
# usage           :
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.6.5
# conda_version   :4.6.14
# =================================================================================================================

from subprocess import call, DEVNULL
import os


class Platypus:
    def __init__(self, tumor_bam, filename, result_directory):
        """
          Class Constructor
          :param tumor_bam: tumor BAM file
          :param filename: Sample ID
          :param result_directory: Output file path
          """
        self.tumor_bam = tumor_bam
        self.filename = filename
        self.result_directory = result_directory
        self.platypusDict = {
            "Exe": ["platypus", "callVariants"],
            "tumor_bam": ["--bamFiles="],
            "reference": ["--refFile=../src/referenceFiles/Homo_sapiens_assembly38.fasta"],
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
        os.mkdir(self.result_directory + "vcf/platypus_output/")

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
        Update Output file paths needed to process Annotation Worflow
        """
        self.platypusDict["tumor_bam"][0] += "./input/tumor_mode/" + self.tumor_bam
        self.platypusDict["output"][0] += "./output/" + self.filename + "/vcf/platypus_output/" + self.filename + ".vcf"
        self.variant_caller_output = "./output/" + self.filename + "/vcf/platypus_output/" + self.filename + ".vcf"

