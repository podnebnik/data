# instructions for preparing your datapackage

A datapackage is a combination of data resources (`.csv` data files) and a datapackage descriptor file (`.yaml`) containing the metadata. 

## preparing the data resources

### file location

Data files should be saved in the `https://github.com/podnebnik/data` repository in the `data/` folder.

### file types

Data files should be in `.csv` format:
* single row header
* comma separated fields 
* one row per record of equal length

*[... ne vem kolk je tle treba še standardizirat...]*

### file names
* names should be descriptive and understandable, avoid unfamiliar abreviations
* if you have several files in your datapackage, they should all have a common and unique prefix
* do not use spaces or any special characters except underscores "`_`"
* use a double underscore "`__`" to delineate hierarchical levels e.g. `emissions_historical__agriculture.csv` 

### variable names

* names should be descriptive and understandable, avoid unfamiliar abreviations
* naming should be parsimonoius: if a descriptor is in the filename, there is no need to repeat it in the variable names within
* do not use spaces or any special characters except underscores "`_`"
* use a double underscore "`__`" to delineate hierarchical levels e.g. `fuel_combustion__transport` 

## preparing the metadata 

Once the data files are all ready, you'll use the `python` package `fricitonless` to infer the metadata directly from the files, as well as manually the information that cannot be inferred. 

The final `.yaml` file containing the metadata should be stored in the root of the `https://github.com/podnebnik/data` repository.

### automatic description of the datapackage

Make sure you have python installed on your system, then install the `frictionless` package: 

```
pip install frictionless
```

The command `describe` will automatically create the basic metadata file and because we want it in yaml format, use the `--yaml` option. 

From the root of the `https://github.com/podnebnik/data` repository you can describe a signle csv file, by running:

```
frictionless describe data/emissions_historical.csv --yaml > datapackage__emissions_historical.yaml
```
or to describe a set of files, you can do:

```
frictionless describe data/emissions_*.csv --yaml > datapackage__emissions.yaml
```

Open the `.yaml` file and inspect it for further reference. You will now ammend it to add:

1. package level metadata - that applies to all the resources e.g. name, title, description, contributors, version, sources..
2. resource level metadata - that applies to individual `.csv` files e.g. title, description, sources; and to individual fields e.g. title, description, type, format.

Instead of manually editing the `.yaml` file direclty, it is safer to use the prepared template> `datapackage__template.py` file. Make a copy of the template to edit. First replace the placeholder with the path to the `.yaml` file you have just created e.g.

```
# use already prepared metadata
package = Package("datapackage__emissions.yaml")
```
### adding package level metadata

Enter the values for the following attributes describing the whole datapackage. 

The package name should match the unique prefix of the data files contained within. 

```
package.name = ""
package.title = ""
package.description = ""
package.contributors = ""
package.version = "0.1.0"
package.licenses = {"name": "AGPL 3.0", 
    "path": "http://www.gnu.org/licenses/agpl-3.0.en.html", 
    "title": "GNU Affero General Public License 3.0"}
```

If all the files in your package come from the same source, you need to add it at the package level. The `path` attribute can be a path or url. 

```
package.source = {
    "title": "",
    "path": ""
}
```
### adding file level metadata

If each file has a different source, you need to add it at file (i.e. resource) level by refering to the resource name as defined in the `.yaml` file. If the source file is in the repository you can use a relative path, otherwise a url would be great. 

```
package.get_resource(<name>).sources = {
    "title": "",
    "path": ""
}
```

Then add the attributes for each field in the resource, using the resource and field names:

```
package.get_resource(<name>).schema.get_field(<field.name>).title = ""
package.get_resource(<name>).schema.get_field(<field.name>).description = ""
```
If you want to change the name of a resource, you can do that like so:
```
package.get_resource(<name>).name = "New better name"
```
And then you must of course use the new name of the resource if you wish to make any more changes to it. 

File level metadata checklist:

1. If you do not have a `sources` attribute at the package level, you *must* have them at file level, one for each file.
1. You *must* add a `title` attribute to each field in each resource. 
1. You can also add a `description` attribute. 
1. You *must* check the data `type` was inferred correctly for each field and ammend it if not. NB: `year` and `date` are valid data types, you should make sure you use them where appropriate. 
1. You can also add a `format` field. See [here](https://specs.frictionlessdata.io/table-schema/#types-and-formats) for valid types and formats. 
1. You can also add constraints for the fields, as well as missing value definitions and primary and foreign keys if necessary. See [this](https://specs.frictionlessdata.io/table-schema/#constraints) for more options. 

### save your metadata

When you are finished editing the metadata, the `.yaml` file is exported with the final line in the template. Name the `.yaml` file using the prefix `datapackage__` and the package name (which should be the same as the prefix of all the files within it) e.g. `datapackage__emissions.yaml`:

```
# save package metadata
package.to_yaml(<.yaml>)
```
Run the file and you're done! 

NB: save the python script you've just written (using the same naming convention as for the `.yaml` file), since you will need it again if you ever want to update your datapackage. 