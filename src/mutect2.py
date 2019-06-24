# !/usr/bin/env python
# title           :mutect2.py
# description     :Mutect 2 Variant Caller Framework
# author          :Juan Maldonado
# date            :6/13/19
# version         :0.5
# usage           :
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.6.5
# conda_version   :4.6.14
# =================================================================================================================


from subprocess import call, DEVNULL
import os


class Mutect2:
    def __init__(self, normal_bam, tumor_bam, filename, result_directory, chromosome_range):
        """
        Class Constructor
        :param normal_bam: normal BAM file
        :param tumor_bam: tumor BAM file
        :param filename: Sample ID
        :param result_directory: Output file path
        :param chromosome_range: Chromosome Range indicated for analysis
        """
        self.normal_bam = normal_bam
        self.tumor_bam = tumor_bam
        self.filename = filename
        self.result_directory = result_directory
        self.chrome_range = chromosome_range
        self.mutect_dict = {
            "Exe": ["java", "-jar", "GenomeAnalysisTK.jar", "-T", "MuTect2"],
            "reference": ["-R", "./referenceFiles/Homo_sapiens_assembly38.fasta"],
            "tumor_bam": ["-I:tumor", "hcc1143_T_subset50K.bam"],
            "normal_bam": ["-I:normal", "hcc1143_N_subset50K.bam"],
            "normalPanel": ["--normal_panel", "./referenceFiles/1kg_40_m2pon_sitesonly_subset50k.vcf"],
            "DBSNP": ["--dbsnp", "./referenceFiles/dbSNP142_GRCh38_subset50k.vcf"],
            "threads": ["-nct", "25"],
            "chromosomeRange": ["-L", "chr6:33,413,000-118,315,000"],
            "output": ["-o", "./mutect2_output/"]

        }
        if normal_bam is None:
            self.adjust_tumor_only()
        self.file_header = "1i #Mutect2"
        self.mutect2 = []
        self.variant_caller_output = ""
        self.variant_caller_snv_output = None
        self.variant_caller_id = "mutect2"
        self.generate_dir()
        self.bind_inputs()

    def run_variant_caller(self):
        """
        Execute Variant Caller Workflow
        """
        for i in self.mutect_dict.values():
            for j in i:
                self.mutect2.append(j)
        print("MuTect2: Calling Variants -> " + self.filename)
        call(self.mutect2, stdout=DEVNULL, stderr=DEVNULL)
        print("Mutect2: Calling Variants Complete -> " + self.filename)

    def adjust_tumor_only(self):
        self.mutect_dict.pop('normal_bam', None)
        self.mutect_dict.pop('normalPanel', None)
        self.mutect_dict.pop('DBSNP', None)

    def generate_dir(self):
        """
        Generates Output Subdirectory to store VCF results
        """
        os.mkdir(self.result_directory + "vcf/mutect2_output/")

    def bind_inputs(self):
        """
        Update Dictionaries with relevant input needed to process workflow
        Update Output file paths needed to process Annotation Worflow
        """
        if self.normal_bam is None:
            self.mutect_dict["tumor_bam"][1] = "./input/tumor_mode/" + self.tumor_bam
        else:
            self.mutect_dict["tumor_bam"][1] = "./input/normal_mode/" + self.tumor_bam
            self.mutect_dict["normal_bam"][1] = "./input/normal_mode/" + self.normal_bam
        self.mutect_dict["output"][1] = "./output/" + self.filename + "/vcf/mutect2_output/" + self.filename + ".vcf"
        self.variant_caller_output += self.mutect_dict["output"][1]

        # Bind Chromosome Range

        self.mutect_dict["chromosomeRange"][1] = self.chrome_range


