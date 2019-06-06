from subprocess import call, DEVNULL
import os

# Pending:
#
# 1. Create a new directory in sniper_output per sample
class Sniper:



    fileHeader = "1i #SomaticSniper"
    sniper = []
    variantCallerOutput = ""

    # Constructor
    def __init__(self, normalBAM, tumorBAM, fileName, resultDirectory):
        self.normalBAM = normalBAM
        self.tumorBAM = tumorBAM
        self.fileName = fileName
        self.resultDirectory = resultDirectory

        self.sniperDictionary = {
            "Exe": ["bam-somaticsniper"],
            "qualityFilter": ["-q", "1"],
            "omitVariantsLOH": ["-L", "-G"],
            "SomaticSnvQuality": ["-Q", "15"],
            "priorProbSomatic": ["-s", "0.01"],
            "thetaMaqConsensus": ["-T", "0.85"],
            "numHalotypes": ["-N", "2"],
            "priorDifHalotypes": ["-r", "0.001"],
            "normalID": ["-n", "NORMAL"],
            "tumorID": ["-t", "TUMOR"],
            "outputFormat": ["-F", "vcf"],
            "reference": ["-f", "./referenceFiles/Homo_sapiens_assembly38.fasta"],
            "tumorBam": ["hcc1143_T_subset50K.bam"],
            "normalBam": ["hcc1143_N_subset50K.bam"],
            "output": ["./sniper_output/"]
        }
        self.fileHeader = "1i #SomaticSniper"
        self.sniper = []
        self.variantCallerOutput = ""
        self.variantCallerSnvOutput = None
        self.callerID = "sniper"
        self.genDir()
        self.bindInputs()
    # Runs MuSE via BASH
    def runVariantCaller(self):
        for i in self.sniperDictionary.values():
            for j in i:
                self.sniper.append(j)

        print("Somatic Sniper: Calling Variants -> " + self.fileName)
        call(self.sniper, stdout=DEVNULL, stderr=DEVNULL)
        print("Somatic Sniper: Calling Variants Complete -> " + self.fileName)

    # Generate Directory
    def genDir(self):
        os.mkdir(self.resultDirectory + "VCF/somatic_sniper_output/")


    # Updates Dictionaries
    def bindInputs(self):

        # samtools User Specific Arguments
        self.sniperDictionary["tumorBam"][0] = "./input/normal_mode/" + self.tumorBAM
        self.sniperDictionary["normalBam"][0] = "./input/normal_mode/" + self.normalBAM
        self.sniperDictionary["output"][0] = "./output/" + self.fileName + "/VCF/somatic_sniper_output/" + self.fileName + ".vcf"
        self.variantCallerOutput += self.sniperDictionary["output"][0]


