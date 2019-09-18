<p align="center">
<img src=https://github.com/BioHPC/SLUPipe/blob/master/src/misc/slupipe.png width="250" height="250"/>
</p>

# SLUPipe: A (S)omatic Ana(L)ysis (U)mbrella (Pipe)line 

## Table of Contents
 + [Description](#description)
 + [Features](#features)
 + [Requirements](#requirements)
 + [Express Installation - Anaconda](#express-installation---anaconda)
 + [Installation - Anaconda](#installation-anaconda)
 + [Usage - Anaconda](#usage---anaconda)
 + [Usage - Sample Entry/Output](#usage---sample-entryoutput)
 + [Usage - JSON file Configuration](#usage---json-file-configuration)
 + [Usage - Example Workflow](#usage---example-workflow)
 + [Usage - SLUPipe Configuration for High Performance Computing - SLURM](#usage---slupipe-configuration-for-high-performance-computing---slurm)
 
 
## Description

SLUPipe is a DNA Sequencing Variant Calling Pipeline based on the National Cancer Institute's GDC guidelines. SLUPipe focuses towards automating, merging and parallelizing the following GDC's DNA-Sequence Analysis workflows to increase sample analysis throughput :

- Somatic Variant Calling
- Variant Annotation
- Aggregated Somatic Mutation

For further information on GDC Guidelines visit: https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/DNA_Seq_Variant_Calling_Pipeline/


## Features

SLUPipe provides variant calling for paired (Normal & Tumor) and non-paired (Tumor Only) aligned samples at the request of the research group:

### Variant Callers

**Paired Sample Variant Callers (Normal Mode):**
- MuSE (1.0.rc)
- Mutect2 (GATK3.8.1)
- Somatic Sniper (1.0.5.0)
- Varscan (2.4.3.2)
- Strelka 2 (2.9.10)

**Non-paired Sample Variant Callers (Tumor Only):**
- Pindel (0.2.5b9)
- Platypus (1.0.3)
- Mutect2

Variants callers can be toggled on/off as requested by the user (config file). 

### Variant Annotation

Raw VCF files are annotated using Ensembl VEP (v95). The following databases are used for VCF Annotation:

- GENCODE v.22
- sift v.5.2.2
- ESP v.20141103
- polyphen v.2.2.2
- dbSNP v.146
- Ensembl genebuild v.2014-07
- Ensembl regbuild v.13.0
- HGMD public v.20154
- ClinVar v.201601

## Requirements 
**Requirements:**

**Python 3+**

**Pandas**

**Glob**

**Linux Compatible Computer**

**CPU Processors with AVX Instruction Support**

## Express Installation - Anaconda 

For convenience, SLUPipe has been configured to run in Anaconda Environments

**1. Clone Github Repository**
```console
$ git clone https://github.com/BioHPC/SLUPipe.git
```
**2. Download & Install Anacaonda 4.5+**

https://www.anaconda.com/distribution/

**3. Automate creation of Anaconda environment.**
```console
$ cd SLUPipe
$ conda env create -f environment.yml (environment.yml can be found in SLUPipe root directory)
```
**IMPORTANT :** $SLUIPipePATH is your current working directory (user can check this by typing "pwd" in terminal)

**Please Note:** Environment creation will take around 30-45 minutes to complete.

**4. Configure Ensembl VEP For Variant Annotation & MAF Conversion (Local Cache Installation):**
   Create .vep directory at your home directory ($HOME) to store offline cache. 
   1. $ cd ~ (Takes you to your home directory. You can also use cd $HOME as well)
   2. $ mkdir .vep
   3. $ cd .vep
   3. $ curl -O -C - ftp://ftp.ensembl.org/pub/release-95/variation/indexed_vep_cache/homo_sapiens_vep_95_GRCh38.tar.gz
   4. $ tar xzf homo_sapiens_vep_96_GRCh38.tar.gz
   
**Please Note:** Download time will vary depending on time of day (1 Hr+)
   
**5. Copying Strelka 2 Configuration File to SLUPipe Working Directory:**
   1. Locate "configureStrelkaSomaticWorkflow.py" found in conda env bin directory (~/.conda/envs/SLUPipe/bin)
   2. Copy file into SLUPipe working directory ($SLUPipe/src)
   
   ``` console
   $ cp ~/.conda/envs/SLUPipe/bin/configureStrelkaSomaticWorkflow.py $SLUPipe/src
   ```
   
   
**Tip:** If unable to locate ./conda/envs/SLUPipe/bin directory, please run the following two commands to locate path:
```
$ source activate SLUPipe (start SLUPipe environment)
$ which python (prints full path related to SLUPipe conda environment)
```
## Installation - Anaconda 
**1. Clone Github Repository**
```console
$ git clone https://github.com/BioHPC/SLUPipe.git
```
**2. Download & Install Anacaonda 4.5+**

https://www.anaconda.com/distribution/

**3.A Create an Anaconda Environment**
```console
$ conda create -n SLUPipe 
```
**4. Activate the Anaconda Environment:**
```console
$ source activate SLUPipe
```
**5. The SLUPipe will require the following Python packages for it to be functionable**

**biobambam-2.0.87**
```console
$ conda install -c bioconda biobambam 
```
**bwa.kit-0.7.15**
```console
$ conda install -c bioconda bwakit 
```
**ensembl-vep 95.3**
``` console
$ conda install -c bioconda ensembl-vep=95.3 
```
**GenomeAnalysisTK-3.8.0**
``` console
$ conda install -c bioconda gatk
```
**MuSE 1.0.rc**
``` console
$ conda install -c bioconda muse 
```
**pandas 0.24.2**
``` console
$ conda install -c anaconda pandas 
```
**pindel-0.2.5b9**
``` console
$ conda install -c bioconda pindel 
```
**platypus-opt 1.0.3**
``` console
$ conda install -c bioconda platypus-variant 
```
**psycopg2 - 2.7.6.1**
``` console
$ conda install -c anaconda psycopg2 
```
**samtools-1.9**
``` console 
$ conda install -c bioconda samtools
```
**strelka 2.9.10**
``` console
$ conda install -c bioconda strelka 
```
**somatic-sniper 1.0.5.0**
``` console
$ conda install -c bioconda somatic-sniper 
```
**varscan - 2.4.3.2**
``` console
$ conda install -c bioconda varscan 
```
**vcf2maf - 1.6.16**
``` console
$ conda install -c bioconda vcf2maf
```
**6. Configuring Ensembl VEP For Variant Annotation & MAF Conversion (Local Cache Installation):**
   1. Create .vep directory to store offline cache: mkdir ~/.vep
   2. $ cd $HOME/.vep
   3. $ curl -O -C - ftp://ftp.ensembl.org/pub/release-95/variation/indexed_vep_cache/homo_sapiens_vep_95_GRCh38.tar.gz
   4. $ tar xzf homo_sapiens_vep_96_GRCh38.tar.gz
  
**Please Note:** Download time will vary depending on time of day (1 Hr+)
   
**7. Copying Strelka 2 Configuration File to SLUPipe Working Directory:**
   1. Locate "configureStrelkaSomaticWorkflow.py" found in SLUPipe conda env bin directory (~/.conda/envs/SLUPipe/bin)
   2. Copy file into SLUPipe working directory ($SLUPipe/src)
   
   ``` console
   $ cp ~/.conda/envs/SLUPipe/bin/configureStrelkaSomaticWorkflow.py $SLUPipe/src
   ```
   
   
   **Please Note:** $SLUIPipePATH is your current working directory (user can check this by typing "pwd" in terminal)
   
**Tip:** If unable to locate ./conda/envs/SLUPipe/bin directory, please run the following two commands to locate path:
```
$ source activate SLUPipe (start SLUPipe environment)
$ which python (prints full path related to SLUPipe conda environment)
```

## Usage - Anaconda  

**Activate Anaconda Environment**
``` console
$ source activate SLUPipe
```
**Execute Pipeline Workflow**
```console
$ python3 slupipe.py <config.json>
```

**Version Summary & Execution Description**
```console
$ python3 slupipe.py 
```
**Check Latest Software Release**
```console
$ python3 slupipe.py --update
```
## Usage - Sample Entry/Output 

SLUPipe processes and stores results using the following directories found within SLUPipe/src/:

**Reference Files (referenceFiles):** Place reference .fasta, .fai, dnSNP, normal panels files within this directory. 

Reference Files Needed:

**GATK Tutorial Data 9183 Somatic Variants: https://drive.google.com/drive/folders/1QdtVEronIzs04L37BFkw29TLjNWcyOpf**

1. 1kg_40_m2pon_sitesonly_subset50k.vcf            
2. 1kg_40_m2pon_sitesonly_subset50k.vcf.gz 
3. 1kg_40_m2pon_sitesonly_subset50k.vcf.idx 
4. 1kg_40_m2pon_sitesonly_subset50k.vcf.gz.tbi 
5. dbSNP142_GRCh38_subset50k.vcf.gz 
6. dbSNP142_GRCh38_subset50k.vcf            
7. dbSNP142_GRCh38_subset50k.vcf.idx 
8. dbSNP142_GRCh38_subset50k.vcf.gz.tbi   

**GATK Resource Bundle: https://software.broadinstitute.org/gatk/download/bundle**
   
9. Homo_sapiens_assembly38.dict         
10. Homo_sapiens_assembly38.fasta.index 
11. Homo_sapiens_assembly38.fasta.fai 
12. Homo_sapiens_assembly38.fasta 


**Input Files (Input):**  Place all .bam files to be processed in here (SLUPipe will automate generation of .bai files within this directory). Sample files for testing can be found here: https://drive.google.com/drive/folders/1QdtVEronIzs04L37BFkw29TLjNWcyOpf

Sample Files:

**GATK Tutorial Data 9183 Somatic Variants: https://drive.google.com/drive/folders/1QdtVEronIzs04L37BFkw29TLjNWcyOpf**

1. hcc1143_T_subset50K.bam
2. hcc1143_T_subset50K.bai
3. hcc1143_N_subset50K.bam
4. hcc1143_N_subset50K.bai

**Output Files (Output):**  SLUPipe workflow results will be placed here. Each sample result will have its files organized with the following directory structure:

    -Sample_1:
        ->annotated_vcfs:
            ->mutect_output
                -sample_1_muse.annotated.vcf
            ->strelka_output
                -sample_1_strelka.annotated.vcf
        ->mafs:
            -sample_1_muse.maf
            -sample_1_strelka.maf
        ->vcfs
            ->mutect_output
                -sample_1.vcf
            ->strelka_output
                -sample_1.vcf
                
**Important:** Users have completely liberty of creating more reference/input/output directories outside of those described here as long as they're specified in the JSON Configuration file.

## Usage - JSON file configuration

Users are able to customize SLUPipe workflows to their needs via JSON configuration files. **ALL** config files must be constructed with the following structure: 

**Configuration File Structure Format (JSON)**:

    [
      {
        "Pipeline_Mode":"-T",
        "Variant_Callers":["Pindel","Platypus"],
        "Input_Directory":"/student/foo/SLUPipe/src/input",
        "Output_Directory":"student/foo/SLUPipe/src/output",
        "Chromosome_Range": "chr1:16,000,000-215,000,000",
        "vep_ScriptPath": "/student/foo/.conda/envs/SLUPipe/share/ensembl-vep-95.3-0",
        "vep_CachePath": "/student/foo/.vep",
        "reference_directory": "/student/foo/referenceFiles",
        "cpuCores": "8"
      }
    ]
    
**Pipeline Mode & Variant Callers are indicated in the JSON file as followed:**

    Non-paired Mode (Tumor Only) = "-T"
    
    Paired Mode (Normal Mode) = "-N"
    
    MuSE = "Muse"
    MuTect2 = "Mutect"
    Varscan = "Varscan"
    Somatic Sniper = "Sniper"
    Strelka 2 = "Strelka2"
    Pindel = "Pindel"
    Platypus "Platypus"

    

## Usage - Example Workflow

**Pipeline Workflow Example (Non-paired Mode):**

    (SLUPipe)$ python3 slupipe.py config.json
    TUMOR MODE: DIRECTORY SUMMARY (X to Exit):
    --------------------------------------------------------------------------------
    NO.               ID               TUMOR
    --------------------------------------------------------------------------------
    1             tumor2_T         tumor2_T.bam
    2             tumor1_T         tumor1_T.bam
    
    IS THIS CORRECT (Y/N): Y
    SELECT FILE NUMBERS TO PROCESS (Separate File Numbers By Space): 1
    
    ############################
    COMMENCING PIPELINE WORKFLOW
    ############################
    
    Pindel: Calling Variants -> tumor2_T
    Pindel: Calling Variants Complete -> tumor2_T
    Platypus: Calling Variants -> tumor2_T
    Platypus: Calling Variants Complete -> tumor2_T
    MuTect2: Calling Variants -> tumor2_T
    Mutect2: Calling Variants Complete -> tumor2_T
    Ensembl VEP: Annotating Variants -> tumor2_T-pindel
    Ensembl VEP: Annotating Variants Complete -> tumor2_T-pindel
    Ensembl VEP: Annotating Variants -> tumor2_T-platypus
    Ensembl VEP: Annotating Variants Complete -> tumor2_T-platypus
    Ensembl VEP: Annotating Variants -> tumor2_T-mutect2
    Ensembl VEP: Annotating Variants Complete -> tumor2_T-mutect2
    VCF2MAF: Converting VCF to MAF -> tumor2_T-pindel
    VCF2MAF: VCF to MAF Conversion Complete -> tumor2_T-pindel
    VCF2MAF: Converting VCF to MAF -> tumor2_T-platypus
    VCF2MAF: VCF to MAF Conversion Complete -> tumor2_T-platypus
    VCF2MAF: Converting VCF to MAF -> tumor2_T-mutect2
    VCF2MAF: VCF to MAF Conversion Complete -> tumor2_T-mutect2
    Merging MAF: Saving Merged MAFs -> ./output/maf/tumor2_T.final.maf
    
    ---------------------- MERGED MAF SUMMARY ---------------------------
    
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1619 entries, 0 to 1618
    Columns: 134 entries, Hugo_Symbol to variant_caller
    dtypes: float64(70), int64(5), object(59)
    memory usage: 1.7+ MB
    None
    count     1619
    unique       1
    top        maf
    freq      1619
    Name: variant_caller, dtype: object
    
    ---------------------------------------------------------------------
    
    ############################
     PIPELINE WORKFLOW COMPLETE
    ############################
    
    
    
**Pipeline Workflow Result (Non-paired Mode MAF File):**
    
    GNU nano 2.3.1                                                     File: tumor2_T.final.maf                                                                                                                 

    Hugo_Symbol     Entrez_Gene_Id  Center  NCBI_Build	Chromosome	Start_Position  End_Position    Strand  Variant_Classification  Variant_Type    Reference_Allele        Tumor_Seq_Allele1	Tumor_Seq_Allele2	dbSNP_RS        dbSNP_Val_Status        Tumor_Sample_Barcode    Matched_Norm_Sample_Barcode     Match_Norm_Seq_Allele1  Match_Norm_Seq_Allele2  Tumor_Validation_Allele1        Tumor_Validation_Allele2        Match_Norm_Validation_Allele1   Match_Norm_Validation_Allele2   Verification_Status     Validation_Status	Mutation_Status Sequencing_Phase        Sequence_Source Validation_Method	Score   BAM_File        Sequencer	Tumor_Sample_UUID	Matched_Norm_Sample_UUID        HGVSc   HGVSp   HGVSp_Short     Transcript_ID   Exon_Number     t_depth t_ref_count     t_alt_count     n_depth n_ref_count     n_alt_count     all_effects     Allele  Gene    Feature Feature_type    Consequence     cDNA_position   CDS_position    Protein_position        Amino_acids     Codons  Existing_variation	ALLELE_NUM	DISTANCE        STRAND_VEP	SYMBOL  SYMBOL_SOURCE   HGNC_ID BIOTYPE CANONICAL	CCDS    ENSP    SWISSPROT	TREMBL  UNIPARC RefSeq  SIFT    PolyPhen        EXON    INTRON  DOMAINS AF	AFR_AF  AMR_AF  ASN_AF  EAS_AF  EUR_AF  SAS_AF  AA_AF   EA_AF   CLIN_SIG        SOMATIC PUBMED  MOTIF_NAME	MOTIF_POS	HIGH_INF_POS    MOTIF_SCORE_CHANGE	IMPAC$
    FAM131C 0	.	GRCh38  chr1    16063558        16063558        +	Missense_Mutation	SNP     C	C	T	rs755896471             TUMOR   NORMAL  C	C                                                                                                                               c.101G>A        p.Arg34His	p.R34H  ENST00000375662 2/7     42	38	4	50	50	0	FAM131C,missense_variant,p.Arg34His,ENST00000375662,NM_182623.2;FAM131C,intron_variant,,ENST00000494078,;	T	ENSG00000185519 ENST00000375662 Transcript	missense_variant        285/1695        101/843 34/280  R/H     cGc/cAc rs755896471,COSM6378897 1               -1	FAM131C HGNC    HGNC:26717	protein_coding  YES     CCDS41270.1     ENSP00000364814 Q96AQ9          UPI000022B016   NM_182623.2     tolerated(1)    benign(0)	2/7             hmmpanther:PTHR15736:SF2,hmmpanther:PTHR15736                                                                                   0,1                                             MODERATE        1	SNV     1               0,1                                                                                     Tier5   GCG     .	.                                                                                               2.442e-05               2.979e-05               5.806e-05                               0.00013000000$
    MRPS15  0	.	GRCh38  chr1    36455626        36455626        +	3'Flank SNP     A	A	G	rs2275479               TUMOR   NORMAL  A	A                                                                                                                                                       ENST00000373116         13	11	2	13	13	0	MRPS15,downstream_gene_variant,,ENST00000373116,NM_031280.3;MRPS15,downstream_gene_variant,,ENST00000462067,;MRPS15,downstream_gene_variant,,ENST00000477040,;MRPS15,downstream_gene_variant,,ENST00000488606,; G	ENSG00000116898 ENST00000373116 Transcript	downstream_gene_variant                                         rs2275479	1	92.0    -1	MRPS15  HGNC    HGNC:14504	protein_coding  YES     CCDS411.1	ENSP00000362208 P82914          UPI0000135287   NM_031280.3                                             0.1358  0.0802  0.1297          0.3065  0.0905  0.0859                                                                          MODIFIER        1	SNV     1                                                                                                       Tier5   TAA     .	.                                                                                                                                                                       36455626        maf
    CENPF   0	.	GRCh38  chr1    214608652	214608652	+	Intron  SNP     G	G	A	rs1482929177            TUMOR   NORMAL  G	G                                                                                                                               c.-41-5062G>A                   ENST00000366955         57	45	11	19	19	0	CENPF,intron_variant,,ENST00000366955,NM_016343.3;CENPF,intron_variant,,ENST00000464322,;CENPF,intron_variant,,ENST00000495259,;,regulatory_region_variant,,ENSR00000386218,;ABHD17AP3,non_coding_transcript_exon_variant,,ENST00000503096,;UBE2V1P13,downstream_gene_variant,,ENST00000436983,;        A	ENSG00000117724 ENST00000366955 Transcript	intron_variant                                          rs1482929177    1               1	CENPF   HGNC    HGNC:1857	protein_coding  YES     CCDS31023.1     ENSP00000355922 P49454          UPI00001AE985   NM_016343.3                             1/19                                                                                                                                            MODIFIER        1	SNV     1                                                                                               1.0     PASS    CGG     .	.                                                                                                                    $


## Usage - SLUPipe Configuration for High Performance Computing - SLURM

SLUPipe has been developed to be compatible with High Performance Computing (HPC) and SLURM Job Scheduling.

**SLUPipe Execution:**

Users will construct and provide a base JSON configuration file providing same arguments as before with the inclusion of two new key values:
1. Number of Nodes : Nodes used during HPC Workflow
2. Node Samples : Samples processed per node during HPC Workflow

**IMPORTANT:** SLUPipe HPC mode will process **ALL** samples found within the **input directory**.


**HPC Base Configuration File Example**

    [
      {
        "Pipeline_Mode":"-T",
        "Variant_Callers":["Pindel","Platypus"],
        "Input_Directory":"/student/foo/SLUPipe/src/input",
        "Output_Directory":"student/foo/SLUPipe/src/output",
        "Chromosome_Range": "chr1:16,000,000-215,000,000",
        "vep_ScriptPath": "/student/foo/.conda/envs/SLUPipe/share/ensembl-vep-95.3-0",
        "vep_CachePath": "/student/foo/.vep",
        "reference_directory": "/student/foo/referenceFiles",
        "nodes": "2",
        "node_samples": [] <- Must always be empty list
      }
    ]
    
**Once the base configuration file has been constructed, users must then execute the following script to adapt workload for SLURM compatibility:**

``` console
$ python3 gen_batches.py <base_configuration_file>
```

**This scripts divides all the samples found in the input directory into smaller jobs by generating new JSON files, each representing a portion of a the total workload:**

    Input Directory:
        -> Demo1_T.bam
        -> Demo1_N.bam
        -> Demo2_T.bam
        -> Demo2_N.bam
    
    
    2 Samples / 2 Nodes = 1 Sample Per Job: 
    
    Auto Generated JSON 1:
    [
      {
        "Pipeline_Mode":"-T",
        "Variant_Callers":["Pindel","Platypus"],
        "Input_Directory":"/student/foo/SLUPipe/src/input",
        "Output_Directory":"student/foo/SLUPipe/src/output",
        "Chromosome_Range": "chr1:16,000,000-215,000,000",
        "vep_ScriptPath": "/student/foo/.conda/envs/SLUPipe/share/ensembl-vep-95.3-0",
        "vep_CachePath": "/student/foo/.vep",
        "reference_directory": "/student/foo/referenceFiles",
        "nodes": "2",
        "node_samples:["Demo1_T.bam","Demo1_N.bam"]
      }
    ]
    
    Auto Generated JSON 2:
    [
      {
        "Pipeline_Mode":"-T",
        "Variant_Callers":["Pindel","Platypus"],
        "Input_Directory":"/student/foo/SLUPipe/src/input",
        "Output_Directory":"student/foo/SLUPipe/src/output",
        "Chromosome_Range": "chr1:16,000,000-215,000,000",
        "vep_ScriptPath": "/student/foo/.conda/envs/SLUPipe/share/ensembl-vep-95.3-0",
        "vep_CachePath": "/student/foo/.vep",
        "reference_directory": "/student/foo/referenceFiles",
        "nodes": "2",
        "node_samples:["Demo2_T.bam","Demo2_N.bam"]
      }
    ]

**Once the JSON files have been created, users can then generate a SLURM compatible BASH script to send jobs to SLURM Job Scheduler:**

    #1/bin/bash
    
    source activate SLUPipe
    
    for FILE in *.json:
        echo ${FILE}; do
        sbatch -n 2 -t 1-00:00 --job-name=SLUPipe --cpus-per-task=10 --partition=medmem --wrap="python3 slupipe_apex.py ${FILE}"
        sleep 1
        
    done
    
    
**Run BASH Script**

``` console
$ ./run_slupipe_hpc.sh
```

Each job's results will be placed in the output directory specified in base configuration JSON file. 















