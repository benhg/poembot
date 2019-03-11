strin = " ".join(open(input("Poem File?\n") + ".txt", "r").readlines())


def split_string(str, limit, sep=" "):
    words = str.split()
    if max(map(len, words)) > limit:
        raise ValueError("limit is too small")
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


broken = split_string(strin, limit=32)
new = input("what day is this for?")

with open(new+".txt", "w") as fh:
    for line in broken:
        print(len(line))
        fh.write(line+"\n")