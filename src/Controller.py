import os
import Pipeline
from subprocess import call
import sys
#######################################
#                                     #
#     ##    #   #######   #######     #
#     # #   #   #         #           #
#     #  #  #   #  ####   #######     #
#     #   # #   #     #         #     #
#     #    ##   #######   #######     #
#                                     #
#######################################

# Version: 1.1 (4/15/19)
# Anaconda 3.6
# Authors: Juan Maldonado & Zohair Siddiqui
# Adviser : Dr. Ahn
# Client: Dr. Guo
# CAPSTONE II, Spring 2019
# Consult README.md for detailed description of installation process and usage.

########################################
#         PIPELINE CONTROLLER          #
########################################

# USAGE: python3 NGS.py

# This file will be in charge of managing all instances of variant callers

# To Do List:

# 8. Error Handling

# COMMENTS:

# USAGE: python3 PipelineController.py
# Generating vcf.gz and vcf.gz.tbi FORMAT (MuSE Sump)
# bgzip -c file.vcf > file.vcf.gz (generates vcf.gz file)
# tabix -p vcf file.vcf.gz (generates index file)




class Controller:
    def __init__(self ,configFile):
        self.samplesToProcess = []
        self.directory = []
        self.variantcallers_tumorMode = list(configFile["variantCallers_tumorMode"])
        self.variantcallers_normalMode = list(configFile["variantCallers_normalMode"])
        self.inputTumorDirectory = configFile["input_tumor"]
        self.inputNormalDirectory = configFile["input_normal"]
        self.chromosomeRange = configFile["chromosome_Range"]
        self.vep_script_path = configFile["vepScriptPath"]
        self.vep_cache_path = configFile["vepCachePath"]
        self.buffer = ""
        self.main_menu = 1
        self.menu = 1

    def run(self):
        print()
        print(" #######   #         #     #   #######   #   #######   #######")
        print(" #         #         #     #   #     #   #   #     #   #")
        print(" #######   #         #     #   #######   #   #######   #######")
        print("       #   #         #     #   #         #   #         #")
        print(" #######   #######   #######   #         #   #         #######  ")
        print()
        print("Version 1.0, Juan Maldonado & Zohair Siddiqui, St. Louis University, 2019.")

        while self.main_menu == 1:
            print()
            self.buffer = input("Welcome to the NGS Pipeline. Type T for TUMOR ONLY Mode, N for NORMAL MODE or X to Exit: ")
            # TUMOR MODE
            if self.buffer == 'T':
                while self.menu == 1:
                    print()
                    # STORE USER INPUTS
                    print("READING TUMOR MODE DIRECTORY")
                    self.readDirectory(0)
            # NORMAL MODE
            elif self.buffer == 'N':
                while self.menu == 1:
                    print()
                    print("READING NORMAL MODE DIRECTORY")
                    self.readDirectory(1)
            elif self.buffer == 'X':
                print("Exiting Program")
                self.main_menu = 0

    """
    
    Make this section read the entire directory and then ask user to choose which files he would like to process;
    prompting in case a file already exists
    
    DONE:
    
    1. LET USER CHOOSE WHICH FILES TO PROCESS
    2. CREATE DIRECTORY PER SAMPLE
    
    PENDING:
    
    RELAY RESULT DIRECTORY TO VARIANT CALLER, ANNOTATOR & CONVERTER
    
    """

    def checkConfig(self):
        print(self.vep_cache_path)
        print(self.vep_script_path)
        print(self.chromosomeRange)
        print(self.inputNormalDirectory)
        print(self.inputTumorDirectory)

        for i in self.variantcallers_normalMode:
            print(i)

        for a in self.variantcallers_tumorMode:
            print(a)


    def readDirectory(self, flag):
        # User Has Indicated TUMOR ONLY MODE
        if flag == 0:
            directoryListing = os.listdir(self.inputTumorDirectory)
            for item in directoryListing:
                if "_T" and '.bam' in item:
                    # Capture Filename
                    fileName = os.path.splitext(os.path.basename(item))[0]
                    # Capture tumorBAM PATH
                    tumorBam = os.path.basename(item)
                    # Store in Sample List
                    self.directory.append(directoryStruct(tumorBam, fileName))

            self.confirmInputs(0)

        # User Has Indicated NORMAL MODE
        if flag == 1:
            directoryListing = os.listdir(self.inputNormalDirectory)
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
        # Confirming TUMOR ONLY MODE Inputs
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

                NGS = Pipeline.Pipeline(self.samplesToProcess, self.chromosomeRange, self.vep_script_path, self.vep_cache_path)

                # Pindel, Platypus, MuTect

                NGS.runTumorMode("Pindel", "Platypus", "MuTect") ## Add Callers Here
                print()
                print("############################")
                print(" PIPELINE WORKFLOW COMPLETE")
                print("############################")
                print()
                self.samplesToProcess.clear()
                self.directory.clear()
                self.menu = 0
            elif confirmation == 'N':
                print("Please Insert Sample Files Into Appropriate Directories")
                self.samplesToProcess.clear()
                self.directory.clear()
                self.menu = 0
            elif confirmation == 'X':
                print("Returning to Main Menu")
                self.samplesToProcess.clear()
                self.directory.clear()
                self.menu = 0

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

                NGS = Pipeline.Pipeline(self.samplesToProcess, self.chromosomeRange, self.vep_script_path, self.vep_cache_path)

                # MuSE,MuTect,Varscan,Sniper,Strelka2
                NGS.runNormalMode("MuSE", "MuTect", "Varscan", "Sniper", "Strelka2") # Add Normal Callers Here
                print()
                print("############################")
                print(" PIPELINE WORKFLOW COMPLETE")
                print("############################")
                print()
                self.directory.clear()
                self.samplesToProcess.clear()
                self.menu = 0
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
        if flag == 0:

            directoryListing = os.listdir(self.inputTumorDirectory)
            for item in directoryListing:
                if ".bam" in item:
                    bamFile = os.path.abspath(item)
                    baiFile = bamFile.replace(".bam", ".bai")
                    call(["samtools", "index", item, baiFile])
        if flag == 1:
            directoryListing = os.listdir(self.inputNormalDirectory)
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
        self.normalBAM = normalBAM
        self.tumorBAM = tumorBAM
        self.fileName = fileName
        self.resultDirectory = ""



    def genDirectory(self):
        os.mkdir("./output/" + self.fileName + "/")
        os.mkdir("./output/" + self.fileName + "/VCF/")
        os.mkdir("./output/" + self.fileName + "/AnnotatedVCF/")
        os.mkdir("./output/" + self.fileName + "/MAF/")
        self.resultDirectory = "./output/" + self.fileName + "/"

