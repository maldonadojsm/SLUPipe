# !/usr/bin/env python
# title           :slupipe.py
# description     :SLUPipe Execution Script
# author          :Juan Maldonado
# date            :6/13/19
# version         :0.5
# usage           :python3 slupipe.py <config.json>
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.6.5
# conda_version   :4.6.14
# =================================================================================================================

import controller as cn
import json
import sys
import os
import argparse
from subprocess import call, check_output


def check_version():
    """
    Checks latest software releases found in repository.
    """
    call(["git", "fetch"])
    local_branch = check_output(["git", "rev-parse", "HEAD"])
    master_branch = check_output(["git", "rev-parse", "master@{upstream}"])

    if local_branch != master_branch:
        print("New Software Release Found. Please head to "
              "https://github.com/BioHPC/SLUPipe/tree/master/src for further information.")

    elif local_branch == master_branch:
        print("Running Latest Software Release.")



"""
 python3 slupipe.py config.json node_dir(optional)
"""
def main():
    """
    Main method will process differing executions of program depending if the user has provided a config.json file
    """
    parser = argparse.ArgumentParser(description="Process Custom Variant Caller Configs")

    parser.add_argument('slupipe_conf',metavar='<config.json>', action='store', type=str, help='SLUPipe Config File')
    parser.add_argument('variant_one', nargs='?', help='Variant Caller Config 1', default='')
    parser.add_argument('variant_two', nargs='?', help='Variant Caller Config 2',default='')
    parser.add_argument('variant_three',nargs='?', help='Variant Caller Config 3',default='')
    parser.add_argument('variant_four', nargs='?',help='Variant Caller Config 4',default='')
    parser.add_argument('variant_five', nargs='?', help='Variant Caller Config 5',default='')

    args = parser.parse_args()

    variant_caller = ["muse.json", "mutect.json", "varscan.json", "sniper.json"]
    if args.variant_one:
        if args.variant_one in variant_caller:
            print(os.path.abspath(args.variant_one))
    if args.variant_two:
        if args.variant_two in variant_caller:
            print(os.path.abspath(args.variant_two))

    if args.variant_three:
        if args.variant_three in variant_caller:
            print(os.path.abspath(args.variant_three))

    if args.variant_four:
        if args.variant_four in variant_caller:
            print(os.path.abspath(args.variant_four))

    if args.variant_five:
        if args.variant_five in variant_caller:
            print(os.path.abspath(args.variant_five))



    #DEFAULT MODE
    if len(sys.argv) == 2:

        # User has indicated to check for updates
        if sys.argv[1] == "--update":
            check_version()
        # User has provided a config.json file
        else:
            with open(sys.argv[1], 'r') as file:
                config_dict = json.load(file)

            slu_pipe = cn.Controller(0,config_dict)
            slu_pipe.configure_pipeline(0)
    # Test MuSE
    elif len(sys.argv) == 3:
        # User has indicated to check for updates
        if sys.argv[1] == "--update":
            check_version()
        # User has provided a config.json file
        else:
            with open(sys.argv[1], 'r') as file:
                config_dict = json.load(file)


            args = parser.parse_args()

            print(args)

            print(os.path.abspath(sys.argv[2]))
            slu_pipe = cn.Controller(1, config_dict, os.path.abspath(sys.argv[2]))
            slu_pipe.configure_pipeline(0)


    # User hasn't provided a config.json file
    else:
        slu_pipe = cn.Controller()
        slu_pipe.show_summary()


if __name__ == '__main__':
    main()






