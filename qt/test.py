import os

import sys


path = '/'.join(sys.argv[0].split('\\')[:-1])
print(path+'/img')
print(os.listdir(path+'/img'))