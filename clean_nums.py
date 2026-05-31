import re, os

src = "/root/pcs-build/src"
for f in os.listdir(src):
    if not f.endswith(".html"):
        continue
    path = os.path.join(src, f)
    with open(path) as fh:
        c = fh.read()
    # strip ALL line-number prefixes: 1|, 1|1|, 22|, 22|22|, etc.
    c = re.sub(r'^\d+\|(?:\d+\|)?', '', c, flags=re.MULTILINE)
    with open(path, 'w') as fh:
        fh.write(c)
    print(f"{f} cleaned")
