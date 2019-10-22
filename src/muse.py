# !/usr/bin/env python
# title           :muse.py
# description     :MuSE Variant Caller Framework
# author          :Juan Maldonado
# date            :6/28/19
# version         :0.1
# usage           :
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.5.3
# conda_version   :4.6.14
# =================================================================================================================

import os
import json
from subprocess import call, DEVNULL


class Muse:
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
        :param json_arg_file: json argument file path (Custom Variant Caller Objects)

        """
        self.normal_bam = normal_bam
        self.tumor_bam = tumor_bam
        self.filename = filename
        self.result_directory = result_directory + "vcf/muse_output/"
        self.chromosome_range = chromosome_range
        self.input_directory = input_directory
        self.reference_directory = reference_directory

        # Custom Arguments

        with open(json_arg_file, 'r') as json_file:
            data = json.load(json_file)

            self.custom_call_dict = {i: j for i, j in data[0]['call'].items()}
            self.custom_sump_dict = {i: j for i, j in data[0]['sump'].items()}

        self.file_header = "1i #MuSE"
        self.muse_call = ["MuSE", "call"]
        self.muse_sump = ["MuSE", "sump"]

        self.variant_caller_output = ""
        self.variant_caller_snv_output = None
        self.variant_caller_id = "muse"
        self.generate_dir()
        self.bind_inputs()

    def run_variant_caller(self):
        """
        Execute Variant Caller Workflow
        """
        print("MuSE: Calling Variants -> " + self.filename)
        call(self.muse_call, stdout=DEVNULL, stderr=DEVNULL)
        call(self.muse_sump, stdout=DEVNULL, stderr=DEVNULL)
        print("MuSE: Calling Variants Complete -> " + self.filename)

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

        # ./src/input/ + tumor/normal.bam

        # Bind Reference
        self.custom_call_dict["-f"] = self.reference_directory + "Homo_sapiens_assembly38.fasta"

        # Bind Chromosome Range

        self.custom_call_dict["-r"] = self.chromosome_range

        # Bind Samples

        # Bind Output

        self.custom_call_dict["-O"] = self.result_directory + self.filename

        #################

        # MuSE Sump User Specific Arguments

        self.custom_sump_dict["-I"] = self.custom_call_dict["-O"] + ".MuSE" + ".txt"

        self.custom_sump_dict["-D"] = self.reference_directory + "dbSNP142_GRCh38_subset50k.vcf.gz"

        self.custom_sump_dict["-O"] = self.result_directory + self.filename + ".vcf"

        self.variant_caller_output += self.custom_sump_dict["-O"]
        # Bind Chrome Range

        for i, j in self.custom_call_dict.items():
            self.muse_call.append(i)
            self.muse_call.append(j)

        self.muse_call.append(self.input_directory + self.tumor_bam)
        self.muse_call.append(self.input_directory + self.normal_bam)

        for i, j in self.custom_sump_dict.items():
            self.muse_sump.append(i)
            self.muse_sump.append(j)
