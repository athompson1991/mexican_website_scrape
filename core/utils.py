import hashlib
import os
import datetime
import shutil


def get_urls(file):
    with open(file) as f:
        lines = f.read().split("\n")
    return set([l.split(",")[0] for l in lines][1:])

def url_hash(url):
    return hashlib.sha224(url.encode("utf-8")).hexdigest()

def transfer_csvs(site, specific_file=None):
    raw_data_dir = "data/" + site + "_listings/"
    files = os.listdir(raw_data_dir)
    if specific_file is None:
        check_dict = {}
        for file in files:
            date_str = file.split(".")[0][-17:]
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d_%f")
            check_dict[dt] = file
        max_dt = max(check_dict.keys())
        target_file =  check_dict[max_dt]
    else:
        target_file = raw_data_dir + specific_file
    destination = "listings_tables/" + site + ".csv"
    shutil.copyfile(raw_data_dir + target_file, destination)
    print("Copied over: " + target_file)

def camel_case_split(str):
    words = [[str[0]]]

    for c in str[1:]:
        if words[-1][-1].islower() and c.isupper():
            words.append(list(c))
        else:
            words[-1].append(c)
    return "_".join([''.join(word).lower() for word in words])
