import sys
# print  (sys.version_info)
if sys.version_info[0]==2:
    reload(sys)
    sys.setdefaultencoding('utf8')
    
def  wait4input():
    if sys.version_info[0]==2:
        t=raw_input()
    if sys.version_info[0]==3:
        t=input()

# wait4input()