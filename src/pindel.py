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


class Pindel:
    def __init__(self, tumor_bam, filename, result_directory, input_directory, reference_directory, chromosome_range):
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
        self.pindel_read_dict = {
            "Exe": ["pindel"],
            "reference": ["-f", "./referenceFiles/Homo_sapiens_assembly38.fasta"],
            "configuration_file": ["-i", "config.txt"],
            "chromosomeRange": ["-c", "chr6:33,413,000-118,315,000"],
            "threads": ["-T", "8"],
            "output": ["-o", "./pindel_output/"]
        }
        self.pindel_convert_dict = {
            "Exe ": ["pindel2vcf"],
            "input": ["-p", "./pindel_output/"],
            "reference": ["-r", "./referenceFiles/Homo_sapiens_assembly38.fasta"],
            "refName": ["-R", "Homo_Sapiens_Assembly38"],
            "refDate": ["-d", "20101123"],
            "output": ["-v", "./pindel_output/"]
        }
        self.file_header = "li #Pindel"
        self.pindel_read = []
        self.pindel_convert = []
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
        for i in self.pindel_read_dict.values():
            for j in i:
                self.pindel_read.append(j)

        for i in self.pindel_convert_dict.values():
            for j in i:
                self.pindel_convert.append(j)

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
        # Pindel Read
        self.pindel_read_dict["configuration_file"][1] = self.configuration_file
        self.pindel_read_dict["output"][1] = self.result_directory + self.filename

        # Pindel2VCF
        self.pindel_convert_dict["input"][1] = self.result_directory + self.filename + "_D"
        self.pindel_convert_dict["output"][1] = self.result_directory + self.filename + ".vcf"
        self.variant_caller_output += self.pindel_convert_dict["output"][1]

        # Bind Chromosome Range

        #self.pindel_read_dict["chromosomeRange"][1] = self.chrome_range

        self.pindel_read_dict["reference"][1] = self.reference_directory + "Homo_sapiens_assembly38.fasta"
        self.pindel_convert_dict["reference"][1] = self.reference_directory + "Homo_sapiens_assembly38.fasta"



