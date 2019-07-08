# !/usr/bin/env python
# title           :maf_merger.py
# description     :Aggregates maf files into a master maf file
# author          :Juan Maldonado
# date            :6/13/19
# version         :0.5
# usage           :
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.6.5
# conda_version   :4.6.14
# ============================
import pandas as pd
import glob


def merge_maf(filename, output_dir):

    variant_caller_names = []
    mafs = []

    for file in glob.glob(output_dir + filename + "/maf/*.maf"):
        variant_caller_name = file.split(".")[2]
        variant_caller_names.append(variant_caller_name)
        maf = pd.read_csv(file, delimiter='\t', header=1)
        maf['variant_caller'] = variant_caller_name
        mafs.append(maf)

    final_maf = mafs[0]

    for i in range(1, len(mafs)):
        final_maf = pd.concat([final_maf, mafs[i]], ignore_index=True, axis=0)

    final_maf.to_csv(path_or_buf=output_dir + filename + "/maf/" + filename + ".final.maf", sep='\t', index=False)

    print("Merging MAF: Saving Merged MAFs -> .output/MAF/" + filename + ".final.maf")
    print()
    print("---------------------- MERGED MAF SUMMARY ---------------------------")
    print()
    print(final_maf.info())
    print(final_maf['variant_caller'].describe())
    print()
    print("---------------------------------------------------------------------")




