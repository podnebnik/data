#!/usr/bin/python

from pyaxis import pyaxis
import pandas as pd
import os

ENCODING = 'cp1250'


def next_to_this_file(fn):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), fn))



def convert_px(px_filename, csv_filename):
    print("loading .px: %s" % (px_filename,))
    d = pyaxis.parse(px_filename, encoding=ENCODING)

    f1 = d["DATA"].copy()

    # lowercase columns
    print("lowercasing columns")
    f1 = f1.rename(columns={col: col.lower().replace(' ', '_') for col in f1.columns })

    # clean up values
    print("cleaning values")
    f2 = f1.copy()
    f2["data"] = f2["data"].replace('"-"', None)
    f2["data"] = f2["data"].replace('"..."', None)

    # check
    f2[f2["data"] == '"-"']
    
    # save into csv
    print("saving to csv: %s" % (csv_filename,))

    # ensure stable sort for clean diffs
    f3 = f2.sort_values(by=["leto", "gorivo", "meritve"])

    f4 = f3.rename(columns={
        "gorivo": "fuel",
        "leto": "year",
        "meritve": "measured",
    })

    f4.to_csv(csv_filename, index=False)
    
    units = ", ".join(d["METADATA"].get("UNITS", []))
    

    print("done.")
    return d


if __name__ == "__main__":
    convert_px(
        next_to_this_file("2021/1818002S.px"),
        next_to_this_file("../data/balance_of_fuels.csv")
    )
