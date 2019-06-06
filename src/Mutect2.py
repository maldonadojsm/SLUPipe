from subprocess import call, DEVNULL
import os

# Performance Observations:
# 1. 8-10% MEM Usage/Instance
# 2. 150-200% CPU Usage/Instance
# 3. Avg Duration: 30min (2 Instances)

class Mutect2:

    # Constructor
    def __init__(self, normalBAM, tumorBAM, fileName, resultDirectory, chromeRange):
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
        os.mkdir(self.resultDirectory + "VCF/mutect2_output/")

    # Updates Dictionaries
    def bindInputs(self):

        if self.normalBAM is None:
            self.mutectDictionary["tumorBam"][1] = "./input/tumor_mode/" + self.tumorBAM
        else:
            self.mutectDictionary["tumorBam"][1] = "./input/normal_mode/" + self.tumorBAM
            self.mutectDictionary["normalBam"][1] = "./input/normal_mode/" + self.normalBAM
        self.mutectDictionary["output"][1] = "./output/" + self.fileName + "/VCF/mutect2_output/" + self.fileName + ".vcf"
        self.variantCallerOutput += self.mutectDictionary["output"][1]

        # Bind Chromosome Range

        self.mutectDictionary["chromosomeRange"][1] = self.chrome_range


