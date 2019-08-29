# !/usr/bin/env python
# title           :slupipe_apex.py
# description     :Script which configures SLUPipe for HPC
# author          :Juan Maldonado
# date            :7/24/19
# version         :1.0
# usage           :python3 slupipe_apex.py
# notes           :
# python_version  :3.6.5
# =================================================================================================================

import controller as cn
import json
import sys
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


def main():
    """
    Main method will process differing executions of program depending if the user has provided a config.json file
    """
    if len(sys.argv) == 2:

        # User has indicated to check for updates
        if sys.argv[1] == "--update":
            check_version()

        #
        # SLUPIPE HTC: User has provided a config.json file. This JSON file will contain a key which will store all
        # of the files that the node will process. The JSON has been generated via an external script.
        #
        else:
            with open(sys.argv[1], 'r') as file:
                config_dict = json.load(file)
            slu_pipe = cn.Controller(config_dict)
            # Input samples to be processed by computer node
            slu_pipe.configure_pipeline(1)
    # User hasn't provided a config.json file
    else:
        slu_pipe = cn.Controller()
        slu_pipe.show_summary()


if __name__ == '__main__':
    main()