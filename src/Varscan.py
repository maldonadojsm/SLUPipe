from subprocess import call, DEVNULL
import os


class Varscan:

    # Constructor
    def __init__(self, normalBAM, tumorBAM, fileName, resultDirectory):
        self.normalBAM = normalBAM
        self.tumorBAM = tumorBAM
        self.fileName = fileName
        self.resultDirectory = resultDirectory
        self.samtoolsDictionary = {
            "mpileup": ["samtools", "mpileup"],
            "reference": ["-f", "./referenceFiles/Homo_sapiens_assembly38.fasta"],
            "skipAlign": ["-q", "1"],
            "bamFiles": ["-B", "hcc1143_N_subset50K.bam", "hcc1143_T_subset50K.bam"],
            "output": ["-o", "./varscan_output/"]
        }

        self.varscanSomaticDictionary = {
            "somatic": ["varscan", "somatic"],
            "input|output": ["input_pileup_filepath", "vcf_output_filepath"],
            "mpileup": ["--mpileup", "1"],
            "minCoverage": ["--min-coverage", "8"],
            "minCovNorm": ["--min-coverage-normal", "8"],
            "minCovTum": ["--min-coverage-tumor", "6"],
            "minVarFreq": ["--min-var-freq", "0.10"],
            "minFreqHom": ["--min-freq-for-hom", "0.75"],
            "normPurity": ["--normal-purity", "1.0"],
            "tumPurity": ["--tumor-purity", "1.00"],
            "pValue": ["--p-value", "0.99"],
            "somPValue": ["--somatic-p-value", "0.05"],
            "strandFilter": ["--strand-filter", "0"],
            "outputFormat": ["--output-vcf"]

        }
        self.processDictionary = {
            "processSomatic": ["varscan", "processSomatic"],
            "output": ["./varscan_output/"],
            "minTumFreq": ["--min-tumor-freq", "0.10"],
            "maxNormFreq": ["--max-normal-freq", "0.05"],
            "pValue": ["--p-value", "0.07"]
        }


        self.fileHeader = "1i #Varscan Indels"
        self.fileHeaderSNP = "1i #Varscan SNPs"
        self.samtools = []
        self.varscan = []
        self.processIndel = []
        self.processSnv = []
        self.callerID = "varscan"
        self.variantCallerOutput = ""
        self.variantCallerSnvOutput = ""
        self.genDir()
        self.bindInputs()

    # Runs MuSE via BASH
    def runVariantCaller(self):
        # Samtools
        for i in self.samtoolsDictionary.values():
            for j in i:
                self.samtools.append(j)
        # Varscan Somatic
        for i in self.varscanSomaticDictionary.values():
            for j in i:
                self.varscan.append(j)
        # Process Indel
        for i in self.processDictionary.values():
            for j in i:
                self.processIndel.append(j)

        print("Varscan: Calling Variants -> " + self.fileName)
        # Samtools
        call(self.samtools, stdout=DEVNULL, stderr=DEVNULL)
        # Varscan Somatic
        call(self.varscan, stdout=DEVNULL, stderr=DEVNULL)
        # Process Indels

        call(self.processIndel,  stdout=DEVNULL, stderr=DEVNULL)

        # Process SNV

        self.processDictionary["output"][0] = "./output/" + self.fileName + "/VCF/varscan_output/" + self.fileName + ".snv.vcf"
        self.variantCallerSnvOutput += self.processDictionary["output"][0]

        # for i in self.processDictionary.values():
        #     for j in i:
        #         self.processSnv.append(j)
        #call(self.processSnv,  stdout=DEVNULL, stderr=DEVNULL)
        print("Varscan: Calling Variants Complete -> " + self.fileName)


    # Generate Directory
    def genDir(self):
        os.mkdir(self.resultDirectory + "VCF/varscan_output/")


    # Updates Dictionaries
    def bindInputs(self):

        # samtools User Specific Arguments
        self.samtoolsDictionary["bamFiles"][1] = "./input/normal_mode/" + self.normalBAM
        self.samtoolsDictionary["bamFiles"][2] = "./input/normal_mode/" + self.tumorBAM
        self.samtoolsDictionary["output"][1] = "./output/" + self.fileName + "/VCF/varscan_output/" + self.fileName + ".pileup"

        # varscan User Specific Arguments
        self.varscanSomaticDictionary["input|output"][0] = self.samtoolsDictionary["output"][1]
        self.varscanSomaticDictionary["input|output"][1] = "./output/" + self.fileName + "/VCF/varscan_output/" + self.fileName
        # processIndel
        self.processDictionary["output"][0] = "./output/" + self.fileName + "/VCF/varscan_output/" + self.fileName + ".indel.vcf"
        self.variantCallerOutput += self.processDictionary["output"][0]


