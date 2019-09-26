# !/usr/bin/env python
# title           :maf_converter.py
# description     :Converts Annotated VCF files into MAF files
# author          :Juan Maldonado
# date            :6/13/19
# version         :0.5
# usage           :
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.6.5
# conda_version   :4.6.14
# =================================================================================================================

from subprocess import call, DEVNULL


class mafConverter:
    def __init__(self, annotated_vcf_obj, vep_script, vep_cache, output_dir, reference_dir):
        """
        Class Constructor
        :param annotated_vcf_obj: Annotator object storing relevant information to process VCF to MAF conversion
        :param vep_script: Ensembl VEP Script Path (Absolute)
        :param vep_cache: Ensembl VEP Cache Path (Absolute)
        """
        self.annotated_object = annotated_vcf_obj
        self.vep_script = vep_script
        self.vep_cache = vep_cache
        self.output_directory = output_dir
        self.reference_dir = reference_dir
        self.conversion_dict = {
            "Exe": ["vcf2maf.pl"],
            "Input": ["--input-vcf", "input_file_path"],
            "Output": ["--output-maf", "output_file_path"],
            "Reference": ["--ref-fasta", "./referenceFiles/Homo_sapiens_assembly38.fasta"],
            "VEPScript": ["--vep-path", "/student/maldonadojs/.conda/envs/SLUPipe/share/ensembl-vep-95.3-0"],
            "VEPCache": ["--vep-data", "/student/maldonadojs/.vep"],
            "Filter": ["--filter-vcf", "0"],
            "ncbiBuild": ["--ncbi-build", "GRCh38"]
        }
        #
        self.maf_output_file_path = ""
        self.maf_snv_output_file_path = ""
        self.filename = self.annotated_object.filename
        self.file_header = self.annotated_object.file_header
        self.convert = []
        self.convert_snv = []
        self.bind_inputs()

    def process_conversion(self):
        """
        Execute VCF to MAF Conversion Workflow
        """
        print("VCF2maf: Converting VCF to maf -> " + self.filename + "-" + self.annotated_object.variant_caller_id)

        for i in self.conversion_dict.values():
            for j in i:
                self.convert.append(j)
        call(self.convert, stdout=DEVNULL, stderr=DEVNULL)

        # SNV VCF Files
        if self.annotated_object.anno_output_snv_file_path is not None:
            self.conversion_dict["Input"][1] = self.annotated_object.anno_output_snv_file_path
            self.conversion_dict["Output"][1] = self.output_directory + self.annotated_object.filename + "/maf/" + self.annotated_object.filename + "." + self.annotated_object.variant_caller_id + "snv" + ".maf"
            self.maf_snv_output_file_path = self.conversion_dict["Output"][1]

            for i in self.conversion_dict.values():
                for j in i:
                    self.convert_snv.append(j)
            call(self.convert_snv, stdout=DEVNULL, stderr=DEVNULL)

        print("VCF2maf: VCF to maf Conversion Complete -> " + self.filename + "-" + self.annotated_object.variant_caller_id)

    def bind_inputs(self):
        """
        Updates Conversion Dictionary with relevant arguments needed for proper execution of VCF to MAF conversion.
        Updates Output Directory file path needed for MAF Merging.
        """
        # Update Input & Output File Paths
        self.conversion_dict["Input"][1] = self.annotated_object.anno_output_file_path
        self.conversion_dict["Output"][1] = self.output_directory + self.annotated_object.filename + "/maf/" + self.annotated_object.filename + "." + self.annotated_object.variant_caller_id + ".maf"
        self.maf_output_file_path = self.conversion_dict["Output"][1]

        # Bind VEP Cache and Script FilePath

        self.conversion_dict["VEPScript"][1] = self.vep_script
        self.conversion_dict["VEPCache"][1] = self.vep_cache

        # Bind Reference Directory

        self.conversion_dict["Reference"][1] = self.reference_dir + "Homo_sapiens_assembly38.fasta"
