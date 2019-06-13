# !/usr/bin/env python
# title           :Mutect2.py
# description     :Mutect 2 Variant Caller Framework
# author          :Juan Maldonado
# date            :6/13/19
# version         :0.4
# usage           :
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.6.5
# conda_version   :4.6.14
# =================================================================================================================


from subprocess import call, DEVNULL
import os


class Mutect2:

    # Constructor
    def __init__(self, normalBAM, tumorBAM, fileName, resultDirectory, chromeRange):
        """
        Class Constructor
        :param normalBAM: normal BAM file
        :param tumorBAM: tumor BAM file
        :param fileName: Sample ID
        :param resultDirectory: Output file path
        :param chromeRange: Chromosome Range indicated for analysis
        """
        self.normalBAM = normalBAM
        self.tumorBAM = tumorBAM
        self.fileName = fileName
        self.resultDirectory = resultDirectory
        self.chrome_range = chromeRange
        self.mutectDictionary = {
            "Exe": ["java", "-jar", "GenomeAnalysisTK.jar", "-T", "MuTect2"],
            "reference": ["-R", "./referenceFiles/Homo_sapiens_assembly38.fasta"],
            "tumorBam": ["-I:tumor", "hcc1143_T_subset50K.bam"],
            "normalBam": ["-I:normal", "hcc1143_N_subset50K.bam"],
            "normalPanel": ["--normal_panel", "./referenceFiles/1kg_40_m2pon_sitesonly_subset50k.vcf"],
            "DBSNP": ["--dbsnp", "./referenceFiles/dbSNP142_GRCh38_subset50k.vcf"],
            "threads": ["-nct", "25"],
            "chromosomeRange": ["-L", "chr6:33,413,000-118,315,000"],
            "output": ["-o", "./mutect2_output/"]

        }
        if normalBAM is None:
            self.adjustForTumorOnly()
        self.fileHeader = "1i #Mutect2"
        self.mutect2 = []
        self.variantCallerOutput = ""
        self.variantCallerSnvOutput = None
        self.callerID = "mutect2"
        self.genDir()
        self.bindInputs()

    # Runs MuSE via BASH
    def runVariantCaller(self):
        """
        Execute Variant Caller Workflow
        """
        for i in self.mutectDictionary.values():
            for j in i:
                self.mutect2.append(j)
        print("MuTect2: Calling Variants -> " + self.fileName)
        call(self.mutect2, stdout=DEVNULL, stderr=DEVNULL)
        print("Mutect2: Calling Variants Complete -> " + self.fileName)

    def adjustForTumorOnly(self):
        self.mutectDictionary.pop('normalBam', None)
        self.mutectDictionary.pop('normalPanel', None)
        self.mutectDictionary.pop('DBSNP', None)


    # Generate Directory
    def genDir(self):
        """
        Generates Output Subdirectory to store VCF results
        """
        os.mkdir(self.resultDirectory + "VCF/mutect2_output/")

    # Updates Dictionaries
    def bindInputs(self):
        """
        Update Dictionaries with relevant input needed to process workflow
        Update Output file paths needed to process Annotation Worflow
        """
        if self.normalBAM is None:
            self.mutectDictionary["tumorBam"][1] = "./input/tumor_mode/" + self.tumorBAM
        else:
            self.mutectDictionary["tumorBam"][1] = "./input/normal_mode/" + self.tumorBAM
            self.mutectDictionary["normalBam"][1] = "./input/normal_mode/" + self.normalBAM
        self.mutectDictionary["output"][1] = "./output/" + self.fileName + "/VCF/mutect2_output/" + self.fileName + ".vcf"
        self.variantCallerOutput += self.mutectDictionary["output"][1]

        # Bind Chromosome Range

        self.mutectDictionary["chromosomeRange"][1] = self.chrome_range


