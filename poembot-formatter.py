# strin = " ".join(open(input("Poem File?\n") + ".txt", "r").readlines())


def split_string(str, limit=32, sep=" "):
    words = str.split()
    print(len(words))
    try:
        if max(map(len, words)) > limit:
            raise ValueError("limit is too small")
    except Exception as e:
        print(e)
        return
    res, part, others = [], words[0], words[1:]
    for word in others:
        if len(sep) + len(word) > limit - len(part):
            res.append(part)
            part = word
        else:
            part += sep + word
    if part:
        res.append(part)
    return res

"""
broken = split_string(strin, limit=32)
new = input("what day is this for?")

with open(new+".txt", "w") as fh:
    for line in broken:
        print(len(line))
        fh.write(line+"\n")
"""

import csv

with open("19poems.csv") as fh:
    reader = csv.DictReader(fh)
    for line in reader:
        fixed_text = split_string(line["Text of poem"], limit=32)
        author = split_string(line["Author"], limit=32)
        title = split_string(line["Title"])
        date = line["Date"].zfill(2)
        print(date)
        with open("poems/{}.txt".format(date), "w") as fh2:
            for line2 in title:
                fh2.write(line2+"\n")
            fh2.write("\n")
            fh2.write("By: ")
            for line2 in author:
                fh2.write(line2+ "\n")
            fh2.write("\n")
            for line2 in fixed_text:
                fh2.write(line2+"\n")
