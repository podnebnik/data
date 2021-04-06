from frictionless import Package, describe

# use already prepared metadata
package = Package(<.yaml>)

# add package attributes
package.name = "" # same as suffix of the .csv files in the package
package.title = "" # descriptive package title
package.description = "" # longer description 
package.contributors = "" # single author or array if there were more
package.version = "0.1.0" # use semantic versioning
package.licenses = {"name": "AGPL 3.0",  # do not change the licence unless you know what you're doing
    "path": "http://www.gnu.org/licenses/agpl-3.0.en.html", 
    "title": "GNU Affero General Public License 3.0"}

# add package source if it is the same for all files
package.sources = {
    "title": "",
    "path": "" #
}

# add or change individual resource sources by refering to the resource name
package.get_resource(<name>).sources = {
    "title": "",
    "path": ""
}

# change individual resource names if they are inappropriate
package.get_resource(<name>).name = ""

# add or change individual resource attributes by refering to the resource name and field:
package.get_resource(<name>).schema.get_field(<fileld.name>).title = ""
package.get_resource(<name>).schema.get_field(<fileld.name>).description = ""

# change the year field to the correct type:
package.get_resource(<name>).schema.get_field("year").type = "year"


# save package metadata
package.to_yaml(<.yaml>)