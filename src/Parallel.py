# !/usr/bin/env python
# title           :Parallel.py
# description     :Parallelizes Variant Calling, Variant Annotation, MAF Conversion & Merging Workflow
# author          :Juan Maldonado
# date            :6/13/19
# version         :0.4
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
        self.incomingBatch = incoming_workflow
        self.parallelThreads = []

    def constructThreads(self, flag):
        """
        Builds threads in accordance to flag value.
        :param flag: 0: Build threads for parallel execution of variant caller objects
                     1: Build threads for parallel execution of variant annotation
                     2: Build threads for parallel execution of MAF conversion
        """
        for i in self.incomingBatch:
            self.parallelThreads.append(self.prepareBatch(i, flag))

    def captureBatch(self, incoming_workflow):
        """
        Captures new object workflow to be parallelized
        :param incoming_workflow: Python List containing workflow objects
        """
        self.incomingBatch = incoming_workflow

    def prepareBatch(self, object, flag):
        """
        Indicates which method within object will be parallelized
        :param object: Workflow Object (Variant Calling, Variant Annotation, MAF Conversion)
        :param flag: 0: Build threads for parallel execution of variant caller objects
                     1: Build threads for parallel execution of variant annotation
                     2: Build threads for parallel execution of MAF conversion
        :return: Parallelized Object
        """

        if flag == 0:
            m = mp.Process(target=object.runVariantCaller)
            return m

        elif flag == 1:
            m = mp.Process(target=object.processAnnotation)
            return m

        # Conversions

        elif flag == 2:
            m = mp.Process(target=object.processConversion)
            return m

    def runInParallel(self):
        """
        Start & Join Parallel Threads
        """
        for p in self.parallelThreads:
            p.start()
        for p in self.parallelThreads:
            p.join()













