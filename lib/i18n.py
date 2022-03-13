import gettext
from babel.messages.catalog import Catalog
from frictionless import Package

def collect_messages(catalog: Catalog, pkg: Package):
    if pkg.title:
        catalog.add(f"pkg.{pkg.name}.title", "", user_comments=("Original string: ", pkg.title, ))

    if pkg.description:
        catalog.add(f"pkg.{pkg.name}.description", "", user_comments=("Original string: ", pkg.description, ))

    for resource in pkg.resources:
        if resource.tabular:
            for field in resource.schema.fields:
                if field.name:
                    catalog.add('pkg.{}.{}.{}'.format(pkg.name, resource.name, field.name), "", locations=[(resource.path, 0)], user_comments=("Original string: ", field.title, ))