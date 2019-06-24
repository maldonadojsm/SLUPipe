# !/usr/bin/env python
# title           :controller.py
# description     :Configures SLUPipeline Workflow
# author          :Juan Maldonado
# date            :6/13/19
# version         :0.5
# usage           :SEE slupipe.py
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.6.5
# conda_version   :4.6.14
# =================================================================================================================

import os
import pipeline as pl
import sys
import shutil
from subprocess import call


# Pending:
#
# 1. Automate Bai Generation:

#
# User Story 1:
#
# 1. Reads input directory and then proceeds to check if there is a .bai file for the .bam in question. If there isn't,
# the program them proceeds to generating the .bai. I think this process should be performed based on which files are
# were chosen to be processed.
#
# User Story 2:





class Controller:

    def __init__(self, config_dict=None):
        """
        Class Constructor
        :param config_dict: Python Dictionary Storing Pipeline Configuration
        """
        self.samplesToProcess = []
        self.directory = []
        # config.json file Dictionary
        if config_dict is not None:
            self.pipeline_mode = config_dict[0]['Pipeline_Mode']
            self.variant_callers = config_dict[0]['Variant_Callers']
            self.input_directory = config_dict[0]['Input_Directory']
            self.chromosome_range = config_dict[0]['Chromosome_Range']
            self.vep_script = config_dict[0]['vep_ScriptPath']
            self.vep_cache = config_dict[0]['vep_CachePath']

    def configure_pipeline(self):
        """
        Configures pipeline mode in accordance to config file (-T: Non-Paired Mode, -N: Paired Mode)
        """
        if self.pipeline_mode == "-T":
            self.read_directory(0)

        elif self.pipeline_mode == "-N":
            self.read_directory(1)

    def show_summary(self):
        """
        Provide Execution & Version Summary of SLUPipe
        """
        print()
        print(" #######   #         #     #   #######   #   #######   #######")
        print(" #         #         #     #   #     #   #   #     #   #")
        print(" #######   #         #     #   #######   #   #######   #######")
        print("       #   #         #     #   #         #   #         #")
        print(" #######   #######   #######   #         #   #         #######  ")
        print("")
        print("SLUPipe: A (S)omatic Ana(L)ysis (U)mbrella (Pipe)line")
        print()
        print("Version: v0.5")
        print("         Build Date June 22 2019")
        print("         Build Time 00:43:02")
        print("         Authors: Dr. Tae-Hyuk (Ted) Ahn , Juan Maldonado , Zohair Siddiqui. St. Louis University, 2019.")
        print()
        print("Usage:   slupipe.py <config.json> -> Execute Pipeline Workflow")
        print("         slupipe.py --update -> Check for most recent software release")
        print()
        print("Config File Structure:  Pipeline Mode     -T for Non-paired Mode / -N for Paired Mode")
        print()
        print("                        Variant Callers   Specify List of Variant Callers for pipeline workflow")
        print("                                          in accordance pipeline mode")
        print()
        print("                        Input Directory   Samples Directory. Pipeline will automate creation of .bai files")
        print()
        print("                        Chromosome Range  Specify Chromosome Range for analysis (Format: chr1:16,000,000-215,000,000")
        print()
        print("                        VEP Script        Ensembl VEP absolute path")
        print()
        print("                        VEP Cache         Ensemble VEP local cache path")
        print()
        print("                        CPU Cores         Cores used for pipeline workflow")

    def read_directory(self, flag):
        """
        Read input directory
        :param flag: 0: Process files required for Non-paired mode (Tumor Mode), 1: Process files required for Paired Mode (Normal Mode)
        """
        if flag == 0:
            self.generate_bai_files()
            directory_listing = os.listdir(self.input_directory)
            for item in directory_listing:
                if "_T" and '.bam' in item:
                    # Capture Filename
                    filename = os.path.splitext(os.path.basename(item))[0]
                    # Capture tumorBAM PATH
                    tumor_bam = os.path.basename(item)
                    # Store in Sample List
                    self.directory.append(directoryStruct(tumor_bam, filename))
            self.confirm_inputs(0)

        if flag == 1:
            self.generate_bai_files()
            directory_listing = os.listdir(self.input_directory)
            for item in directory_listing:
                if "_N" and ".bam" in item:
                    for item2 in directory_listing:
                        if "_T" and ".bam" in item2:
                            normal_bam_file = os.path.splitext(os.path.basename(item))[0].replace("_N", "")
                            tumor_bam_file = os.path.splitext(os.path.basename(item2))[0].replace("_T", "")

                            # If BAM Normal and Tumor Files have same ID
                            if normal_bam_file == tumor_bam_file:
                                filename = normal_bam_file
                                # Store in Sample List
                                self.directory.append(directoryStruct(os.path.basename(item2), filename, os.path.basename(item)))
            self.confirm_inputs(1)

    def confirm_inputs(self, flag):
        """
        Prompts user to confirm correct inputs before initializing pipeline
        :param flag: -T: Display files that will be used for Non-Paired Mode, -N: Display files that will be used for Paired Mode
        :return:
        """
        if flag == 0:
            dash = '-' * 80
            print("TUMOR MODE: DIRECTORY SUMMARY (X to Exit):")
            print(dash)
            print("{:<10s}{:>10s}{:>20s}".format('NO.', 'ID', 'TUMOR'))
            print(dash)
            for i in range(len(self.directory)):
                print("{:<10s}{:>12s}{:>21s}".format(str(i + 1), self.directory[i].filename, self.directory[i].tumor_bam))
            print()
            confirmation = input("IS THIS CORRECT (Y/N): ")
            # START PIPELINE
            if confirmation == 'Y':
                file_num = input("SELECT FILE NUMBERS TO PROCESS (Separate File Numbers By Space): ")
                args = file_num.split()
                for i in args:
                    self.samplesToProcess.append(sampleStruct(self.directory[int(i) - 1].tumor_bam, self.directory[int(i) - 1].filename))

                # Generate Output Directories
                for j in self.samplesToProcess:
                    j.gen_sample_output_directory()

                # Run SLUPipe
                self.run_pipeline()
                
            elif confirmation == 'N':
                print("Please Insert Sample Files Into Appropriate Directories")
                sys.exit(1)

            elif confirmation == 'X':
                print("Exiting Program")
                sys.exit(1)

        # Confirming NORMAL MODE inputs
        if flag == 1:
            dash = '-' * 80
            print("NORMAL MODE: DIRECTORY SUMMARY (X to Exit):")
            print(dash)
            print("{:<10s}{:>10s}{:>20s}{:>20s}".format('NO.', 'ID', 'NORMAL', 'TUMOR'))
            print(dash)
            for i in range(len(self.directory)):
                print("{:<10s}{:>10s}{:>22s}{:>21s}".format(str(i + 1), self.directory[i].filename,
                                                            self.directory[i].normal_bam, self.directory[i].tumor_bam))
            print()
            confirmation = input("IS THIS CORRECT (Y/N): ")
            # START PIPELINE
            if confirmation == 'Y':
                file_num = input("SELECT FILE NUMBERS TO PROCESS (Separate File Numbers By Space): ")
                args = file_num.split()
                for i in args:
                    self.samplesToProcess.append(sampleStruct(self.directory[int(i) - 1].tumor_bam, self.directory[int(i) - 1].filename, self.directory[int(i) - 1].normal_bam))

                # Generate Output Directories
                for j in self.samplesToProcess:
                    j.gen_sample_output_directory()

                # Run SLUPipe
                self.run_pipeline()

            elif confirmation == 'N':
                print("Please Insert Sample Files Into Appropriate Directories")
                sys.exit(1)

            elif confirmation == 'X':
                print("Exiting Program")
                sys.exit(1)

    def run_pipeline(self):
        """
        Run SLUPipe.
        """
        print()
        print("############################")
        print("COMMENCING PIPELINE WORKFLOW")
        print("############################")
        print()

        slu_pipe = pl.Pipeline(self.samplesToProcess, self.chromosome_range, self.vep_script, self.vep_cache,
                                     self.pipeline_mode, self.variant_callers)
        slu_pipe.run_workflow()
        print()
        print("############################")
        print(" PIPELINE WORKFLOW COMPLETE")
        print("############################")
        print()

        self.samplesToProcess.clear()
        self.directory.clear()

    # Generate .bai for every .bam file found in directory
    def generate_bai_files(self):
        """
        Automate creation of .bai needed to process variant calling workflow
        """
        directory_listing = os.listdir(self.input_directory)
        for item in directory_listing:
            if ".bam" in item:
                bam_file = os.path.abspath("input/" + item)
                bai_file = bam_file.replace(".bam", ".bai")
                call(["samtools", "index", bam_file, bai_file])



class directoryStruct:
    def __init__(self, tumor_bam, filename, normal_bam = None):
        self.normal_bam = normal_bam
        self.tumor_bam = tumor_bam
        self.filename = filename

# Structure To Store Sample Information
class sampleStruct:
    def __init__(self, tumor_bam, filename, normal_bam=None):
        """
        Python structure that stores all relevant files for sample X analysis
        :param tumor_bam: BAM file necessary for Paired and Non-Paired Mode
        :param filename : Sample ID used to track progress throuhgout pipeline worfklow
        :param normal_bam: BAM file necessary for Paired Mode (Optional)
        """
        self.normal_bam = normal_bam
        self.tumor_bam = tumor_bam
        self.filename = filename
        self.results_directory = ""

    def gen_sample_output_directory(self):
        """
        Create output directory needed to store generated files from pipeline workflow
        """
        if os.path.exists("./output/" + self.filename + "/"):
            shutil.rmtree("./output/" + self.filename + "/")

        os.mkdir("./output/" + self.filename + "/")
        os.mkdir("./output/" + self.filename + "/vcf/")
        os.mkdir("./output/" + self.filename + "/annotated_vcf/")
        os.mkdir("./output/" + self.filename + "/maf/")
        self.results_directory = "./output/" + self.filename + "/"