import MuSE
import Mutect2
import Varscan
import Sniper
import sys
import Annotator
from subprocess import call, DEVNULL

class MAFCoverter:
    def __init__(self, annotatedInfo, vepScript, vepCache):
        self.annotatedObject = annotatedInfo
        self.vepScript = vepScript
        self.vepCache = vepCache
        self.conversionDict = {
            "Exe": ["vcf2maf.pl"],
            "Input": ["--input-vcf", "input_filepath"],
            "Output": ["--output-maf", "output_filepath"],
            "Reference": ["--ref-fasta", "./referenceFiles/Homo_sapiens_assembly38.fasta"],
            "VEPScript": ["--vep-path", "/student/maldonadojs/.conda/envs/SLUPipe/share/ensembl-vep-95.3-0"],
            "VEPCache": ["--vep-data", "/student/maldonadojs/.vep"],
            "Filter": ["--filter-vcf", "0"],
            "ncbiBuild": ["--ncbi-build", "GRCh38"]
        }

        self.mafOutput = ""
        self.mafSnvOutput = ""
        self.fileName = self.annotatedObject.fileName
        self.fileHeader = self.annotatedObject.fileHeader
        self.convert = []
        self.convertSNV = []
        self.bindInputs()

    def processConversion(self):
        print("VCF2MAF: Converting VCF to MAF -> " + self.fileName + "-" + self.annotatedObject.callerID)

        for i in self.conversionDict.values():
            for j in i:
                self.convert.append(j)
        call(self.convert, stdout=DEVNULL, stderr=DEVNULL)

        # SNV VCF Files
        if self.annotatedObject.annotatorOutputSNV is not None:
            self.conversionDict["Input"][1] = self.annotatedObject.annotatorOutputSNV
            self.conversionDict["Output"][1] = "./output/" + self.annotatedObject.fileName + "/MAF/" + self.annotatedObject.fileName + "_" + self.annotatedObject.callerID + "snv" + ".maf"
            self.mafSnvOutput = self.conversionDict["Output"][1]

            for i in self.conversionDict.values():
                for j in i:
                    self.convertSNV.append(j)
            call(self.convertSNV, stdout=DEVNULL, stderr=DEVNULL)

        print("VCF2MAF: VCF to MAF Conversion Complete -> " + self.fileName + "-" + self.annotatedObject.callerID)

    def bindInputs(self):
        # Update Input & Output File Paths
        self.conversionDict["Input"][1] = self.annotatedObject.annotatorOutput
        self.conversionDict["Output"][1] = "./output/" + self.annotatedObject.fileName + "/MAF/" + self.annotatedObject.fileName + "_" + self.annotatedObject.callerID + ".maf"
        self.mafOutput = self.conversionDict["Output"][1]

        # Bind VEP Cache and Script FilePath

        self.conversionDict["VEPScript"][1] = self.vepScript
        self.conversionDict["VEPCache"][1] = self.vepCache

