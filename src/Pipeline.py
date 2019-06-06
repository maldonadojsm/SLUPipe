import Parallel
import MuSE
import Mutect2
import Varscan
import Sniper
import Annotator
import MAFConverter
import Pindel
import Platypus
import Strelka
import MAFMerger


class Pipeline:
    def __init__(self, userInputs, chromosomeRange, vepScript, vepCache):
        self.inputs = userInputs
        self.parallelProcesses = []
        self.workflowQueue = []
        self.museFlag = ""
        self.mutectFlag = ""
        self.varscanFlag = ""
        self.sniperFlag = ""
        self.strelkaFlag = ""
        self.pindelFlag = ""
        self.platypusFlag = ""
        self.vepScript = vepScript
        self.vepCache = vepCache
        self.chrome_range = chromosomeRange

        #############################################################

        # VARIANT CALLER PROCESSING CLUSTERS

        # MuSE
        self.clusterM = []
        # Mutect 2
        self.clusterT = []
        # Varscan
        self.clusterV = []
        # Somatic Sniper
        self.clusterS = []
        # Strelka 2
        self.strelka2 = []
        # Pindel
        self.clusterP = []
        # Platypus
        self.clusterY = []

        ############################################################

        # ANNOTATION PROCESSING CLUSTERS

        # Process N MuSE VCF File Annotations of N Samples in Parallel
        self.annotationClusterM = []
        # Process N Mutect 2 VCF File Annotations of N Samples in Parallel
        self.annotationClusterT = []
        # Process N Somatic Sniper VCF File Annotations of N Samples in Parallel
        self.annotationClusterS = []
        # Process N Varscan VCF File Annotations of N Samples in Parallel
        self.annotationClusterV = []
        # Process N Strelka 2 VCF File Annotations of N Samples in Parallel
        self.annotationClusterK = []
        # Process N Pindel VCF File Annotations of N Samples in Parallel
        self.annotationClusterP = []
        # Process N Platypus VCF File Annotations of N Samples in Parallel
        self.annotationClusterY = []

        ##########################################################

        # CONVERSION PROCESSING CLUSTERS

        # Process N VCF to MAF Conversion for N Annotated MuSE VCF File of N Samples in Parallel
        self.conversionClusterM = []
        # Process N VCF to MAF Conversion for N Annotated Mutect 2 VCF File of N Samples in Parallel
        self.conversionClusterT = []
        # Process N VCF to MAF Conversion for N Annotated Somatic Sniper VCF File of N Samples in Parallel
        self.conversionClusterS = []
        # Process N VCF to MAF Conversion for N Annotated Varscan VCF File of N Samples in Parallel
        self.conversionClusterV = []
        # Process N VCF to MAF Conversion for N Annotated Strelka 2 VCF File of N Samples in Parallel
        self.conversionClusterK = []
        # Process N VCF to MAF Conversion for N Annotated Pindel VCF File of N Samples in Parallel
        self.conversionClusterT = []
        # Process N VCF to MAF Conversion for N Annotated Platypus VCF File of N Samples in Parallel
        self.conversionClusterY = []
        # Process N VCF To MAF Conversion for N Annotated Pindel VCF of N Samples in Parallel
        self.conversionClusterP = []
    def runNormalMode(self, MuSE = None, MuTect = None, Varscan = None, SomaticSniper = None, Strelka = None):

        # Update Variant Caller Flags
        self.museFlag = MuSE
        self.mutectFlag = MuTect
        self.varscanFlag = Varscan
        self.sniperFlag = SomaticSniper
        self.strelkaFlag = Strelka

        self.buildClusters(1)
        self.parallelizeProcesses(1)
        for i in self.parallelProcesses:
            i.runInParallel()
        self.mergeMafs()
        return 0

    def runTumorMode(self, Pindel = None, Platypus = None, Mutect = None,):
        # Update Variant Caller Flags
        self.mutectFlag = Mutect
        self.pindelFlag = Pindel
        self.platypusFlag = Platypus

        self.buildClusters(0)
        self.parallelizeProcesses(0)
        for i in self.parallelProcesses:
            i.runInParallel()
        self.mergeMafs()
        return 0

    def buildClusters(self, flag):
        # TUMOR MODE
        if flag == 0:
            # Variant Callers
            for i in self.inputs:

                self.clusterP.append(Pindel.Pindel(i.tumorBAM, i.fileName, i.resultDirectory, self.chrome_range)) # WORKING

                self.clusterY.append(Platypus.Platypus(i.tumorBAM, i.fileName, i.resultDirectory)) # WORKING

                self.clusterT.append(Mutect2.Mutect2(None, i.tumorBAM, i.fileName, i.resultDirectory, self.chrome_range)) # WORKING
            # Annotations
            for i, j, k in zip(self.clusterP, self.clusterY, self.clusterT):
                self.annotationClusterP.append(Annotator.Annotator(i))
                self.annotationClusterY.append(Annotator.Annotator(j))
                self.annotationClusterT.append(Annotator.Annotator(k)) #
            # Conversions
            for i, j, k in zip(self.annotationClusterP, self.annotationClusterY, self.annotationClusterT):
                self.conversionClusterP.append(MAFConverter.MAFCoverter(i, self.vepScript, self.vepCache))
                self.conversionClusterY.append(MAFConverter.MAFCoverter(j, self.vepScript, self.vepCache))
                self.conversionClusterT.append(MAFConverter.MAFCoverter(k, self.vepScript, self.vepCache))

        # NORMAL MODE
        elif flag == 1:
            for i in self.inputs:

                self.clusterM.append(MuSE.MuSE(i.normalBAM, i.tumorBAM, i.fileName, i.resultDirectory, self.chrome_range))

                self.clusterT.append(Mutect2.Mutect2(i.normalBAM, i.tumorBAM, i.fileName, i.resultDirectory, self.chrome_range))

                self.clusterV.append(Varscan.Varscan(i.normalBAM, i.tumorBAM, i.fileName, i.resultDirectory))

                self.clusterS.append(Sniper.Sniper(i.normalBAM, i.tumorBAM, i.fileName, i.resultDirectory))

                self.strelka2.append(Strelka.Strelka(i.normalBAM, i.tumorBAM, i.fileName , i.resultDirectory))
            # Annotations
            for i, j, k, l, m in zip(self.clusterM, self.clusterT, self.clusterS, self.clusterV, self.strelka2):
                self.annotationClusterM.append(Annotator.Annotator(i)) # WORKING
                self.annotationClusterT.append(Annotator.Annotator(j)) #
                self.annotationClusterS.append(Annotator.Annotator(k))
                self.annotationClusterV.append(Annotator.Annotator(l))
                self.annotationClusterK.append(Annotator.Annotator(m))
            # Conversions
            for i, j, k, l, m in zip(self.annotationClusterM, self.annotationClusterT, self.annotationClusterS,
                                  self.annotationClusterV,self.annotationClusterK):
                self.conversionClusterM.append(MAFConverter.MAFCoverter(i, self.vepScript, self.vepCache))
                self.conversionClusterT.append(MAFConverter.MAFCoverter(j, self.vepScript, self.vepCache))
                self.conversionClusterS.append(MAFConverter.MAFCoverter(k, self.vepScript, self.vepCache))
                self.conversionClusterV.append(MAFConverter.MAFCoverter(l, self.vepScript, self.vepCache))
                self.conversionClusterK.append(MAFConverter.MAFCoverter(m, self.vepScript, self.vepCache))

    def parallelizeProcesses(self, flag):

        # Workflow Containers
        self.caller_workflowQueue = []
        self.anno_workflowQueue = []
        self.conv_workflowQueue = []

        #TUMOR MODE
        if flag == 0:
            # Build Workflow
            if self.pindelFlag == "Pindel":
                self.caller_workflowQueue.append(self.clusterP)
                self.anno_workflowQueue.append(self.annotationClusterP)
                self.conv_workflowQueue.append(self.conversionClusterP)

            if self.platypusFlag == "Platypus":
                self.caller_workflowQueue.append(self.clusterY)
                self.anno_workflowQueue.append(self.annotationClusterY)
                self.conv_workflowQueue.append(self.conversionClusterY)

            if self.mutectFlag == "MuTect":
                self.caller_workflowQueue.append(self.clusterT)
                self.anno_workflowQueue.append(self.annotationClusterT)
                self.conv_workflowQueue.append(self.conversionClusterT)

        # NORMAL MODE
        if flag == 1:
            # Build Workflow
            if self.museFlag == "MuSE":
                self.caller_workflowQueue.append(self.clusterM)
                self.anno_workflowQueue.append(self.annotationClusterM)
                self.conv_workflowQueue.append(self.conversionClusterM)

            if self.mutectFlag == "MuTect":
                self.caller_workflowQueue.append(self.clusterT)
                self.anno_workflowQueue.append(self.annotationClusterT)
                self.conv_workflowQueue.append(self.conversionClusterT)

            if self.sniperFlag == "Sniper":
                self.caller_workflowQueue.append(self.clusterS)
                self.anno_workflowQueue.append(self.annotationClusterS)
                self.conv_workflowQueue.append(self.conversionClusterS)

            if self.varscanFlag == "Varscan":
                self.caller_workflowQueue.append(self.clusterV)
                self.anno_workflowQueue.append(self.annotationClusterV)
                self.conv_workflowQueue.append(self.conversionClusterV)

            if self.strelkaFlag == "Strelka2":
                self.caller_workflowQueue.append(self.strelka2)
                self.anno_workflowQueue.append(self.annotationClusterK)
                self.conv_workflowQueue.append(self.conversionClusterK)

        # Variant Calling
        for i in self.caller_workflowQueue:
            process = Parallel.ParallelP(i)
            process.constructThreads(0)
            self.parallelProcesses.append(process)
        # Annotation
        for i in self.anno_workflowQueue:
            process = Parallel.ParallelP(i)
            process.constructThreads(1)
            self.parallelProcesses.append(process)
        # Conversion
        for i in self.conv_workflowQueue:
            process = Parallel.ParallelP(i)
            process.constructThreads(2)
            self.parallelProcesses.append(process)

    def mergeMafs(self):
        fileNames = []
        for i in self.inputs:
            fileNames.append(i.fileName)
        # remove duplicate filenames
        fileNames = list(dict.fromkeys(fileNames))
        for i in fileNames:
            MAFMerger.mergeMafs(i)



