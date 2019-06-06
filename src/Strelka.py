from subprocess import call, DEVNULL
import os

class Strelka:
    # Constructor
    def __init__(self, normalBAM, tumorBAM, fileName, resultDirectory):
        self.normalBAM = normalBAM
        self.tumorBAM = tumorBAM
        self.fileName = fileName
        self.resultDirectory = resultDirectory

        # Strelka2 creates ./strelka2_output/runWorkflow.py, a config script based on input arguments
        self.strelkaConfigDictionary = {
            "Exe": ["python", "./configureStrelkaSomaticWorkflow.py"],
            "normalBam": ["--normalBam", "./hcc1143_N_subset50K.bam"],
            "tumorBam": ["--tumorBam", "./hcc1143_T_subset50K.bam"],
            "reference": ["--referenceFasta", "./referenceFiles/Homo_sapiens_assembly38.fasta"],
            "runDir": ["--runDir", "./VCF/strelka2_output"]
        }
        # Strelka2 runs the config python script with desired number of threads '-j num_threads'
        self.strelkaRunDictionary = {
            "runDir": ["python", "./strelka2_output/runWorkflow.py"],
            "localMachine": ["-m", "local"],
            "threads": ["-j", "8"]

        }

        self.fileHeader = "1i #Strelka2"
        self.strelkaConfig = []
        self.strelkaRun = []
        # Strelka2 sets up an entire directory each run, this path will be created
        self.runDir = "./output/" + self.fileName + "/VCF/strelka2_output"
        # List type signifies to Annotator.py to expect 2 VCFs, 1 snvs and 1 indels VCF file

        self.variantCallerOutput = "./output/" + self.fileName + "/VCF/strelka2_output/results/variants/somatic.indels.vcf"
        self.variantCallerSnvOutput = "./output/" + self.fileName + "/VCF/strelka2_output/results/variants/somatic.snvs.vcf"
        self.callerID = "strelka2"
        self.genDir()
        self.bindInputs()

    # Runs Strelka2 via BASH
    def runVariantCaller(self):
        for i in self.strelkaConfigDictionary.values():
            for j in i:
                self.strelkaConfig.append(j)
        for i in self.strelkaRunDictionary.values():
            for j in i:
                self.strelkaRun.append(j)
        print("Strelka 2: Calling Variants -> " + self.fileName)

        # Creating the Strelka2 temporary directory
        call(self.strelkaConfig, stdout=DEVNULL, stderr=DEVNULL)

        call(self.strelkaRun, stdout=DEVNULL, stderr=DEVNULL)
        call(["gunzip", self.runDir+"/results/variants/somatic.snvs.vcf.gz", self.runDir + "/results/variants/somatic.indels.vcf.gz"])

        # Moving VCF to permanent Strelka2 directory
        # call(["cp", self.runDir+"/results/variants/somatic.snvs.vcf", "./output/" + self.fileName + "/VCF/strelka2_output/" + self.fileName + ".somatic.snvs.vcf"])
        # call(["cp", self.runDir+"/results/variants/somatic.indels.vcf", "./output/" + self.fileName + "/VCF/strelka2_output/"+ self.fileName + ".somatic.indels.vcf"])
        print("Strelka 2: Calling Variants Complete -> " + self.fileName)


    # Generate Directory
    def genDir(self):
        os.mkdir(self.resultDirectory + "VCF/strelka2_output/")


    # Updates Dictionaries
    def bindInputs(self):
        # Strelka Call User Specific Arguments
        self.strelkaConfigDictionary["tumorBam"][1] = "./input/normal_mode/" + self.tumorBAM
        self.strelkaConfigDictionary["normalBam"][1] = "./input/normal_mode/" + self.normalBAM
        self.strelkaConfigDictionary["runDir"][1] = self.runDir
        self.strelkaRunDictionary["runDir"][1] = self.runDir+"/runWorkflow.py"
