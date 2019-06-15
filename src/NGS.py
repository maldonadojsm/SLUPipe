# !/usr/bin/env python
# title           :NGS.py
# description     :SLUPipe Execution Script
# author          :Juan Maldonado
# date            :6/13/19
# version         :0.4
# usage           :python3 NGS.py <config.json>
# notes           :SEE README.txt for Usages & List of Dependencies
# python_version  :3.6.5
# conda_version   :4.6.14
# =================================================================================================================

import Controller
import json
import sys
from subprocess import call


def check_version():
    """
    Checks latest software releases found in repository.
    """
    call(["git", "fetch"])
    local_branch = call(["git", "rev-parse", "HEAD"])
    master_branch = call(["git", "rev-parse", "master@{upstream}"])

    if local_branch != master_branch:
        print("New Software Release Found. Please head to "
              "https://github.com/BioHPC/SLUPipe/tree/master/src for further information")

    elif local_branch == master_branch:
        print("Running Latest Software Release ")


def main():
    """
    Main method will process differing executions of program depending if the user has provided a config.json file
    """
    if len(sys.argv) == 2:

        # User has indicated to check for updates
        if sys.argv[1] == "--update":
            check_version()
        # User has provided a config.json file
        else:
            with open(sys.argv[1], 'r') as file:
                config_dict = json.load(file)

            slu_pipe = Controller.Controller(config_dict)
            slu_pipe.configure_pipeline()

    # User hasn't provided a config.json file
    else:
        slu_pipe = Controller.Controller()
        slu_pipe.show_summary()


if __name__ == '__main__':
    main()






