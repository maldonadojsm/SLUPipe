import Controller
import config as cfg
import json
import sys




# This currently sends the config file towards the controller class and then the contro

"""

python3 SLUPipe.py (argv[0]) config.json(argv[1])

"""

def main():



    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as file:
            config_dict = json.load(file)

        NGS = Controller.Controller(config_dict)
        NGS.runGo()



    # # Parse File
    #
    #     pipeline_mode = config_dict[0]['Pipeline_Mode']
    #     variant_callers = config_dict[0]['Variant_Callers']
    #     input_directory = config_dict[0]['Input_Directory']
    #     chromosome_range = config_dict[0]['Chromosome_Range']
    #     vep_script = config_dict[0]['vep_ScriptPath']
    #     vep_cache = config_dict[0]['vep_CachePath']


    else:
        NGS = Controller.Controller()
        NGS.runSummary()



if __name__ == '__main__':
    main()






