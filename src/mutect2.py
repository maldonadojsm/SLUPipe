# !/usr/bin/env python
# title           :mutect2.py
# description     :Mutect 2 Variant Caller Framework
# author          :Juan Maldonado
# date            :6/28/19
# version         :0.1
# usage           :
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.5.3
# conda_version   :4.6.14
# =================================================================================================================


from subprocess import call, DEVNULL
import json
import os


class Mutect2:
    def __init__(self, normal_bam, tumor_bam, filename, result_directory, input_directory,
                 reference_directory, chromosome_range, json_arg_file=None):
        """
        Class Constructor
        :param normal_bam: normal BAM file
        :param tumor_bam: tumor BAM file
        :param filename: Sample ID
        :param result_directory: Output file path
        :param chromosome_range: Chromosome Range indicated for analysis
        :param input_directory: BAM files input directory
        :param reference_directory: Fasta files input directory
        """
        self.normal_bam = normal_bam
        self.tumor_bam = tumor_bam
        self.filename = filename
        self.result_directory = result_directory + "vcf/mutect2_output/"
        self.chrome_range = chromosome_range
        self.input_directory = input_directory
        self.reference_directory = reference_directory

        with open(json_arg_file, 'r') as json_file:
            data = json.load(json_file)
            self.custom_mutect_dict = {i: j for i, j in data[0]['mutect2'].items()}

        self.file_header = "1i #Mutect2"
        self.mutect2 = ["java", "-jar", "GenomeAnalysisTK.jar", "-T", "MuTect2"]
        self.variant_caller_output = ""
        self.variant_caller_snv_output = None
        self.variant_caller_id = "mutect2"
        self.generate_dir()
        self.bind_inputs()

    def run_variant_caller(self):
        """
        Execute Variant Caller Workflow
        """
        print("MuTect2: Calling Variants -> " + self.filename)
        variant_caller_log = open(self.result_directory + "variant_caller_logs.txt", "w")
        call(self.mutect2, stdout=variant_caller_log, stderr=DEVNULL)
        print("Mutect2: Calling Variants Complete -> " + self.filename)
        variant_caller_log.close()
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

        if self.normal_bam is None:
            self.mutect2.append("-I:tumor")
            self.mutect2.append(self.input_directory + self.tumor_bam)
        else:

            self.mutect2.append("-I:tumor")
            self.mutect2.append(self.input_directory + self.tumor_bam)
            self.mutect2.append("-I:normal")
            self.mutect2.append(self.input_directory + self.normal_bam)

            self.mutect2.append("--normal_panel")
            self.mutect2.append(self.reference_directory + "1kg_40_m2pon_sitesonly_subset50k.vcf")

            self.mutect2.append("--dbsnp")
            self.mutect2.append(self.reference_directory + "dbSNP142_GRCh38_subset50k.vcf")

        self.mutect2.append("-o")
        self.mutect2.append(self.result_directory + self.filename + ".vcf")

        self.variant_caller_output += self.result_directory + self.filename + ".vcf"

        # Bind Reference & DBSNP Files
        self.mutect2.append("-R")
        self.mutect2.append(self.reference_directory + "Homo_sapiens_assembly38.fasta")

        # Bind Chromosome Range
        self.mutect2.append("-L")
        self.mutect2.append(self.chrome_range)

        for i, j in self.custom_mutect_dict.items():
            self.mutect2.append(i)
            self.mutect2.append(j)



