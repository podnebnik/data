#!/usr/bin/env python

import os
from invoke import task
from pathlib import Path
import zipfile
import subprocess
from datapackage_to_datasette import datapackage_to_datasette, DataImportError

def build_container(dataset_name):
    """ Build docker container from datasette dataset """
    import subprocess
    process = subprocess.Popen(['datasette', 'package', 'build/{}/data.db'.format(dataset_name), '-m', 'build/{}/metadata.json'.format(dataset_name), '-t', 'ghcr.io/podnebnik/data-{}:latest'.format(dataset_name)])
    process.communicate()

def package_dataset(dataset_name):
    """ Package frictionless data dataset to datasette format """

    try:
        Path("build/{}".format(dataset_name)).mkdir(parents=True, exist_ok=True)
        datapackage_to_datasette(
            'build/{}/data.db'.format(dataset_name),
            'datasets/{}/datapackage.yaml'.format(dataset_name),
            'build/{}/metadata.json'.format(dataset_name),
            write_mode='replace'
        )
    except DataImportError:
        raise

@task
def package(c, dataset_name=None):
    if dataset_name is None:
        datasets = os.listdir("datasets")
    else:
        datasets = [dataset_name]
    
    for dataset in datasets:
        package_dataset(dataset)
        build_container(dataset)

@task
def zip(c, packageName):
    excludedFiles = [".DS_Store"]
    zip = zipfile.ZipFile("packages/{}.zip".format(packageName), mode="w")
    for root, dirs, files in os.walk('datasets/{}'.format(packageName)):
        if root == "datasets/{}/sources".format(packageName):  # exclude sources
            continue
        for file in files:
            fileName = Path(root, file)
            if file not in excludedFiles:
                archiveName = Path(*(fileName.parts[1:]))
                zip.write(fileName, archiveName)
    zip.close()
