from subprocess import call, DEVNULL
import os


class Pindel:
    def __init__(self, tumorBAM, fileName, resultDirectory, chromeRange):
        self.tumorBAM = tumorBAM
        self.fileName = fileName
        self.resultDirectory = resultDirectory
        self.chrome_range = chromeRange
        self.pindelReadDictionary = {
            "Exe": ["pindel"],
            "reference": ["-f", "./referenceFiles/Homo_sapiens_assembly38.fasta"],
            "configFile": ["-i", "config.txt"],
            "chromosomeRange": ["-c", "chr6:33,413,000-118,315,000"],
            "threads": ["-T", "8"],
            "output": ["-o", "./pindel_output/"]
        }
        self.pindelConvertDictionary = {
            "Exe ": ["pindel2vcf"],
            "input": ["-p", "./pindel_output/"],
            "reference": ["-r", "./referenceFiles/Homo_sapiens_assembly38.fasta"],
            "refName": ["-R", "Homo_Sapiens_Assembly38"],
            "refDate": ["-d", "20101123"],
            "output": ["-v", "./pindel_output/"]
        }
        self.fileHeader = "li #Pindel"
        self.pindelRead = []
        self.pindelConvert = []
        self.callerID = "pindel"
        self.variantCallerOutput = ""
        self.variantCallerSnvOutput = None
        self.configFile = "./pindel_output/"
        self.genDir()
        self.genConfigFile()
        self.bindInputs()

    # Generate Directory
    def genDir(self):
        os.mkdir(self.resultDirectory + "VCF/pindel_output/")

    def runVariantCaller(self):
        for i in self.pindelReadDictionary.values():
            for j in i:
                self.pindelRead.append(j)

        for i in self.pindelConvertDictionary.values():
            for j in i:
                self.pindelConvert.append(j)

        # EXTRACTING READS FROM BAM FILE
        print("Pindel: Calling Variants -> " + self.fileName)
        call(self.pindelRead, stdout=DEVNULL, stderr=DEVNULL)
        # CONVERT TO VCF
        call(self.pindelConvert, stdout=DEVNULL, stderr=DEVNULL)
        print("Pindel: Calling Variants Complete -> " + self.fileName)

    def genConfigFile(self):
        self.configFile = "./output/" + self.fileName + "/VCF/pindel_output/" + self.fileName + "_config.txt"
        # Forums say it varies from 300-400..
        insertSize = 350
        parameters = "./input/tumor_mode/"+self.tumorBAM + " " + str(insertSize) + " " + self.fileName

        file = open(self.configFile, "w+")
        file.write(parameters)
        file.close()

    def bindInputs(self):
        # Pindel Read
        self.pindelReadDictionary["configFile"][1] = self.configFile
        self.pindelReadDictionary["output"][1] = "./output/" + self.fileName + "/VCF/pindel_output/" + self.fileName

        # Pindel2VCF
        self.pindelConvertDictionary["input"][1] = "./output/" + self.fileName + "/VCF/pindel_output/" + self.fileName + "_D"
        self.pindelConvertDictionary["output"][1] = "./output/" + self.fileName + "/VCF/pindel_output/" + self.fileName + ".vcf"
        self.variantCallerOutput += self.pindelConvertDictionary["output"][1]

        # Bind Chromosome Range

        self.pindelReadDictionary["chromosomeRange"][1] = self.chrome_range


