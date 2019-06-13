# !/usr/bin/env python
# title           :Controller.py
# description     :Configures SLUPipeline Workflow
# author          :Juan Maldonado
# date            :6/13/19
# version         :0.4
# usage           :SEE NGS.py
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.6.5
# conda_version   :4.6.14
# =================================================================================================================

import os
import Pipeline
from subprocess import call

class Controller:

    def __init__(self , config_dict = None):
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


    def run(self):
        """
        Configures pipeline mode in accordance to config file (-T: Non-Paired Mode, -N: Paired Mode)
        """
        if self.pipeline_mode == "-T":
            self.readDirectory(0)

        elif self.pipeline_mode == "-N":
            self.readDirectory(1)

    def exeSummary(self):
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
        print("Version: v0.4")
        print("         Build Date June 1 2019")
        print("         Build Time 00:43:02")
        print("         Authors: Dr. Tae-Hyuk (Ted) Ahn , Juan Maldonado , Zohair Siddiqui. St. Louis University, 2019.")
        print()
        print("Usage:   NGS.py <config.json> -> Execute Pipeline Workflow")
        print("         NGS.py --update -> Check for most recent software release")
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

    def readDirectory(self, flag):
        """
        Read input directory
        :param flag: 0: Process files required for Non-paired mode (Tumor Mode), 1: Process files required for Paired Mode (Normal Mode)
        """
        if flag == 0:
            directoryListing = os.listdir(self.input_directory)
            for item in directoryListing:
                if "_T" and '.bam' in item:
                    # Capture Filename
                    fileName = os.path.splitext(os.path.basename(item))[0]
                    # Capture tumorBAM PATH
                    tumorBam = os.path.basename(item)
                    # Store in Sample List
                    self.directory.append(directoryStruct(tumorBam, fileName))

            self.confirmInputs(0)
        if flag == 1:

            directoryListing = os.listdir(self.input_directory)
            for item in directoryListing:
                if "_N" and ".bam" in item:
                    for item2 in directoryListing:
                        if "_T" and ".bam" in item2:
                            normalFile = os.path.splitext(os.path.basename(item))[0].replace("_N", "")
                            tumorFile = os.path.splitext(os.path.basename(item2))[0].replace("_T", "")
                            # If BAM Normal and Tumor Files have same ID
                            if normalFile == tumorFile:
                                fileName = normalFile
                                # Store in Sample List
                                self.directory.append(directoryStruct(os.path.basename(item2), fileName, os.path.basename(item)))

            self.confirmInputs(1)


    def confirmInputs(self, flag):
        """
        Prompts user to confirm correct inputs before initializing pipeline
        :param flag: -T: Display files that will be used for Non-Paired Mode, -N: Display files that will be used for Paired Mode
        :return:
        """
        if flag == 0:
            dash = '-' * 80
            print("TUMOR MODE DIRECTORY SUMMARY (X to Exit):")
            print(dash)
            print("{:<10s}{:>10s}{:>20s}".format('NO.', 'ID', 'TUMOR'))
            print(dash)
            for i in range(len(self.directory)):
                print("{:<10s}{:>12s}{:>21s}".format(str(i + 1), self.directory[i].fileName, self.directory[i].tumorBAM))
            print()
            confirmation = input("IS THIS CORRECT (Y/N): ")
            # START PIPELINE
            if confirmation == 'Y':
                fileNo = input("SELECT FILE NUMBERS TO PROCESS (Separate File Numbers By Space): ")
                args = fileNo.split()
                for i in args:
                    self.samplesToProcess.append(sampleStruct(self.directory[int(i) - 1].tumorBAM, self.directory[int(i) - 1].fileName))

                # Generate Output Directories
                for j in self.samplesToProcess:
                    j.genDirectory()

                ## Add a notifaction stating which variant callers will be used to process bam files.
                print()
                print("############################")
                print("COMMENCING PIPELINE WORKFLOW")
                print("############################")
                print()

                NGS = Pipeline.Pipeline(self.samplesToProcess, self.chromosome_range, self.vep_script, self.vep_cache)

                # Pindel, Platypus, MuTect

                NGS.runTumorMode("Pindel", "Platypus", "MuTect") ## Add Callers Here
                print()
                print("############################")
                print(" PIPELINE WORKFLOW COMPLETE")
                print("############################")
                print()
                self.samplesToProcess.clear()
                self.directory.clear()
            elif confirmation == 'N':
                print("Please Insert Sample Files Into Appropriate Directories")
                self.samplesToProcess.clear()
                self.directory.clear()
            elif confirmation == 'X':
                print("Returning to Main Menu")
                self.samplesToProcess.clear()
                self.directory.clear()

        # Confirming NORMAL MODE inputs
        if flag == 1:
            dash = '-'*80
            print("NORMAL MODE DIRECTORY SUMMARY (X to Exit):")
            print(dash)
            print("{:<10s}{:>10s}{:>20s}{:>20s}".format('NO.', 'ID', 'NORMAL', 'TUMOR'))
            print(dash)
            for i in range(len(self.directory)):
                print("{:<10s}{:>10s}{:>22s}{:>21s}".format(str(i+1), self.directory[i].fileName, self.directory[i].normalBAM, self.directory[i].tumorBAM))
            print()
            confirmation = input("IS THIS CORRECT (Y/N): ")
            # START PIPELINE
            if confirmation == 'Y':
                fileNo = input("SELECT FILE NUMBERS TO PROCESS (Separate File Numbers By Space): ")
                args = fileNo.split()
                for i in args:
                    self.samplesToProcess.append(sampleStruct(self.directory[int(i) - 1].tumorBAM, self.directory[int(i) - 1].fileName, self.directory[int(i) - 1].normalBAM))

                # Generate Output Directories
                for j in self.samplesToProcess:
                    j.genDirectory()

                print()
                print("############################")
                print("COMMENCING PIPELINE WORKFLOW")
                print("############################")
                print()

                # NGS = Pipeline.Pipeline(self.samplesToProcess, self.chromosomeRange, self.vep_script_path, self.vep_cache_path)

                # MuSE,MuTect,Varscan,Sniper,Strelka2
                NGS.runNormalMode("MuSE", "MuTect", "Varscan", "Sniper", "Strelka2") # Add Normal Callers Here
                print()
                print("############################")
                print(" PIPELINE WORKFLOW COMPLETE")
                print("############################")
                print()
                self.directory.clear()
                self.samplesToProcess.clear()
                return 0

            # CORRECT USER INPUTS
            elif confirmation == 'N':
                print("Please Insert Sample Files Into Appropriate Directories")
                self.samplesToProcess.clear()
                return 0
            elif confirmation == 'X':
                print("Returning to Main Menu")
                self.samplesToProcess.clear()
                return 0

    # Generate .bai for every .bam file found in directory
    def generateBai(self, flag):
        """
        Automates creation of  .bai files from user provided .bam files
        :param flag: 0: Gen .bai files for Non-paired Mode, 1: Gen .bai for Paired Mode
        """
        if flag == 0:

            directoryListing = os.listdir(self.input_directory)
            for item in directoryListing:
                if ".bam" in item:
                    bamFile = os.path.abspath(item)
                    baiFile = bamFile.replace(".bam", ".bai")
                    call(["samtools", "index", item, baiFile])
        if flag == 1:
            directoryListing = os.listdir(self.input_directory)
            for item in directoryListing:
                if ".bam" in item:
                    bamFile = os.path.abspath(item)
                    baiFile = bamFile.replace(".bam", ".bai")
                    call(["samtools", "index", item, baiFile])

class directoryStruct:
    def __init__(self, tumorBAM, fileName, normalBAM = None):
        self.normalBAM = normalBAM
        self.tumorBAM = tumorBAM
        self.fileName = fileName

# Structure To Store Sample Information
class sampleStruct:
    def __init__(self, tumorBAM, fileName, normalBAM = None):
        """
        Python structure that stores all relevant files for sample X analysis
        :param tumorBAM: BAM file necessary for Paired and Non-Paired Mode
        :param fileName: Sample ID used to track progress throuhgout pipeline worfklow
        :param normalBAM: BAM file necessary for Paired Mode (Optional)
        """
        self.normalBAM = normalBAM
        self.tumorBAM = tumorBAM
        self.fileName = fileName
        self.resultDirectory = ""



    def genDirectory(self):
        """
        Create output directory needed to store generated files from pipeline workflow
        """
        os.mkdir("./output/" + self.fileName + "/")
        os.mkdir("./output/" + self.fileName + "/VCF/")
        os.mkdir("./output/" + self.fileName + "/AnnotatedVCF/")
        os.mkdir("./output/" + self.fileName + "/MAF/")
        self.resultDirectory = "./output/" + self.fileName + "/"

