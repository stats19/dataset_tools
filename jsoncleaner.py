import json

with open("C:/Users/Pierre/Desktop/Projet_annuel/substitute.txt", "r") as substitutesplayers:
    for line in substitutesplayers:
        print(line)
        ds = json.loads(line) #this contains the json
        substitutesdico = {}
        for key, values in ds.items():
            # print("old :  %s" %(values))
            old = values
            # print(key)
            print(old)
            seen = set()
            new_l = []
            if old :
                for d in old:
                    t = tuple(d.items())
                    if t not in seen:
                        seen.add(t)
                        new_l.append(d)

                # print(new_l)
                # print("new : %s" %(list(set(values))))
                substitutesdico[key] = new_l
        print(substitutesdico)
        if substitutesdico:
            with open("C:/Users/Pierre/PycharmProjects/xmlscript/test3.txt", "a") as clean_substitutesplayers:
                clean_substitutesplayers.write("%s\n" % (str(substitutesdico)))
            print(substitutesplayers)
