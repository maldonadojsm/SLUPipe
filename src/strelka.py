# !/usr/bin/env python
# title           :strelka.py
# description     :Strelka 2 variant caller framework
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


class Strelka:
    def __init__(self, normal_bam, tumor_bam, filename, result_directory):
        """
        Class Constructor
        :param normal_bam: normal BAM file
        :param tumor_bam: tumor BAM file   
        :param filename:  Sample ID
        :param result_directory: Output file path
        """
        self.normal_bam = normal_bam
        self.tumor_bam = tumor_bam
        self.filename = filename
        self.result_directory = result_directory
        
        self.strelka_config_dict = {
            "Exe": ["python", "./configureStrelkaSomaticWorkflow.py"],
            "normal_bam": ["--normalBam", "./hcc1143_N_subset50K.bam"],
            "tumor_bam": ["--tumorBam", "./hcc1143_T_subset50K.bam"],
            "reference": ["--referenceFasta", "./referenceFiles/Homo_sapiens_assembly38.fasta"],
            "run_directory": ["--runDir", "./vcf/strelka2_output"]
        }
        
        self.strelka_run_dict = {
            "run_directory": ["python", "./strelka2_output/runWorkflow.py"],
            "localMachine": ["-m", "local"],
            "threads": ["-j", "8"]

        }

        self.file_header = "1i #Strelka2"
        self.strelka_config = []
        self.strelka_run = []

        self.run_directory = "./output/" + self.filename + "/vcf/strelka2_output"
        # List type signifies to annotator.py to expect 2 VCFs, 1 snvs and 1 indels VCF file
        self.variant_caller_output = "./output/" + self.filename + "/vcf/strelka2_output/results/variants/somatic.indels.vcf"
        self.variant_caller_snv_output = "./output/" + self.filename + "/vcf/strelka2_output/results/variants/somatic.snvs.vcf"
        self.variant_caller_id = "strelka2"
        self.generate_dir()
        self.bind_inputs()

    def run_variant_caller(self):
        """
        Generates Output Subdirectory to store VCF results
        """
        for i in self.strelka_config_dict.values():
            for j in i:
                self.strelka_config.append(j)
        for i in self.strelka_run_dict.values():
            for j in i:
                self.strelka_run.append(j)
        print("Strelka 2: Calling Variants -> " + self.filename)

        # Creating the Strelka2 temporary directory
        call(self.strelka_config, stdout=DEVNULL, stderr=DEVNULL)

        call(self.strelka_run, stdout=DEVNULL, stderr=DEVNULL)
        call(["gunzip", self.run_directory+"/results/variants/somatic.snvs.vcf.gz", self.run_directory + "/results/variants/somatic.indels.vcf.gz"])

        print("Strelka 2: Calling Variants Complete -> " + self.filename)

    def generate_dir(self):
        """
        Generates Output Subdirectory to store VCF results
        """
        os.mkdir(self.result_directory + "vcf/strelka2_output/")

    def bind_inputs(self):
        """
         Update Dictionaries with relevant input needed to process workflow
         Update Output file paths needed to process Annotation Worflow
         """

        # Strelka Call User Specific Arguments
        self.strelka_config_dict["tumor_bam"][1] = "./input/normal_mode/" + self.tumor_bam
        self.strelka_config_dict["normal_bam"][1] = "./input/normal_mode/" + self.normal_bam
        self.strelka_config_dict["run_directory"][1] = self.run_directory
        self.strelka_run_dict["run_directory"][1] = self.run_directory+"/runWorkflow.py"
