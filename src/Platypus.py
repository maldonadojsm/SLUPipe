from subprocess import call, DEVNULL
import os


class Platypus:
    def __init__(self, tumorBAM, fileName, resultDirectory):
        self.tumorBAM = tumorBAM
        self.fileName = fileName
        self.resultDirectory = resultDirectory
        self.platypusDict = {
            "Exe": ["platypus", "callVariants"],
            "tumorBam": ["--bamFiles="],
            "reference": ["--refFile=../src/referenceFiles/Homo_sapiens_assembly38.fasta"],
            "output": ["--output="]
        }
        self.platypus = []
        self.fileHeader = "li #Platypus"
        self.callerID = "platypus"
        self.variantCallerOutput = ""
        self.variantCallerSnvOutput = None
        self.genDir()
        self.bindInputs()

    # Generate Directory
    def genDir(self):
        os.mkdir(self.resultDirectory + "VCF/platypus_output/")

    def runVariantCaller(self):
        for i in self.platypusDict.values():
            for j in i:
                self.platypus.append(j)

        print("Platypus: Calling Variants -> " + self.fileName)
        call(self.platypus, stdout=DEVNULL, stderr=DEVNULL)
        print("Platypus: Calling Variants Complete -> " + self.fileName)

    def bindInputs(self):
        self.platypusDict["tumorBam"][0] += "./input/tumor_mode/" + self.tumorBAM
        self.platypusDict["output"][0] += "./output/" + self.fileName + "/VCF/platypus_output/" + self.fileName + ".vcf"
        self.variantCallerOutput = "./output/" + self.fileName + "/VCF/platypus_output/" + self.fileName + ".vcf"

