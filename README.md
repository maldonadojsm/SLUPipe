<p align="center">
<img src=https://github.com/BioHPC/SLUPipe/blob/master/src/misc/slupipe.png width="250" height="250"/>
</p>

# SLUPipe: A (S)omatic Ana(L)ysis (U)mbrella (Pipe)line 

## Table of Contents
 + [Description](#description)
 + [Features](#features)
 + [Installation](#installation)
 + [Usage](#usage)
 
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
- MuSE 
- Mutect2
- Somatic Sniper
- Varscan 
- Strelka 2

**Non-paired Sample Variant Callers (Tumor Only):**
- Pindel
- Platypus
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

## Installation

For convenience, SLUPipe has been configured to run in Anaconda Environments

**1. Clone Github Repository**
```console
git clone https://github.com/BioHPC/SLUPipe/tree/master/src
```
**2. Download & Install Anacaonda 4.5+**

https://www.anaconda.com/distribution/

**3. Create an Anaconda Environment which uses Python3.6.8 as default:**
```console
conda create -n SLUPipe python=3.6
```
**4. Activate the Anaconda Environment:**
```console
source activate SLUPipe
```
**5. The NGS Pipeline will require the following Python packages for it to be fully functionable:**

**biobambam-2.0.87**
```console
conda install -c bioconda biobambam 
```
**bwa.kit-0.7.15**
```console
conda install -c bioconda bwakit 
```
**ensembl-vep 95.3**
``` console
conda install -c bioconda ensembl-vep=95.3 
```
**GenomeAnalysisTK-3.8.0**
``` console
conda install -c bioconda gatk
```
**MuSE 1.0.rc**
``` console
conda install -c bioconda muse 
```
**pandas 0.24.2**
``` console
conda install -c anaconda pandas 
```
**pindel-0.2.5b9**
``` console
conda install -c bioconda pindel 
```
**platypus-opt 1.0.3**
``` console
conda install -c bioconda platypus-variant 
```
**psycopg2 - 2.7.6.1**
``` console
conda install -c anaconda psycopg2 
```
**samtools-1.9**
``` console 
conda install -c bioconda samtools
```
**strelka 2.9.10**
``` console
conda install -c bioconda strelka 
```
**somatic-sniper 1.0.5.0**
``` console
conda install -c bioconda somatic-sniper 
```
**varscan - 2.4.3.2**
``` console
conda install -c bioconda varscan 
```
**vcf2maf - 1.6.16**
``` console
conda install -c bioconda vcf2maf
```

**Configuring Ensembl VEP For Variant Annotation & MAF Conversion (Local Cache Installation):**
   1. Create .vep directory to store offline cache: mkdir ~/.vep
   2. cd $HOME/.vep
   3. curl -O ftp://ftp.ensembl.org/pub/release-95/variation/indexed_vep_cache/homo_sapiens_vep_95_GRCh38.tar.gz
   4. tar xzf homo_sapiens_vep_96_GRCh38.tar.gz


**IMPORTANT**

 VCF2MAF May Downgrade Samtools 1.9 to 1.7  causing issues. Reinstall Samtools (1.9) to solve. 


## Usage

**Activate Anaconda Environment**
``` console
source activate SLUPipe
```
**Execute Pipeline Workflow**
```console
python3 slupipe.py <config.json>
```

**Version Summary & Execution Description**
```console
python3 slupipe.py 
```

**Check Latest Software Release**
```console
python3 slupipe.py --update
```


**Reference Files:** Place reference .fasta files in **referenceFiles** directory.

**Non-paired Mode (Tumor Only) Input Entries:** Place Tumor .bam files in **tumor mode directory** (input/tumor_mode).

**Paired Mode (Normal Mode) Input Entries:** Place Normal & Tumor .bam files in **normal mode directory** (input/normal_mode).


**Configuration File Structure Format (JSON)**:

    [
      {
        "Pipeline_Mode":"-T",
        "Variant_Callers":["Pindel","Platypus"],
        "Input_Directory":"/student/foo/SLUPipe/src/input/tumor_mode",
        "Chromosome_Range": "chr1:16,000,000-215,000,000",
        "vep_ScriptPath": "/student/foo/.conda/envs/SLUPipe/share/ensembl-vep-95.3-0",
        "vep_CachePath": "/student/foo/.vep",
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

    
    
**Pipeline Workflow Example (Non-paired Mode):**

    (SLUPipe) MacBook-Pro-2:src username$ python3 NGS.py config.json
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
    Merging MAF: Saving Merged MAFs -> .output/MAF/tumor2_T.final.maf
    
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






