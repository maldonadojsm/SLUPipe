# !/usr/bin/env python
# title           :annotator.py
# description     :Annotates variants using Ensemble VEP
# author          :Juan Maldonado
# date            :6/13/19
# version         :0.1
# usage           :
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.6.5
# conda_version   :4.6.14
# =================================================================================================================

from subprocess import call, DEVNULL


class Annotator:
    def __init__(self, variant_caller):
        """
        :param caller: imports variant caller object storing relevant information to process variant annotation.
        """
        self.variant_caller_obj = variant_caller
        self.annotator_dict = {
            "Exe": ["vep"],
            "Input": ["-i", "input_file_path"],
            "Output": ["-o", "output_file_path"],
            "FormatFlags": ["--vcf", "--offline", "--force_overwrite"]
        }

        self.anno_output_file_path = ""
        self.anno_output_snv_file_path = ""
        self.filename = ""
        self.variant_caller_id = ""
        self.file_header = self.variant_caller_obj.file_header
        self.annotate = []
        self.annotate_snv = []
        self.bind_inputs()

    def process_annotation(self):
        """
        Executes Variant Annotation Workflow
        """
        print("Ensembl VEP: Annotating Variants -> " + self.filename + "-" + self.variant_caller_id)
        for i in self.annotator_dict.values():
            for j in i:
                self.annotate.append(j)
        call(self.annotate, stdout=DEVNULL, stderr=DEVNULL)
        # SNV VCF Files
        if self.variant_caller_obj.variant_caller_snv_output is not None:
            self.annotator_dict["Input"][1] = self.variant_caller_obj.variant_caller_snv_output
            self.annotator_dict[
                "Output"][1] = "./" + self.variant_caller_obj.filename + "/annotated_vcf/" + self.variant_caller_obj.filename + "_" + self.variant_caller_obj.variant_caller_id + "snv" + ".annotated.vcf"
            self.anno_output_snv_file_path = self.annotator_dict["Output"][1]
            for i in self.annotator_dict.values():
                for j in i:
                    self.annotate_snv.append(j)
            call(self.annotate_snv, stdout=DEVNULL, stderr=DEVNULL)
        print("Ensembl VEP: Annotating Variants Complete -> " + self.filename + "-" + self.variant_caller_id)

    def bind_inputs(self):
        """
        Updates Annotation Dictionary with relevant arguments for variant annotation.
        Updates Annotated VCF output directory & sample ID needed for MAF Conversion
        """
        self.annotator_dict["Input"][1] = self.variant_caller_obj.variant_caller_output
        self.annotator_dict["Output"][1] = "./output/" + self.variant_caller_obj.filename + "/annotated_vcf/" + self.variant_caller_obj.filename + "_" + self.variant_caller_obj.variant_caller_id + ".annotated.vcf"
        self.anno_output_file_path = self.annotator_dict["Output"][1]
        self.filename = self.variant_caller_obj.filename
        self.variant_caller_id = self.variant_caller_obj.variant_caller_id

