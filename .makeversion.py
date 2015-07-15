import pymangal
import os

with open('.version', 'w') as f:
    f.write(pymangal.__version__)
    f.write("\n")

with open('.tag', 'r') as f:
    t = f.readline().rstrip()

if not t == pymangal.__version__ :
    os.system("git tag {0}".format(pymangal.__version__))
