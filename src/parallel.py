# !/usr/bin/env python
# title           :parallel.py
# description     :Parallelizes Variant Calling, Variant Annotation, MAF Conversion & Merging Workflow
# author          :Juan Maldonado
# date            :6/13/19
# version         :0.5
# usage           :
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.6.5
# conda_version   :4.6.14
# =================================================================================================================

import multiprocessing as mp


class ParallelP:
    def __init__(self, incoming_workflow):
        """

        :param incoming_workflow: Python List containing workflow objects (Variant Calling, Variant Annotation or
        MAF Conversion) which will be parallelized
        """
        self.incoming_workflow = incoming_workflow
        self.parallel_threads = []

    def construct_threads(self, flag):
        """
        Builds threads in accordance to flag value.
        :param flag: 0: Build threads for parallel execution of variant caller objects
                     1: Build threads for parallel execution of variant annotation
                     2: Build threads for parallel execution of MAF conversion
        """
        for i in self.incoming_workflow:
            self.parallel_threads.append(self.prepare_batch(i, flag))

    def capture_batch(self, incoming_workflow):
        """
        Captures new object workflow to be parallelized
        :param incoming_workflow: Python List containing workflow objects
        """
        self.incoming_workflow = incoming_workflow

    def prepare_batch(self, workflow_object, flag):
        """
        Indicates which method within object will be parallelized
        :param workflow_object: Workflow Object (Variant Calling, Variant Annotation, MAF Conversion)
        :param flag: 0: Build threads for parallel execution of variant caller objects
                     1: Build threads for parallel execution of variant annotation
                     2: Build threads for parallel execution of MAF conversion
        :return: An object whose processes run in parallel 
        """

        if flag == 0:
            m = mp.Process(target=workflow_object.run_variant_caller)
            return m

        elif flag == 1:
            m = mp.Process(target=workflow_object.process_annotation)
            return m

        # Conversions

        elif flag == 2:
            m = mp.Process(target=workflow_object.process_conversion)
            return m

    def run_in_parallel(self):
        """
        Start & Join Parallel Threads
        """
        for p in self.parallel_threads:
            p.start()
        for p in self.parallel_threads:
            p.join()













