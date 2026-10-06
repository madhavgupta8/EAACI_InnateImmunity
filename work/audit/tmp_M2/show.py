import sys; sys.path.insert(0,'/Users/madhavgupta/Projects/Papa_EAACIexam/work/audit/tmp_M2')
from pages import *
src=sys.argv[1]
for p in sys.argv[2:]:
    print('=====',src,p); print(cols(get(src,p)))
