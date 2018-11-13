#! /usr/bin/env python

import sys
import subprocess
import os
import logging
import fileinput

from toml_parser import TOMLParser

########################################
# Functions
########################################

def exec_cmd(lst_cmd, shell=False):

    try:
        logger.debug('Command: {0}'.format(cmd))
        ret = subprocess.check_output(lst_cmd, shell)[:-1]
        logger.debug('Return: {0}'.format(ret))
        return ret
    except subprocess.CalledProcessError as e:
        # print("*** Error occured in processing command! ***")
        # print("Return code: {0}".format(e.returncode))
        # print("Command: {0}".format(e.cmd))
        print("Output: {0}".format(e.output))
        # raise e
        pass

########################################
# Main
########################################

if __name__ == '__main__':

    parser = TOMLParser()
    args = sys.argv
    if len(args) == 1:
        raise Exception('Specify command!')
    parser.parse(os.path.expanduser('~/.launcher.toml'))
    conf = parser.dict_root
    
    loglevel = conf['global']['loglevel']
    
    if loglevel == 'DEBUG':
        level_ = logging.DEBUG
    elif loglevel == 'INFO':
        level_ = logging.INFO
    elif loglevel == 'WARNING':
        level_ = logging.WARNING
    elif loglevel == 'ERROR':
        level_ = logging.ERROR
    elif loglevel == 'CRITCAL':
        level_ = logging.CRITCAL
    
    logging.basicConfig(level = level_)
    logger = logging.getLogger(__name__)
    
    logger.debug(conf)
    
    # for item in fileinput.input():
    for item in sys.stdin.readlines():
        item = item.replace('\n', '')
        if conf['global']['calc_pattern'] == 'CMD':
            cmd = sys.argv[1:] + [item]
        elif conf['global']['calc_pattern'] == 'MPI':
            cmd = ['mpirun', '-n'] + sys.argv[1:] + [item]

        print('$ {0}'.format(' '.join(cmd)))
        # print(' '.join(cmd))
        ret = exec_cmd(cmd)
        if ret is not None:
            print(ret)
        print('')
