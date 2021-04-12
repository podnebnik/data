# instructions for preparing your datapackage

A datapackage is a combination of data resources (`.csv` data files) and a datapackage descriptor file (`.yaml`) containing the metadata. 

Create a fork of the `https://github.com/podnebnik/data` repository and follow the instructions below to create your datapackage. (NB: have a look at existing datapackages already in the repo, for reference.)

## preparing the data resources

Use the following template for your datapackage folder structure that you should place in the root of the `https://github.com/podnebnik/data` repository:
```
data/
    - emissions/
        - data/
            - source/
                emissions.xlsx
                pipeline.py
            emissions.csv
            emissions.energy.csv
            emissions.aviation.csv
            emissions.agriculture.csv
        datapackage.yaml
```

1. give your datapackage a unique and descriptive name (e.g. "emissions") and name the folder in root.
2. within the folder create a `data/sources/` subfolder for the original data files (if they exist) and any for code used to transform the data into `.csv` files.
3. place the `.csv` files into the `data/` subfolder (see below for more details on these files)
4. prepare the metadata `.yaml` file for your datapackage (see below for detailed instructions on how to do that). 

### preparing the data files (`.csv` format)

Data files should be in `.csv` format:
* single row header
* comma separated fields 
* one row per record of equal length

The file names should be:
* descriptive and understandable, avoid unfamiliar abbreviations
* if you have several files in your datapackage, they should all have a common and unique prefix - usually the same one as the name of your datapackage (see the example above).

The variable names should be:

* descriptive and understandable, avoid unfamiliar abbreviations
* avoid redundancy: if a descriptor is in the filename, there is no need to repeat it in the variable names 
* do not use spaces or any special characters except underscores "`_`"
* use a double underscore "`__`" to delineate hierarchical levels e.g. `fuel_combustion__transport` 

*e.g. if the file name is `emissions.agriculture.csv` the following applies for variable names:*

* `emissions.agriculture.manure.management` - not OK
* `emissions_agriculture__manure_management` - not OK
* `manure.management` - not OK
* `manure_management` - OK 

## preparing the metadata 

Once the data files are all ready, you will 

1. use the `python` package `frictionless` to infer the basic metadata directly from the files into a `.yaml` file
2. manually add the information that cannot be inferred into the `.yaml` file just created.

The final `.yaml` file containing the metadata should be stored at the same level as the `data/` subfolder in your datapackage. 

### automatic description of the datapackage

Make sure you have python installed on your system, then install the `frictionless` package: 

```
pip install frictionless
```

The `frictionless` command `describe` will automatically create the basic metadata file.

From your datapackage folder you can describe a set of `.csv` files with the help of the `*` wildcard operator like in the following example.  

```
frictionless describe data/emissions*.csv --yaml > datapackage.yaml
```
This creates a `datapackage.yaml` file inferring the metadata for all files that follow the `emissions*.csv` pattern in the `data\` folder. 
### manually amend the datapackage metadata 

Open the `datapackage.yaml` file and amend it to add 

* *package-level metadata* i.e. information that applies to all the `.csv` files in your datapackage
* *resounce-level metadata* i.e. information that applies to individual `.csv` files (which are called *resources*). 

Pay attention to indentation! A newly created `datapackage.yaml` file will only have two fields at the top level: `profile` and `resources`. You should attempt the following fields (*but if any of this metadata does not apply equally to all of the files in your datapackage, you should instead add them to the individual resources instead!*):

* `contributors`: enter your name
* `name`: for your short datapackage name, this should be the same as the folder name (e.g. emissions)
* `title`: should be a longer name of your datapackage (e.g. Historical and projected CO2 equiv. emissions)
* `description`: enter a longer description of your datapackage
* `keywords`: enter relevant keywords in english as an array enclosed in square brackets (e.g. [emissions, agriculure])
* `geography`: enter the geographic area the data refer to (e.g. Europe)
* `schedule`: enter the time resolution for the data e.g. annual, monthly.. 
* `sources`: should follow this template:
```
sources:
  path:         # path to file in repo if exists
  url:          # url to original data source if possible 
  title:        # name of data source
  author:       # organisation or person who is the owner of the data
  code:         # path to code in repo used to transform data into csv files if exists
  date_accessed:# date when data was extracted in ISO format
```
* `licenses:` unless required otherwise by your data source, enter the following: 
```
licenses:
  name: AGPL 3.0
  path: http://www.gnu.org/licenses/agpl-3.0.en.html
  title: GNU Affero General Public License 3.0
```

For each individual file (i.e. resource) check the existing metadata and add or change the following (if appropriate):

* `name`: for your short datapackage name, this should be the same as the folder name (e.g. emissions)
* `title`: should be a longer name of your datapackage (e.g. Historical and projected CO2 equiv. emissions)

If there is not a common data source for the whole package and individual files have their separate `sources` you must add them here instead:
```
sources:
  path:         # path to file in repo if exists
  url:          # url to original data source if possible 
  title:        # name of data source
  author:       # organisation or person who is the owner of the data
  code:         # path to code in repo used to transform data into csv files if exists
  date_accessed:# date when data was extracted in ISO format
```
Finally, the fields in each resource: they already have the `resource.schema.fields.name` and `resource.schema.fields.type` values inferred. 

* `name`: do not change this value, it should be identical to the one in the `.csv` file.
* `type`: you should check the types are correct and change them if required. Usually this will only mean changing the values to `date` or `year` if appropriate. 
* `title`: add a descriptive title e.g. `luluc` -> `Land use and land use change`
* `unit`: if appropriate, add the unit of the variable 
* you can also add a `format` field. See [here](https://specs.frictionlessdata.io/table-schema/#types-and-formats) for valid types and formats. 
* You can also add constraints for the fields, as well as missing value definitions and primary and foreign keys if necessary. See [this](https://specs.frictionlessdata.io/table-schema/#constraints) for more options. 

### translate the metadata 

Once you're finished editing the `datapackage.yaml` file, make a copy of the file and name it `datapakcage.si.yaml` Keeping the keys in the original English, translate the values into Slovenian for the following fields: `name`, `title`, `description`, `keywords`, `resources.name`, `resources.title`, `resources.sources.title`, `resources.sources.title`, `resources.schema.fields.title` and `resource.schema.fields.unit` as appropriate. 

*Do not translate any of the values for the `name` keys!*
## finished?

Once you're happy with the files, the folder structure and the `datapackage.yaml` metadata file, create a (draft) pull request tagging @joahim and @majazaloznik as reviewers.