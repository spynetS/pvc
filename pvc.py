#!/usr/bin/python

from flagser import *
import os
import sys
import subprocess

name = "package"
downloadPath = "/.local/tmp"


def clone(args):
    if not os.path.exists(getFile("")):
        os.mkdir(getFile(""))
    os.chdir(getFile(""))
    os.system("git clone ssh://aur@aur.archlinux.org/"+args[0]+".git")

def getFile(name):
    # get home path
    result = subprocess.check_output("echo $HOME", shell=True).decode("utf-8").replace("\n", "")
    path = result+downloadPath+"/"+name
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

def getVersion():
    file = open(getFile(name)+"/PKGBUILD","r")
    lines = []
    for l in file.readlines():
        if "pkgver=" in l:
            return l.split("=")[1]
def listdir():

    for f in os.listdir(getFile("")):
        print(f)

def update():
    os.chdir(getFile(name))
    os.system("git pull")

def clearPackages(names):
    for name in names:
        os.system("rm -rf "+getFile(name))

    if len(names) > 0 and names[0] == "all":
        for name in os.listdir(getFile("")):
            os.system("rm -rf "+getFile(name))
# the questiion is should 2.0.9 become 2.0.10 or 2.1.0 ?
def increment():
    version = getVersion()
    newVersion = ""
    numbers = []
    for num in version.split("."):
        numbers.append(int(num))
    last = numbers[-1]
    if last != 9:
        numbers[-1] = last+1
    else:
        numbers[len(numbers)-2] = numbers[len(numbers)-2]+1
        numbers[-1] = 0
    for num in numbers:
        newVersion+=str(num)+"."

    newVersion = newVersion[:-1]
    setVersion([newVersion])


def generate(arg):
    name = arg[0] if len(arg)>0 else "package"
    try:
        os.mkdir(name)
    except:
        pass
    os.chdir(name)
    file = '''
pkgname=
pkgver=1.0.0
pkgrel=1
epoch=
pkgdesc=""
arch=(x86_64)
url=""
license=('MIT')
groups=()
depends=()
makedepends=()
checkdepends=()
optdepends=()
provides=()
conflicts=()
replaces=()
backup=()
options=()
install=
changelog=
source=()
noextract=()
md5sums=(SKIP)
validpgpkeys=()

prepare() {

}

build() {
}

package() {
}
              '''
    os.system("touch PKGBUILD")
    f = open("PKGBUILD","w")
    f.write(file)

c = FlagManager([
    Flag("clone","--clone      ", description="clones the package (only packagename ssh://aur@aur.archlinux.org/ already defined)",onCall=lambda args:clone(args)),
    Flag("-v   ","--set-version" , description="the version to set ",onCall=lambda args:setVersion(args)),
    Flag("-gv  ","--get-version", description="outputs current version ",onCall=lambda args:print("pkgver="+getVersion(),end="")),
    Flag("push ", "--push       ", description="push git repo ",onCall=lambda args:upload(args)),
    Flag("pull ", "--pull       ", description="pull ",onCall=lambda args:update()),
    Flag("-n   ","--names      ", description="outputs cloned package names ",onCall=lambda args:listdir()),
    Flag("-rm  ", description="removes followed by name (-rm all removes all)", onCall=lambda args:clearPackages(args)),
    Flag("-i   ", description="increments version (2.0.1 -> 2.0.2)", onCall=lambda args:increment()),
    Flag("init ", description="generates file (followed by prodname)", onCall=generate),
])
c.description = "PackageVersionController (pvc) helps you update the version to your aur package \nit downloads the ssh repo and updates the version \nand creates a srcinfo file and uploads it\n\nUSE\npvc [command] [package name]\nEXAMPLE\npvc clone linecounter-git -v 2.0.1 push linecounter-git -rm linecounter-git\nThis will clone linecounter-git change version and upload it and then delete the clone\n"

fname = sys.argv[len(sys.argv)-1]
result = subprocess.check_output("echo $HOME", shell=True).decode("utf-8").replace("\n", "")
if os.path.exists(result+downloadPath+"/"+fname) and fname not in c.flags:
    name = fname

c.check()



