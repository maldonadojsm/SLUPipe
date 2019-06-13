import pandas as pd
import glob

def mergeMafs(filename):

    #Requires bash command line argument for filename
    variant_caller_names = []
    mafs = []
    #format in /mafs directory: "filename.variantCaller.maf"
    for file in glob.glob("./output/" + filename + "/MAF/*.maf"):
        variant_caller_name = file.split(".")[2]
        variant_caller_names.append(variant_caller_name)
        maf = pd.read_csv(file, delimiter='\t', header=1)
        maf['variant_caller'] = variant_caller_name
        mafs.append(maf)

    finalMaf = mafs[0]

    for i in range(1, len(mafs)):
        finalMaf = pd.concat([finalMaf, mafs[i]], ignore_index=True, axis=0)

    finalMaf.to_csv(path_or_buf="./output/" + filename + "/MAF/" + filename + ".final.maf", sep='\t', index=False)

    print("Merging MAF: Saving Merged MAFs -> .output/MAF/" + filename + ".final.maf")
    print()
    print("---------------------- MERGED MAF SUMMARY ---------------------------")
    print()
    print(finalMaf.info())
    print(finalMaf['variant_caller'].describe())
    print()
    print("---------------------------------------------------------------------")




