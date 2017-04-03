############################################################
# Module  : All System Paths
# Date    : March 23rd, 2017
# Author  : Xiao Ling
############################################################

import os
import shutil
from utils import Writer

############################################################
'''
    System Root
'''
root      = os.getcwd()
input_dir = os.path.join(root, 'input')

# local
if root[0:6] == '/Users':
    data_root = '/Users/lingxiao/Documents/research/data/good-great'

# nlp grid
elif root[0:5] == '/mnt/':
    data_root = '/nlp/users/xiao/good-great'

else:
    data_root = ''

'''
    System Environment
'''
PATH = {# directories that should exist before application runs
        'directories': {
            'deploy' : os.path.join(root, 'deploy')
           ,'log'    : os.path.join(root, 'deploy/logs')
           ,'input'  : os.path.join(root, 'inputs'     )
        },

        # path to files that must exist before application runs
        'assets': {
            # test sets
            'ccb'      : os.path.join(root, 'inputs/test/ccb.txt'    )
           ,'bansal'   : os.path.join(root, 'inputs/test/bansal.txt' )
           ,'anne-25'  : os.path.join(root, 'inputs/test/anne-25.txt' )
           ,'anne-125' : os.path.join(root, 'inputs/test/anne-125.txt')

           # graph
           , 'graph'      : os.path.join(root, 'inputs/raw-graph/graph.json')
           , 'graph-and'  : os.path.join(root, 'inputs/raw-graph/graph_and.json')
           , 'graph-or'   : os.path.join(root, 'inputs/raw-graph/graph_or.json')
           , 'graph-ngram': os.path.join(root, 'inputs/raw-graph/graph-ngram.txt')},

        # path to files created by application
        'inputs': {
            'graph-wt-by-edge-cnt': os.path.join(root, 'inputs/wt-graph/graph-wt-by-edge-cnt.txt')
        }
    }

def setup(PATH,clear_logs):

    os.system('clear')

    log_dir = PATH['directories']['log']

    if clear_logs or os.path.exists(log_dir):
        shutil.rmtree(log_dir)
        os.mkdir(log_dir)
    else:
        os.mkdir(log_dir)

    writer = Writer(log_dir)
    writer.tell('Initializing application [ good-great-combo ] ...')

    for _,path in PATH['directories'].iteritems():
        if not os.path.exists(path):
            writer.tell('making directory at ' + path)
            os.mkdir(path)
        else:
            writer.tell('directory ' + path + ' already exists')

    for _,path in PATH['assets'].iteritems():

        name = path.split('/')[-1]

        if not os.path.exists(path):
            writer.tell('Fatal Error: critical asset ' + name + ' not found at ' + path)
            writer.close()
            raise NameError('Error: path not found: ' + path)
        else:
            writer.tell('Located critical asset ' + name + ' at ' + path)

    writer.tell('complete application setup!')
    writer.close()

setup(PATH,False)


