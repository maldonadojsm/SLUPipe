# !/usr/bin/env python
# title           :strelka.py
# description     :Strelka 2 variant caller framework
# author          :Juan Maldonado
# date            :6/28/19
# version         :0.1
# usage           :
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.6.5
# conda_version   :4.6.14
# =================================================================================================================


from subprocess import call, DEVNULL
import os
import json


class Strelka:
    def __init__(self, normal_bam, tumor_bam, filename, result_directory, input_directory, reference_directory,
                 json_arg_file):
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
        self.result_directory = result_directory + "vcf/strelka2_output/"
        self.input_directory = input_directory
        self.reference_directory = reference_directory
        with open(json_arg_file, 'r') as json_file:
            data = json.load(json_file)
            self.custom_strelka_config_dict = {i: j for i, j in data[0]['strelka_config'].items()}
            self.custom_strelka_run_dict = {i: j for i, j in data[0]['strelka_run'].items()}

        self.run_directory = result_directory + "vcf/strelka2_output"
        self.file_header = "1i #Strelka2"
        self.strelka_config = ["python", "./configureStrelkaSomaticWorkflow.py"]
        self.strelka_run = ["python", self.run_directory + "/runWorkflow.py"]

        # List type signifies to annotator.py to expect 2 VCFs, 1 snvs and 1 indels VCF file
        self.variant_caller_output = self.result_directory + "results/variants/somatic.indels.vcf"
        self.variant_caller_snv_output = self.result_directory + "results/variants/somatic.snvs.vcf"
        self.variant_caller_id = "strelka2"
        self.generate_dir()
        self.bind_inputs()

    def run_variant_caller(self):
        """
        Generates Output Subdirectory to store VCF results
        """
        print("Strelka 2: Calling Variants -> " + self.filename)

        # Creating the Strelka2 temporary directory
        call(self.strelka_config, stdout=DEVNULL, stderr=DEVNULL)
        variant_caller_log = open(self.result_directory + "variant_caller_logs.txt", "w")
        call(self.strelka_run, stdout=variant_caller_log, stderr=DEVNULL)
        call(["gunzip", self.run_directory + "/results/variants/somatic.snvs.vcf.gz",
              self.run_directory + "/results/variants/somatic.indels.vcf.gz"])
        variant_caller_log.close()

        print("Strelka 2: Calling Variants Complete -> " + self.filename)

    def generate_dir(self):
        """
        Generates Output Subdirectory to store VCF results
        """
        os.mkdir(self.result_directory)

    def bind_inputs(self):
        """
         Update Dictionaries with relevant input needed to process workflow
         Update Output file paths needed to process Annotation Workflow
         """

        # Strelka Call User Specific Arguments

        """
        Prepare Strelka Somatic Workflow
        """
        # Dump Normal
        self.strelka_config.append("--normalBam")
        self.strelka_config.append(self.input_directory + self.normal_bam)

        # Dump Tumor

        self.strelka_config.append("--tumorBam")
        self.strelka_config.append(self.input_directory + self.tumor_bam)

        # Set Reference

        self.strelka_config.append("--referenceFasta")
        self.strelka_config.append(self.reference_directory + "Homo_sapiens_assembly38.fasta")

        # Add Custom Arguments

        for i, j in self.custom_strelka_config_dict.items():
            self.strelka_config.append(i)
            if j:
                self.strelka_config.append(j)

        # Set Run Directory

        self.strelka_config.append("--runDir")
        self.strelka_config.append(self.run_directory)


        """
        Prepare Strelka Run
        """

        for i, j in self.custom_strelka_run_dict.items():
            self.strelka_run.append(i)
            if j:
                self.strelka_run.append(j)
