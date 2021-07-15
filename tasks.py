import os
from invoke import task
from pathlib import Path
import zipfile


@task
def zip(c, packageName):
    excludedFiles = [".DS_Store"]
    zip = zipfile.ZipFile("packages/{}.zip".format(packageName), mode="w")
    for root, dirs, files in os.walk(packageName):
        for file in files:
            fileName = Path(root, file)
            if file not in excludedFiles:
                archiveName = Path(*(fileName.parts[1:]))
                zip.write(fileName, archiveName)
    zip.close()
