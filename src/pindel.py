# !/usr/bin/env python
# title           :pindel.py
# description     :Pindel variant caller framework
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


class Pindel:
    def __init__(self, tumor_bam, filename, result_directory, input_directory, reference_directory, chromosome_range,
                 json_arg_file):
        """
         Class Constructor
         :param tumor_bam: tumor BAM file
         :param filename: Sample ID
         :param result_directory: Output file path
         :param chromosome_range: Chromosome Range indicated for analysis
         :param input_directory: BAM files input directory
         :param reference_directory: Fasta files input directory
         """
        self.tumor_bam = tumor_bam
        self.filename = filename
        self.result_directory = result_directory + "vcf/pindel_output/"
        self.chrome_range = chromosome_range
        self.input_directory = input_directory
        self.reference_directory = reference_directory

        with open(json_arg_file, 'r') as json_file:
            data = json.load(json_file)

            self.custom_pindel_read_dict = {i: j for i, j in data[0]['pindel_read'].items()}
            self.custom_pindel2vcf_dict = {i: j for i, j in data[0]['pindel2vcf'].items()}

        self.file_header = "li #Pindel"
        self.pindel_read = ["pindel"]
        self.pindel_convert = ["pindel2vcf"]
        self.variant_caller_id = "pindel"
        self.variant_caller_output = ""
        self.variant_caller_snv_output = None
        self.configuration_file = "./pindel_output/"
        self.generate_dir()
        self.gen_config_file()
        self.bind_inputs()

    def generate_dir(self):
        """
        Generates Output Subdirectory to store VCF results
        """
        os.mkdir(self.result_directory)

    def run_variant_caller(self):
        """
        Execute Variant Caller Workflow
        """
        print("Pindel: Calling Variants -> " + self.filename)
        call(self.pindel_read, stdout=DEVNULL, stderr=DEVNULL)
        # CONVERT TO VCF
        call(self.pindel_convert, stdout=DEVNULL, stderr=DEVNULL)
        print("Pindel: Calling Variants Complete -> " + self.filename)

    def gen_config_file(self):
        """
        Generates necessary pindel configuration file needed for variant caller execution
        """
        self.configuration_file = self.result_directory + self.filename + "_config.txt"
        # Forums say it varies from 300-400..
        insert_size = 350
        parameters = self.input_directory + self.tumor_bam + " " + str(insert_size) + " " + self.filename

        file = open(self.configuration_file, "w+")
        file.write(parameters)
        file.close()

    def bind_inputs(self):
        """
        Update Dictionaries with relevant input needed to process workflow
        Update Output file paths needed to process Annotation Workflow
        Updates Input & Reference File paths
        """

        """
        Prepare Pindel Read
        """

        # Add Reference File
        self.pindel_read.append("-f")
        self.pindel_read.append(self.reference_directory + "Homo_sapiens_assembly38.fasta")

        # Add Config Text

        self.pindel_read.append("-i")
        self.pindel_read.append(self.configuration_file)

        # Add Chromosome Range

        self.pindel_read.append("-c")
        self.pindel_read.append(self.chrome_range)

        # Add Custom Arguments

        for i, j in self.custom_pindel_read_dict.items():
            self.pindel_read.append(i)
            self.pindel_read.append(j)

        # Add Output

        self.pindel_read.append("-o")
        self.pindel_read.append(self.result_directory + self.filename)

        """
        Prepare Pindel2VCF
        """
        # Add Input
        self.pindel_convert.append("-p")
        self.pindel_convert.append(self.result_directory + self.filename + "_D")

        # Add Reference

        self.pindel_convert.append("-r")
        self.pindel_convert.append(self.reference_directory + "Homo_sapiens_assembly38.fasta")

        # Add Custom Arguments

        for i, j in self.custom_pindel2vcf_dict.items():
            self.pindel_convert.append(i)
            self.pindel_convert.append(j)

        # Add Output

        self.pindel_convert.append("-v")
        self.pindel_convert.append(self.result_directory + self.filename + ".vcf")

        self.variant_caller_output += self.result_directory + self.filename + ".vcf"
