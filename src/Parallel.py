import MuSE
import Mutect2
import Varscan
import Sniper
import sys
import multiprocessing as mp

class ParallelP:

    # Constructor
    def __init__(self, incomingClusterQueue):
        self.incomingBatch = incomingClusterQueue
        self.parallelThreads = []

    def constructThreads(self, flag):
        for i in self.incomingBatch:
            self.parallelThreads.append(self.prepareBatch(i, flag))

    def captureBatch(self, incomingCluster):
        self.incomingBatch = incomingCluster

    def prepareBatch(self, Object, flag):
        # Variant Callers
        if flag == 0:
            m = mp.Process(target=Object.runVariantCaller)
            return m

        # Annotations
        elif flag == 1:
            m = mp.Process(target=Object.processAnnotation)
            return m

        # Conversions

        elif flag == 2:
            m = mp.Process(target=Object.processConversion)
            return m



        # Mergers

    def runInParallel(self):
        for p in self.parallelThreads:
            p.start()
        for p in self.parallelThreads:
            p.join()
            # Exit Completed Processes












