#!/usr/bin/env python3
import json
import os
import collections.abc
import shutil
import errno
import sys

# https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth


def copyDir(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise


# os.path.join returns a string, so each level of recursion has different path


def removeFileOrDirectory(destinationPath):
    if os.path.isdir(destinationPath):
        shutil.rmtree(destinationPath)
    elif os.path.isfile(destinationPath):
        os.remove(destinationPath)


def createFoldersAndFiles(path, data):
    for folderOrFilename, obj in data.items():
        destination = str(folderOrFilename)
        destinationPath = os.path.join(path, destination)

        # create a new folder
        if obj.get("create", False):
            removeFileOrDirectory(destinationPath)
            os.mkdir(destinationPath)
        # deep-copy the file or folder, remove any excepts
        elif "src" in obj:
            source = obj["src"]
            sourcePath = os.path.join(parentDir, source)
            removeFileOrDirectory(destinationPath)
            if os.path.isdir(sourcePath):
                copyDir(sourcePath, destinationPath)
            elif os.path.isfile(sourcePath):
                shutil.copyfile(sourcePath, destinationPath)

            if obj.get("except", False):
                print(obj["except"])
                except_array = obj["except"]
                for remove in except_array:
                    print(remove)
                    removePath = os.path.join(parentDir, remove)
                    print(removePath)
                    removeFileOrDirectory(removePath)

        if "children" in obj:
            for child in obj["children"]:
                createFoldersAndFiles(destinationPath, child)


filepath = sys.argv[-1]

f = open(filepath)

data = json.load(f)

parentDir = os.getcwd()

createFoldersAndFiles(parentDir, data)
