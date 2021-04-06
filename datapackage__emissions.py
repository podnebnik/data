from frictionless import Package, describe

# infer package metadata 
package = describe("data/emissions*.csv")

# or use already prepared metadata
# package = Package("datapackage__emissions.yaml")

# add package attributes
package.name = "emissions"
package.title = "Annual CO2 emissions for Slovenia"
package.description = "Annual C02 equivalent emissions from 1986 to most recent year available."
package.contributors = "Žiga Zaplotnik"
package.version = "0.1.0"
package.licenses = {
    "name": "AGPL 3.0", 
    "path": "http://www.gnu.org/licenses/agpl-3.0.en.html", 
    "title": "GNU Affero General Public License 3.0"}

# add a new package attribute
package["geography"] = "Slovenia"

# add sources for a single resource
package.get_resource("emissions_historical_agriculture").sources = {
    "title": "I have no idea where this data is from",
    "path": "../emission_data/TGP 1986-2019.xlsx"
}

# add titles to fields in a single resource
package.get_resource("emissions_historical_agriculture").schema.get_field("year").title = "Year"
package.get_resource("emissions_historical_agriculture").schema.get_field("total").title = "Total emissions from agriculture"
package.get_resource("emissions_historical_agriculture").schema.get_field("enteric_fermentation").title = "Enteric fermentation from cattle, sheep, swine and other livestock"
package.get_resource("emissions_historical_agriculture").schema.get_field("manure_management").title = "Manure management"
package.get_resource("emissions_historical_agriculture").schema.get_field("liming").title = "Liming"
package.get_resource("emissions_historical_agriculture").schema.get_field("urea_application").title = "Urea application"
package.get_resource("emissions_historical_agriculture").schema.get_field("fertilizers").title = "Other carbon containing fertilizers"

# add data types...
package.get_resource("emissions_historical_agriculture").schema.get_field("year").type = "year"

# add a new field attributes
package.get_resource("emissions_historical_agriculture").schema.get_field("urea_application")["unit"] = "tonnes CO2 equiv."
package.get_resource("emissions_historical_agriculture").schema.get_field("fertilizers")["unit"] = "tonnes CO2 equiv."

# save package metadata
package.to_yaml("datapackage__emissions.yaml")