import gettext
from babel.messages.catalog import Catalog
from frictionless import Package

def generate_catalog(pkg: Package, catalog_defaults: dict = {}) -> Catalog:
    catalog = Catalog(**catalog_defaults)

    if pkg.title:
        catalog.add(f"{pkg.name}.title", "", user_comments=("Original string: ", pkg.title, ))

    if pkg.description:
        catalog.add(f"{pkg.name}.description", "", user_comments=("Original string: ", pkg.description, ))

    for resource in pkg.resources:
        if resource.tabular:
            for field in resource.schema.fields:
                if field.name:
                    catalog.add('{}.{}.{}'.format(pkg.name, resource.name, field.name), "", locations=[(resource.path, 0)], user_comments=("Original string: ", field.title, ))
    return catalog