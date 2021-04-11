in no particular order:
 
1. encoding: če v skripti uporabljaš čšž-je, so v `yaml` fajlu v unicode stringih, a je to OK!? A moramo prepovedati vse čšž-je?
1. Lincence? jest sem kr splonkala AGPL iz sledilnik/data. eno je treba za default določit-
1. custom polja v yaml-u, a majo lahko underscore al kaj?
1. missing values. zdej je recimo v `emissions.historical.waste.csv` uporabljen "NO", pa nisem niti ziher a nej bi blo to NA al kej druzga.. ampak zato je tud kot string označena ta spremeljivka. skratka to je treba rešit
1. kaj pa `.timestamp` fajli? oz. ekvivalent?
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
