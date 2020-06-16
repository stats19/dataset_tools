with open("C:/Users/Pierre/PycharmProjects/xmlscript/substitute.sql", "a") as substitutesql:
    lines_seen = set()  # holds lines already seen
    outfile = open("C:/Users/Pierre/PycharmProjects/xmlscript/cleansubstitute.sql", "w")
    for line in open("C:/Users/Pierre/PycharmProjects/xmlscript/substitute.sql", "r"):
        if line not in lines_seen:  # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()