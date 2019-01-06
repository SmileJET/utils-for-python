# encoding:utf8

import os
from glob import glob

def event_for_file(filename):
    try:
        os.remove(filename)
    except:
        print('Remove File [%s] Error.'%(str(filename)))
    

def event_for_dir(dir):
    try:
        for filename in glob(dir+'/*'):
            print(filename)
            if os.path.isfile(filename):
                os.remove(filename)
            elif os.path.isdir(filename):
                event_for_dir(filename)            
        os.removedirs(dir)
    except:
        print('Remove Dir [%s] Error.'%(str(dir)))
