

f1 = open("f1.csv", "r")
contents = f1.read()
contents = contents.replace(",", "\t", -1)
f1.close()
f2 = open("flights.tsv", "w")
f2.write(contents)
f2.close()