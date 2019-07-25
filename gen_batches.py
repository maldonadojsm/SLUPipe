# !/usr/bin/env python
# title           :gen_batches.py
# description     :Generate necessary JSON needed for Node Configuration
# author          :Juan Maldonado
# date            :7/25/19
# version         :1.0
# usage           :python3 gen_batches.py
# notes           :
# python_version  :3.6.5
# =================================================================================================================


import json
import sys

def main():
    """
    Main method will process differing executions of program depending if the user has provided a config.json file
    """
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as file:
            config_dict = json.load(file)

        if config_dict[0] == "-T":
            print("Generating missing .bai files...")
            directory_listing = os.listdir(self.input_directory)
            for item in directory_listing:
                if "_T" and '.bam' in item:
                    # Capture Filename
                    filename = os.path.splitext(os.path.basename(item))[0]
                    # Capture tumorBAM PATH
                    tumor_bam = os.path.basename(item)
                    # Store in Sample List
                    self.directory.append(directoryStruct(tumor_bam, filename))


        if flag == 1:
            print("Generating missing .bai files...")
            self.generate_bai_files()
            directory_listing = os.listdir(self.input_directory)
            for item in directory_listing:
                if "_N" and ".bam" in item:
                    for item2 in directory_listing:
                        if "_T" and ".bam" in item2:
                            normal_bam_file = os.path.splitext(os.path.basename(item))[0].replace("_N", "")
                            tumor_bam_file = os.path.splitext(os.path.basename(item2))[0].replace("_T", "")

                            # If BAM Normal and Tumor Files have same ID
                            if normal_bam_file == tumor_bam_file:
                                filename = normal_bam_file
                                # Store in Sample List
                                self.directory.append(
                                    directoryStruct(os.path.basename(item2), filename, os.path.basename(item)))


    # User hasn't provided a config.json file
    else:
        slu_pipe = cn.Controller()
        slu_pipe.show_summary()


if __name__ == '__main__':
    main()

