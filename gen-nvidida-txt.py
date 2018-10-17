#!/usr/bin/python3

import argparse
import subprocess
import json
import re

if __name__ == '__main__':

    def cli_arguments():
        """ Command line arguments """

        parser = argparse.ArgumentParser(description='https://github.com/fireice-uk/xmr-stak/blob/master/doc/tuning.md#nvidia-backend', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('-i',  '--index',    default='auto', nargs='+', type=str, help='GPU index (auto for autodetect all GPUs)',  metavar=(0, 1))
        parser.add_argument('-t',  '--threads',  default=17,  type=int, help='Number of threads to run per block')
        parser.add_argument('-b',  '--blocks',   default=60,  type=int, help='Number of CUDA blocks started')
        parser.add_argument('-bf', '--bfactor',  default=0,   type=int, help='Increase if running on in-use workstation')
        parser.add_argument('-bs', '--bsleep',   default=0,   type=int, help='Increase if running on in-use workstation')
        parser.add_argument('-a',  '--affine-to-cpu',   action='store_true',  help='Keep GPU thread with along CPU one, can help if both backend are enabled')
        parser.add_argument('-s', '--sync-mode',  default=3,   type=int, help='CUDA sync mode (?)')
        parser.add_argument('-m', '--mem-mode',   default=1,   type=int, help='CUDA memory mode (?)')
        return parser.parse_args()

    CONFIG = cli_arguments()

    if CONFIG.index == 'auto':
        nvidia_smi_output = subprocess.check_output(['nvidia-smi', '--query-gpu=index', '--format=csv,noheader,nounits'])
        GPU_INDEXES = [int(x.strip()) for x in str(nvidia_smi_output, 'utf-8').splitlines()]
    else:
        GPU_INDEXES = [int(x) for x in CONFIG.index]

    JSON_CONF = {"gpu_threads_conf": []}
    for gpu_index in GPU_INDEXES:
        JSON_CONF['gpu_threads_conf'].append({
            'index': gpu_index,
            'threads': CONFIG.threads,
            'blocks': CONFIG.blocks,
            'bfactor': CONFIG.bfactor,
            'bsleep': CONFIG.bsleep,
            'affine_to_cpu': CONFIG.affine_to_cpu,
            'sync_mode': CONFIG.sync_mode,
            'mem_mode': CONFIG.mem_mode,
        })

    STR_CONF = json.dumps(JSON_CONF, indent=4)
    print("\n".join([re.sub(r'^    ', '', x) for x in STR_CONF.split("\n")[1:-1]]))
