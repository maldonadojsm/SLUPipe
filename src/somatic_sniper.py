# !/usr/bin/env python
# title           :somatic_sniper.py
# description     :Somatic Sniper variant caller framework
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


class Sniper:
    def __init__(self, normal_bam, tumor_bam, filename, result_directory):
        """
          Class Constructor
          :param tumor_bam: tumor BAM file
          :param normal_bam: normal BAM file
          :param filename: Sample ID
          :param result_directory: Output file path
          """
        self.normal_bam = normal_bam
        self.tumor_bam = tumor_bam
        self.filename = filename
        self.result_directory = result_directory

        self.sniper_dict = {
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
            "tumor_bam": ["hcc1143_T_subset50K.bam"],
            "normal_bam": ["hcc1143_N_subset50K.bam"],
            "output": ["./sniper_output/"]
        }
        self.file_header = "1i #SomaticSniper"
        self.sniper = []
        self.variant_caller_output = ""
        self.variant_caller_snv_output = None
        self.variant_caller_id = "sniper"
        self.generate_dir()
        self.bind_inputs()

    def run_variant_caller(self):
        """
        Execute Variant Caller Workflow
        """
        for i in self.sniper_dict.values():
            for j in i:
                self.sniper.append(j)

        print("Somatic Sniper: Calling Variants -> " + self.filename)
        call(self.sniper, stdout=DEVNULL, stderr=DEVNULL)
        print("Somatic Sniper: Calling Variants Complete -> " + self.filename)

    def generate_dir(self):
        """
        Generates Output Subdirectory to store VCF results
        """
        os.mkdir(self.result_directory + "vcf/somatic_sniper_output/")

    def bind_inputs(self):
        """
        Update Dictionaries with relevant input needed to process workflow
        Update Output file paths needed to process Annotation Worflow
        """
        self.sniper_dict["tumor_bam"][0] = "./input/" + self.tumor_bam
        self.sniper_dict["normal_bam"][0] = "./input/" + self.normal_bam
        self.sniper_dict["output"][0] = "./output/" + self.filename + "/vcf/somatic_sniper_output/" + self.filename + ".vcf"
        self.variant_caller_output += self.sniper_dict["output"][0]


