import sys
sys.path.insert(0,'audit/tmp_M4')
from pages import pages
src,p=sys.argv[1],sys.argv[2]
print(pages[(src,p)])
