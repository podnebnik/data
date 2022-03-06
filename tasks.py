#!/usr/bin/env python

import os
from invoke import task
from pathlib import Path
import zipfile
import subprocess
from frictionless import Package
import glob
from deepmerge import always_merger
import json
from pprint import pp


def build_container():
    """ Build docker container from datasette dataset """
    import subprocess
    process = subprocess.Popen(['datasette', 'package', *glob.glob('build/*.db'),
                               '-m', 'build/metadata.json', '-t', 'ghcr.io/podnebnik/data:latest'])
    process.communicate()


def datapackage_descriptor_to_metadata_object(descriptor):
    obj = {}
    if descriptor.title:
        obj["title"] = descriptor.title
    if descriptor.description:
        obj["description"] = descriptor.description
    if descriptor.licenses:
        if descriptor.licenses[0].get("name", None):
            obj["license"] = descriptor.licenses[0]["name"]
        if descriptor.licenses[0].get("path", None):
            obj["license_url"] = descriptor.licenses[0]["path"]
        num_licenses = len(descriptor.licenses)
        if num_licenses > 1:
            logging.warning(
                f"{num_licenses} licenses found, but datasette metadata only "
                "allows one license to be specified. Only the first will be used."
            )
    if getattr(descriptor, "schema", None):
        obj["columns"] = {field.name: field.title for field in filter(
            lambda f: getattr(f, "title", None), descriptor.schema.fields)}
        obj["units"] = {field.name: field.unit for field in filter(
            lambda f: hasattr(f, "unit"), descriptor.schema.fields)}
    if getattr(descriptor, "homepage", None):
        obj["source_url"] = descriptor.homepage
    return obj


def extract_metadata(dp, dbname):
    metadata = {"databases": {
        dbname: datapackage_descriptor_to_metadata_object(dp)}}

    metadata["databases"][dbname]["tables"] = {}
    for resource in dp.resources:
        if resource.tabular:
            md = datapackage_descriptor_to_metadata_object(resource)
            if md:
                table_name = resource.name
                metadata["databases"][dbname]["tables"][table_name] = md
    if not metadata["databases"][dbname]["tables"]:
        del metadata["databases"][dbname]["tables"]

    return metadata


def convert(datapackage_path, dbname):
    """ Convert frictionless data package to sqlite database """

    dp = Package(datapackage_path)
    dp.to_sql(f"sqlite:///build/{dbname}.db")
    return extract_metadata(dp, dbname)


def discover_datapackages():
    return glob.iglob('datasets/*/datapackage.yaml')


@task
def package(c):
    Path("build/").mkdir(parents=True, exist_ok=True)
    metadata = {}
    for datapackage_path in discover_datapackages():
        dbname = os.path.basename(os.path.dirname(datapackage_path))
        metadata = always_merger.merge(
            metadata, convert(datapackage_path, dbname))

    with open('build/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=4, sort_keys=True)
    build_container()


@task
def zip(c, packageName):
    excludedFiles = [".DS_Store"]
    zip = zipfile.ZipFile("packages/{}.zip".format(packageName), mode="w")
    for root, dirs, files in os.walk('datasets/{}'.format(packageName)):
        # exclude sources
        if root == "datasets/{}/sources".format(packageName):
            continue
        for file in files:
            fileName = Path(root, file)
            if file not in excludedFiles:
                archiveName = Path(*(fileName.parts[2:]))
                zip.write(fileName, archiveName)
    zip.close()
