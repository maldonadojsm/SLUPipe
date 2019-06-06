configuration = {

    # Disable Variants Callers by replacing variant caller name with "None" ["None","Platypus","None"]
    "variantCallers_tumorMode": ["Pindel", "Platypus", "MuTect2"],
    "variantCallers_normalMode": ["MuSE", "MuTect2", "Varscan", "Sniper", "Strelka2"],
    "input_tumor": "/student/maldonadojs/SLUPipe/SLUPipe_V0.3_TEST/src/input/tumor_mode",
    "input_normal": "/student/maldonadojs/SLUPipe/SLUPipe_V0.3_TEST/src/input/normal_mode",
    "chromosome_Range": "chr1:16,000,000-215,000,000",
    "vepScriptPath": "/student/maldonadojs/.conda/envs/SLUPipe/share/ensembl-vep-95.3-0",
    "vepCachePath": "/student/maldonadojs/.vep",
    "cpuCores": "8",
}
