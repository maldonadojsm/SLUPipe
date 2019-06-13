# !/usr/bin/env python
# title           :MuSE.py
# description     :MuSE Variant Caller Framework
# author          :Juan Maldonado
# date            :6/13/19
# version         :0.4
# usage           :
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.6.5
# conda_version   :4.6.14
# =================================================================================================================

import os
from subprocess import call, DEVNULL


class MuSE:

    # Constructor
    def __init__(self, normalBAM, tumorBAM, fileName, resultDirectory, chromosomeRange):
        """
        Class Constructor
        :param normalBAM: normal BAM file
        :param tumorBAM: tumor BAM file
        :param fileName: Sample ID
        :param resultDirectory: Output file path
        :param chromosomeRange: Chromosome Range indicated for analysis
        """
        self.normalBAM = normalBAM
        self.tumorBAM = tumorBAM
        self.fileName = fileName
        self.resultDirectory = resultDirectory
        self.chromosome_range = chromosomeRange

        self.museCallDictionary = {
            "Exe": ["MuSE", "call"],
            "reference": ["-f", "./referenceFiles/Homo_sapiens_assembly38.fasta"],
            "chromosomeRange": ["-r", "chr1:16,000,000-215,000,000"],
            "tumorBam": ["hcc1143_T_subset50K.bam"],
            "normalBam": ["hcc1143_N_subset50K.bam"],
            "output": ["-O", "./muse_output/"]
        }

        self.museSumpDictionary = {
            "Exe": ["MuSE", "sump"],
            "input": ["-I", "./muse_output/muse_call.MuSE.txt"],
            "DBSNP": ["-E", "-D", "./referenceFiles/dbSNP142_GRCh38_subset50k.vcf.gz"],
            "output": ["-O", "./muse_output/"]
        }

        self.fileHeader = "1i #MuSE"
        self.museCall = []
        self.museSump = []
        self.variantCallerOutput = ""
        self.variantCallerSnvOutput = None
        self.callerID = "muse"
        self.genDir()
        self.bindInputs()

    # Runs MuSE via BASH
    def runVariantCaller(self):
        """
        Execute Variant Caller Workflow
        """
        for i in self.museCallDictionary.values():
            for j in i:
                self.museCall.append(j)
        for i in self.museSumpDictionary.values():
            for j in i:
                self.museSump.append(j)
        print("MuSE: Calling Variants -> " + self.fileName)
        call(self.museCall)#, stdout=DEVNULL, stderr=DEVNULL)
        call(self.museSump) #,  stdout=DEVNULL, stderr=DEVNULL)
        print("MuSE: Calling Variants Complete -> " + self.fileName)

    # Generate Directory
    def genDir(self):
        """
        Generates Output Subdirectory to store VCF results
        """
        os.mkdir(self.resultDirectory + "VCF/muse_output/")

    # Updates Dictionaries
    def bindInputs(self):
        """
        Update Dictionaries with relevant input needed to process workflow
        Update Output file paths needed to process Annotation Worflow
        """
        # MuSE Call User Specific Arguments
        self.museCallDictionary["tumorBam"][0] = "./input/normal_mode/" + self.tumorBAM
        self.museCallDictionary["normalBam"][0] = "./input/normal_mode/" + self.normalBAM
        self.museCallDictionary["output"][1] = "./output/" + self.fileName + "/VCF/muse_output/" + self.fileName

        # MuSE Sump User Specific Arguments
        self.museSumpDictionary["input"][1] = self.museCallDictionary["output"][1] + ".MuSE" + ".txt"
        self.museSumpDictionary["output"][1] = "./output/" + self.fileName + "/VCF/muse_output/" + self.fileName + ".vcf"
        self.variantCallerOutput += self.museSumpDictionary["output"][1]

        # Bind Chrome Range

        self.museCallDictionary["chromosomeRange"][1] = self.chromosome_range

