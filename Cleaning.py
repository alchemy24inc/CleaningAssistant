import os,sys
import shutil

oDirExist=0
oRenders=[]
oPrecomp=[]
oDoRND=None
oDoPRE=None
while oDirExist==0:
    oProject = raw_input("Project to clean (folder's name): ")
    oPath = "//FILESERVER/prod/PROJECTS/%s/WORKSPACE"%(oProject)
    if not os.path.exists(oPath):
        print "Project folder's name doesn't exist. Try again."
    else:
        oDirExist=1
print "\nDo you want to clean..."
while oDoRND not in ["y","n"]:
    oDoRND = raw_input("...RENDERS folders?('y' or 'n') ")
while oDoPRE not in ["y","n"]:
    oDoPRE = raw_input("...PRECOMP folders?('y' or 'n') ")

if oDoRND=="y":
    oDoRND=True
elif oDoRND=="n":
    oDoRND=False
    
if oDoPRE=="y":
    oDoPRE=True
elif oDoPRE=="n":
    oDoPRE=False


print "\nScanning folders..."

oSeqDirs = os.listdir(oPath)
for iSeq in oSeqDirs:
    oShotDirs=os.listdir("/".join([oPath,iSeq]))
    oShotDirs.remove("nfo")
    for iShot in oShotDirs:
        oRenders.append("/".join([oPath,iSeq,iShot,"RENDERS"]))
        oPrecomp.append("/".join([oPath,iSeq,iShot,"ELEMENTS","PRECOMP"]))
    
oRenders.sort()
oPrecomp.sort()

if oDoRND:
    print "Deleting .MOV in RENDERS folder..."
    for r in oRenders:
        iRender = os.listdir(r)
        iRender.sort()
        for i in iRender:
            if i in [".DS_Store","._.DS_Store","Thumbs.db"]:
                continue
            iSplit = i.split(".")
            if len(iSplit)>= 2:
                if iSplit[-1]=="mov":
                    try:
                        os.remove("/".join([r,i]))
                        print ""
                    except:
                        print "Skipping","/".join([r,i])
                        
    print "Deleting folders (except last _comp_ version) in RENDERS folder...\n"
    for r in oRenders:
        iRender = os.listdir(r)
        iRender.sort()
        for i in iRender:
            if i in [".DS_Store","._.DS_Store","Thumbs.db"]:
                continue
            iSplit = i.split(".")
            if len(iSplit) < 2:
                if "comp" not in i.split("_"):
                    try:
                        shutil.rmtree("/".join([r,i]))
                    except:
                        print "Skipping","/".join([r,i])
                        pass
                else:
                    compList=os.listdir(r)
                    compList.sort()
                    for c in compList[:-1]:
                        try:
                            shutil.rmtree("/".join([r,c]))
                        except:
                            print "Skipping","/".join([r,i])
                            pass

if oDoPRE:
    print "Deleting files and folders in PRECOMP folder..."
    for p in oPrecomp:
        iPrecomp = os.listdir(p)
        iPrecomp.sort()
        for i in iPrecomp:
            if len(i.split("."))>= 2:
                os.remove("/".join([p,i]))
            else:
                try:
                    shutil.rmtree("/".join([p,i]))
                except:
                    print "Skipping","/".join([r,i])
                    pass

raw_input("Press ENTER to exit...")
