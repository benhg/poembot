def split_string(str, limit=32, sep=" "):
    words = str.split()
    try:
        if max(map(len, words)) > limit:
            raise ValueError("limit is too small")
    except Exception as e:
        print(e)
        return []
    res, part, others = [], words[0], words[1:]
    for ind, word in enumerate(others):
        if len(sep) + len(word) > limit - len(part):
            res.append(part)
            part = word
        else:
            part += sep + word
    if part:
        res.append(part)
    for i, ln in enumerate(res):
        if i != 0:
            res[i] = "   "+ln
    return res

def split_poem(st):
    lines = []
    for line in st.split("\n"):
        lines.append("\n".join(split_string(line)))
    return lines

import csv

with open("19poems.csv") as fh:
    reader = csv.DictReader(fh)
    for line in reader:
        fixed_text = split_poem(line["Text of poem"])
        author = split_string(line["Author"], limit=32)
        title = split_string(line["Title"])
        date = line["Date"].zfill(2)
        print(date)
        with open("poems/{}.txt".format(date), "w") as fh2:
            for line2 in title:
                fh2.write(line2+"\n")
            fh2.write("\n")
            fh2.write("By ")
            for i , line2 in enumerate(author):
                fh2.write(line2+ "\n")
            fh2.write("\n")
            for line2 in fixed_text:
                fh2.write(line2+"\n")
