import hashlib


def get_urls(file):
    with open(file) as f:
        lines = f.read().split("\n")
    return set([l.split(",")[0] for l in lines][1:])

def url_hash(url):
    return hashlib.sha224(url.encode("utf-8")).hexdigest()