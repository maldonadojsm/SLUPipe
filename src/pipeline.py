# !/usr/bin/env python
# title           :pipeline.py
# description     :Processes and executes SLUPipe workflow
# author          :Juan Maldonado
# date            :6/13/19
# version         :0.5
# usage           :SEE slupipe.py
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.6.5
# conda_version   :4.6.14
# =================================================================================================================

import parallel as pl
import muse as ms
import mutect2 as mt
import varscan as vs
import somatic_sniper as sp
import annotator as an
import maf_converter as mc
import pindel as pd
import platypus as py
import strelka as sl
import maf_merger as mf


class Pipeline:
    def __init__(self, user_samples, chromosome_range, vep_script_path, vep_cache_path, pipeline_mode, variant_callers):
        self.parallel_workflow = []
        self.master_workflow = []
        self.num_variants = len(variant_callers)
        self.variant_annotation_workflow = [list() for i in range(self.num_variants)]
        self.maf_conversion_workflow = [list() for i in range(self.num_variants)]
        self.variant_caller_workflow = []
        self.user_samples = user_samples
        self.vep_script_path = vep_script_path
        self.vep_cache_path = vep_cache_path
        self.chrome_range = chromosome_range
        if pipeline_mode == "-T":
            self.pipeline_mode = 0
        if pipeline_mode == "-N":
            self.pipeline_mode = 1
        self.pindel_flag = 0
        self.platypus_flag = 0
        self.mutect_flag = 0
        self.muse_flag = 0
        self.varscan_flag = 0
        self.sniper_flag = 0
        self.strelka_flag = 0
        self.set_variant_caller_flags(variant_callers)


        #############################################################

        # VARIANT CALLER PROCESSING CLUSTERS

        # muse
        self.muse = []
        # Mutect 2
        self.mutect = []
        # varscan
        self.varscan = []
        # Somatic sniper
        self.sniper = []
        # Strelka 2
        self.strelka2 = []
        # Pindel
        self.pindel = []
        # Platypus
        self.platypus = []

    def set_variant_caller_flags(self, variant_callers):
        """
        Sets variant callers which will be used for analysis (based on user config.json)
        :param variant_callers: Python list containing variant callers specified in config file
        """
        if "Muse" in variant_callers:
            self.muse_flag = 1
        if "Mutect" in variant_callers:
            self.mutect_flag = 1
        if "Varscan" in variant_callers:
            self.varscan_flag = 1
        if "Sniper" in variant_callers:
            self.sniper_flag = 1
        if "Strelka2" in variant_callers:
            self.strelka_flag = 1
        if "Pindel" in variant_callers:
            self.pindel_flag = 1
        if "Platypus" in variant_callers:
            self.platypus_flag = 1

    def run_workflow(self):
        """
        Builds & Executes SLUPipe Workflow
        :return: 0 = Process Complete
        """
        self.build_workflow(self.pipeline_mode)
        self.parallelize_processes()
        for i in self.parallel_workflow:
            i.run_in_parallel()
        self.merge_maf()
        return 0

    def build_workflow(self, flag):
        """
        Constructs SLUPipe workflow based on which mode the user has selected (Non-paired vs Paired)
        Builds Variant Caller objects based on the state of variant caller flags (1 = Variant Caller Enabled / 0 = 
        Variant Caller Disabled)
        :param flag: 0: Non-paired mode workflow / 1: Paired mode workflow
        """
        # TUMOR MODE
        if flag == 0:

            # Variant Callers

            for j in self.user_samples:

                if self.pindel_flag == 1:
                    self.pindel.append(pd.Pindel(j.tumor_bam, j.filename, j.results_directory, self.chrome_range))

                if self.platypus_flag == 1:
                    self.platypus.append(py.Platypus(j.tumor_bam, j.filename, j.results_directory))

                if self.mutect_flag == 1:
                    self.mutect.append(mt.Mutect2(None, j.tumor_bam, j.filename, j.results_directory, self.chrome_range))

            # Add variant caller objects into variant caller workflow list
            
            if self.pindel:
                self.variant_caller_workflow.append(self.pindel)

            if self.platypus:
                self.variant_caller_workflow.append(self.platypus)

            if self.mutect:
                self.variant_caller_workflow.append(self.mutect)
                
            self.master_workflow.append(self.variant_caller_workflow)

        # NORMAL MODE
        elif flag == 1:
            for i in self.user_samples:
                
                if self.muse_flag == 1:
                    self.muse.append(ms.Muse(i.normal_bam, i.tumor_bam, i.filename, i.results_directory, self.chrome_range))
                    
                if self.mutect_flag == 1:
                    self.mutect.append(mt.Mutect2(i.normal_bam, i.tumor_bam, i.filename, i.results_directory, self.chrome_range))
                    
                if self.varscan_flag:
                    self.varscan.append(vs.Varscan(i.normal_bam, i.tumor_bam, i.filename, i.results_directory))
                    
                if self.sniper_flag == 1:
                    self.sniper.append(sp.sniper(i.normal_bam, i.tumor_bam, i.filename, i.results_directory))
                    
                if self.strelka_flag == 1:
                    self.strelka2.append(sl.Strelka(i.normal_bam, i.tumor_bam, i.filename, i.results_directory))

            # Add variant caller objects into variant caller workflow list

            if self.muse:
                self.variant_caller_workflow.append(self.muse)

            if self.mutect:
                self.variant_caller_workflow.append(self.mutect)

            if self.varscan:
                self.variant_caller_workflow.append(self.varscan)

            if self.sniper:
                self.variant_caller_workflow.append(self.sniper)

            if self.strelka2:
                self.variant_caller_workflow.append(self.strelka2)

            self.master_workflow.append(self.variant_caller_workflow)

        # Build Variant Annotation Objects
        for i in range(len(self.variant_annotation_workflow)):
            for j in range(len(self.variant_caller_workflow[i])):
                self.variant_annotation_workflow[i].append(an.Annotator(self.variant_caller_workflow[i][j]))

        self.master_workflow.append(self.variant_annotation_workflow)

        # Build Conversion Objects
        for i in range(len(self.maf_conversion_workflow)):
            for j in range(len(self.variant_annotation_workflow[i])):
                self.maf_conversion_workflow[i].append(mc.mafConverter(self.variant_annotation_workflow[i][j], self.vep_script_path, self.vep_cache_path))

        self.master_workflow.append(self.maf_conversion_workflow)
               
    def parallelize_processes(self):
        """
        parallelizes workflow generated from build_workflow method. 
        """
        for i in range(len(self.master_workflow)):
            for j in self.master_workflow[i]:
                parallel_process = pl.ParallelP(j)
                parallel_process.construct_threads(i)
                self.parallel_workflow.append(parallel_process)
                
    def merge_maf(self):
        """
        Consolidates all generated maf files into a final.maf file
        """
        filenames = []
        for i in self.user_samples:
            filenames.append(i.filename)
        # remove duplicate filenames
        filenames = list(dict.fromkeys(filenames))
        for i in filenames:
            mf.merge_maf(i)


