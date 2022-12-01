# -*- coding: utf-8 -*-

import codecs
import csv
import datetime
import os
import re


INPUT_FILE = "cooling-heating-degree-days.txt"
ENCODING = "iso8859-2"


def to_date(s):
    if s == "/":
        return ''
    return datetime.datetime.strptime(s, "%d.%m.%Y").strftime("%Y-%m-%d")


def null_if_slash(s):
    if s == '/':
        return ''
    return s


def parse_heating_degree_days(input_data):
    in_metadata = False
    in_metadata_data = False
    in_data = False
    in_data_data = False

    postaje_header = ["st_postaje", "tip_postaje", "ime_postaje", "nadm_vis", "lat", "lon", "datum_zacetka", "datum_konca"]
    postaje_data = [postaje_header]
    meritve_header = [
        "st_postaje", "tip_postaje", # added in
        "leto", "tprim12", "tprim15", "zacetek_ks", "konec_ks", "traj_ks", "tpres18", "tpres21", "tpres23", "cdd24"
    ]
    meritve_data = [meritve_header]

    st_postaje = None
    tip_postaje = None

    for line in input_data.splitlines():
        if line.startswith("METAPODATKI PO LOKACIJAH MERITEV"):
            # print([1, line])
            in_metadata = True
            continue

        if line.startswith("PODATKI"):
            # print([2, line])
            in_data = True
            continue

        if in_metadata:
            if line.startswith("----------------------------"):
                # end of metadata
                in_metadata = False
                continue

            # print([1, len(line), line])
            
            line = line.strip()
            if line:
                if not in_metadata_data:
                    # 
                    if line.startswith('Št_post '):
                        # header
                        # print(line)
                        in_metadata_data = True
                        continue
                else:
                    postaje_line = re.split('\s{2,}', line)

                    postaje_line[6] = to_date(postaje_line[6])
                    postaje_line[7] = to_date(postaje_line[7])

                    # print(postaje_line)

                    postaje_data.append(postaje_line)

        if in_data:
            line = line.strip()
            # print([4, line])

            if line.startswith("Številka postaje:"):
                st_postaje = line.split(':', 1)[1].strip()

            if line.startswith('Tip postaje:'):
                tip_postaje = line.split(':', 1)[1].strip()

            if line.startswith("Leto"):
                in_data_data = True
                continue

            if in_data_data:
                if line == '':
                    in_data_data = False
                    continue
                else:
                    meritev_line = [i.strip() for i in line.split('\t')]
                    
                    meritev_line[1] = null_if_slash(meritev_line[1])
                    meritev_line[2] = null_if_slash(meritev_line[2])
                    meritev_line[3] = to_date(meritev_line[3])
                    meritev_line[4] = to_date(meritev_line[4])
                    meritev_line[5] = null_if_slash(meritev_line[5])
                    meritev_line[6] = null_if_slash(meritev_line[6])
                    meritev_line[7] = null_if_slash(meritev_line[7])
                    meritev_line[8] = null_if_slash(meritev_line[8])
                    meritev_line[9] = null_if_slash(meritev_line[9])

                    meritev_record = [st_postaje, tip_postaje] + meritev_line

                    # print(meritev_record)
                    meritve_data.append(meritev_record)

    return postaje_data, meritve_data


def data_file(f):
    return os.path.join(os.path.dirname(__file__), '..', 'data', f)


def save_csv(fn, data):
    with open(data_file(fn), "w") as f:
        w = csv.writer(f)
        for row in data:
            w.writerow(row)


def main():
    
    # read file
    with codecs.open(INPUT_FILE, "r", ENCODING) as f:
        input_data = f.read()

    # parse data
    postaje_data, meritve_data = parse_heating_degree_days(input_data)

    # save csvs
    save_csv("heating.degree_days.csv", meritve_data)
    save_csv("heating.degree_day_stations.csv", postaje_data)


if __name__ == '__main__':
    main()
