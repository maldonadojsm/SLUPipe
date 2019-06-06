from subprocess import call, DEVNULL


class Annotator:
    # Constructor
    def __init__(self, caller):
        self.variantCaller = caller
        self.AnnotateDict = {
            "Exe": ["vep"],
            "Input": ["-i", "input_filepath"],
            "Output": ["-o", "output_filepath"],
            "FormatFlags": ["--vcf", "--offline", "--force_overwrite"]
        }

        self.annotatorOutput = ""
        self.annotatorOutputSNV = ""
        self.fileName = ""
        self.callerID = ""
        self.fileHeader = self.variantCaller.fileHeader
        self.annotate = []
        self.annotateSNV = []
        self.bindInputs()

    def processAnnotation(self):
        print("Ensembl VEP: Annotating Variants -> " + self.fileName + "-" + self.callerID)
        for i in self.AnnotateDict.values():
            for j in i:
                self.annotate.append(j)
        call(self.annotate, stdout=DEVNULL, stderr=DEVNULL)
        # SNV VCF Files
        if self.variantCaller.variantCallerSnvOutput is not None:
            self.AnnotateDict["Input"][1] = self.variantCaller.variantCallerSnvOutput
            self.AnnotateDict[
                "Output"][1] = "./" + self.variantCaller.fileName + "/AnnotatedVCF/" + self.variantCaller.fileName + "_" + self.variantCaller.callerID + "snv" + ".annotated.vcf"
            self.annotatorOutputSNV = self.AnnotateDict["Output"][1]
            for i in self.AnnotateDict.values():
                for j in i:
                    self.annotateSNV.append(j)
            call(self.annotateSNV, stdout=DEVNULL, stderr=DEVNULL)
        print("Ensembl VEP: Annotating Variants Complete -> " + self.fileName + "-" + self.callerID)

    def bindInputs(self):

        self.AnnotateDict["Input"][1] = self.variantCaller.variantCallerOutput
        self.AnnotateDict["Output"][1] = "./output/" + self.variantCaller.fileName + "/AnnotatedVCF/" + self.variantCaller.fileName + "_" + self.variantCaller.callerID + ".annotated.vcf"
        self.annotatorOutput = self.AnnotateDict["Output"][1]
        self.fileName = self.variantCaller.fileName
        self.callerID = self.variantCaller.callerID

