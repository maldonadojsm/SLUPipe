# !/usr/bin/env python
# title           :Annotator.py
# description     :Annotates variants using Ensemble VEP
# author          :Juan Maldonado
# date            :6/13/19
# version         :0.4
# usage           :
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.6.5
# conda_version   :4.6.14
# =================================================================================================================


from subprocess import call, DEVNULL

class Annotator:
    def __init__(self, caller):
        """
        :param caller: imports variant caller object storing relevant information to process variant annotation.
        """
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
        """
        Executes Variant Annotation Workflow
        """
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
        """
        Updates Annotation Dictionary with relevant arguments for variant annotation.
        Updates Annotated VCF output directory & sample ID needed for MAF Conversion
        """
        self.AnnotateDict["Input"][1] = self.variantCaller.variantCallerOutput
        self.AnnotateDict["Output"][1] = "./output/" + self.variantCaller.fileName + "/AnnotatedVCF/" + self.variantCaller.fileName + "_" + self.variantCaller.callerID + ".annotated.vcf"
        self.annotatorOutput = self.AnnotateDict["Output"][1]
        self.fileName = self.variantCaller.fileName
        self.callerID = self.variantCaller.callerID

