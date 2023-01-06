from flagser import *
import os
import sys

name = "package"

def clone(args):
    if not os.path.exists(getFile("")):
        os.mkdir(getFile(""))
    os.chdir(getFile(""))
    os.system("git clone "+args[0])
    print(args)

def getFile(name):
    path = "/home/spy/.local/tmp/"+name
    if not os.path.exists(path):
        print(name+" package does not exist")
        exit()
    return path

def setVersion(args):
    global name
    file = open(getFile(name)+"/PKGBUILD","r")
    lines = []
    for l in file.readlines():
        if "pkgver=" in l:
            l = "pkgver="+args[0]+"\n"
        lines.append(l)

    file.close()
    file = open(getFile(name)+"/PKGBUILD","w")
    file.writelines(lines)
    file.close()
    os.chdir(getFile(name))
    #os.system("ls")
    os.system("makepkg --printsrcinfo > .SRCINFO")

def upload(args):
    os.chdir(getFile(name))
    os.system("git add .")
    os.system("git commit -m 'new version'")
    os.system("git push")

def getVersion(args):
    file = open(getFile(name)+"/PKGBUILD","r")
    lines = []
    for l in file.readlines():
        if "pkgver=" in l:
            print(l,end="")
            break
def listdir():

    for f in os.listdir(getFile("")):
        print(f)

def update():
    os.chdir(getFile(name))
    os.system("git pull")

def clearPackages(names):
    if len(names) > 1:
        for name in names:
            os.system("rm -rf "+getFile(name))

    elif len(names) > 0 and names[0] == "all":
        for name in os.listdir(getFile("")):
            os.system("rm -rf "+getFile(name))



# flags
src = Flag("clone","--clone", description="the ssh git clone",onCall=lambda args:clone(args))
version = Flag("-v","--set-version" , description="the version to set ",onCall=lambda args:setVersion(args))
getversion = Flag("-gv","--get-version", description="outputs current version ",onCall=lambda args:getVersion(args))
push = Flag("push", "--push", description="push git repo ",onCall=lambda args:upload(args))
pull = Flag("pull", "--pull", description="pull ",onCall=lambda args:update())
packages = Flag("-n","--names", description="outputs cloned package names ",onCall=lambda args:listdir())
r = Flag("-rm", description="removes followed by name (-rm all removes all)", onCall=lambda args:clearPackages(args))

c = FlagManager([src, version, getversion, packages, pull, push, r])
c.description = "PackageVersionController (pvc) helps you update the version to your aur package \nit downloads the ssh repo and updates the version \nand creates a srcinfo file and uploads it"

fname = sys.argv[len(sys.argv)-1]
if os.path.exists("/home/spy/.local/tmp/"+fname) and fname not in c.flags:
    name = fname

c.check()



