import os
import shutil
import distutils
from subprocess import call
from distutils.dir_util import copy_tree

# Dev Notes
# Only use built in python libraries to keep configuration to minimum

# TODO
# 1. Refactor this code into classes
# 2. Auto push to newly created repo
# 3. build.gradle processor which allows to add/remove libraries on the fly
#    and other stuff
# 4. Add a logger/silent mode

package=""
projectName=""

# Jumpstart Project Configuration
jumpstartPackage = "com.adgdelhi.jumpstart"
jumpstartDirectoryName = "AndroidJumpstart"
jumpstartRepoURL = "https://github.com/adg-delhi/AndroidJumpstart.git"
srcRelativeRoot = "/app/src/<srcSet>/java/"

def cloneJumpstartRepo():
    call(["git", "clone", jumpstartRepoURL])

def createNewDirectories():
    global projectName
    while (not projectName):
        projectName = raw_input("Enter new app name(e.g. Jumpstart): ")
        if(projectName == ""):
            print("Project name cannot be empty")

    # Keeping for testing purposes
    # if(os.path.exists(projectName)):
    #    shutil.rmtree(projectName)

    print("Copying stuff from " + jumpstartDirectoryName + " to " + projectName)
    shutil.copytree(jumpstartDirectoryName, projectName)
    print("Done Copying")

def changeSourcePackage(srcSet):
    relativeRoot = srcRelativeRoot.replace("<srcSet>", srcSet)
    print (srcSet + ": " + relativeRoot)

    srcPath = projectName +  relativeRoot + jumpstartPackage.replace(".", "/")
    if(os.path.exists(srcPath)):
        print("creating directory structure for new package: " + package)
        packagePath = package.replace(".", "/")
        currentPath = projectName + relativeRoot + "temp/" + packagePath
        print("Copying stuff from " + srcPath + " to " + currentPath)
        shutil.copytree(srcPath, currentPath)
        print("Copying Done! Now removing old stuff")
        shutil.rmtree(projectName + relativeRoot + "com")
        print("Deleting Done!")
        print("Moving new things where they belong!")

        # copying things in a temp folder first in order to avoid same name clashes
        print projectName + relativeRoot + "temp/" + " to " + projectName + relativeRoot
        copy_tree(projectName + relativeRoot + "temp/", projectName + relativeRoot)
        print("Removing temporary directory")
        shutil.rmtree(projectName + relativeRoot + "temp")
    else:
        print "Path does not exist " + srcPath


def replacePackageInSource():
    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk("./" + projectName):
        for file in files:
            filePath = root + "/" + file
            if(".git/" in filePath):
                print "Skipping: " + filePath
                continue
            else:
                print(filePath)

            fileText = ""
            with open(filePath) as f:
                fileText = f.read().replace(jumpstartPackage, package)

            with open(filePath, "w") as f:
                f.write(fileText)

cloneJumpstartRepo()
createNewDirectories()

while (not package):
    package = raw_input("Enter new app package(e.g. com.google.inbox): ")
    if(package == ""):
        print("Package name cannot be empty")

# TODO this can be improved. Iterate the directory instead
changeSourcePackage("main")
changeSourcePackage("androidTest")
changeSourcePackage("debug")
changeSourcePackage("debugProd")
changeSourcePackage("release")
changeSourcePackage("test")

replacePackageInSource()
