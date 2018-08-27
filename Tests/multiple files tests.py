f1 = open('./testfakelog.txt.txt', 'r')
f2 = open('./writetest.txt.txt', 'w')

line1 = f1.readline()
print(line1)
f2.write(line1)

f1.close()
f2.close()


#Bestätigt, dass mehrere Dateien gleichzeitig bearbeitet werden können.
