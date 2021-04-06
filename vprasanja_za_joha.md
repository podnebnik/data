in no particular order:

1. kateri atributi so dovoljeni? ker ena [specifikacija je tukaj](https://specs.frictionlessdata.io/data-package/#metadata) alternativno je [tukaj en seznam](https://specs.frictionlessdata.io/data-package/#metadata) Samo recimo `contributors` piše, da mora biti array, ampak v resnici ni treba, da je. Pa recimo `author` dela, čeprav ga ni na seznamu, ampak druge stvari, ki jih ni na seznamu pa ne delajo.  
1. encoding: če v skripti uporabljaš čšž-je, so v `yaml` fajlu v unicode stringih, a je to OK!?
1. Lincence? jest sem kr splonkala AGPL iz sledilnik/data. 
1. anyway, katere atribute *moramo* uporabiti? najboljš, da jih konkretno določimo, če ne bo kaos?
1. kaj pa `.timestamp` fajli?
1. a naj folk ročno popravlja `.yaml` al po navodilih al naj dobijo template? ok, zdej je template.
1. meni ne dela validacija za cel data package, samo za posamezen resource. 

recimo tole dela:
```
frictionless describe data/emissions_historical.csv --yaml > datapackage__emissions_historical.yaml
frictionless validate datapackage__emissions_historical.yaml 
```
tole pa ne:

```
frictionless describe data/emissions_historical*.csv --yaml > datapackage__emissions.yaml
frictionless validate datapackage__emissions.yaml 
```
9. kam naj dajo originalne (recimo .xlsx) fajle. Opcija je, da imamo še folder `data_raw` ali kaj podobnega?
9. `sources` ima samo `title` in `path` atributa. Meni je to ful čudno. Jaz bi mela še vsaj avtorja (i.e. organizacijo) in nekaj v smislu `date_accessed` al neki?
9. dodajanje novih polj, sploh na nivoju package-a. recimo `geography` (slovenija, evropa..), ali pa `time_resolution` (annual, monthly), pa na nivoju fieldov recimo `unit` (e.g. tonnes of CO2 equiv, C). To moramo vse v naprej definirat?
9. jest ne znam pythona, sam vem pa, da se ziher da to lepš delat: 
* recimo a moraš res za vsak atribut vedno `get_field()` in `get_resource()` uporabit al se da kako to nestat? 
```
package.get_resource("emissions_historical_agriculture").schema.get_field("fertilizers").title = "Other carbon containing fertilizers"
package.get_resource("emissions_historical_agriculture").schema.get_field("fertilizers").description = "Other carbon containing fertilizers"
```
* al pa kako se na eleganten način recimo doda isti atribut z isto vrednostjo večim fieldom v enem fajlu? Recimo, da hočeš vsem razen `year` dodat `unit`, ne boš valda vsake vrstice pisal posebi:
```
package.get_resource("emissions_historical_agriculture").schema.get_field("urea_application")["unit"] = "tonnes CO2 equiv."
package.get_resource("emissions_historical_agriculture").schema.get_field("fertilizers")["unit"] = "tonnes CO2 equiv."
```