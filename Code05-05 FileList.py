import os
for dirName, subDirList, fnames in os.walk('C:/images/'):
    for fname in fnames:
        # print(fname)
        #
        # print(os.path.join(dirName,fname)[1])
        if os.path.splitext(fname)[1].upper() == '.RAW' :
            print(os.path.join(dirName,fname))