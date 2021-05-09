# import csv

# def change_format(fname, fenc, wname, wenc):
#     f = open(fname, encoding=fenc)
#     reader = csv.reader(f)

#     w = open(wname, 'w', encoding=wenc, newline='')
#     writer = csv.writer(w, delimiter=',')
#     for l in reader:
#         wlist = []
#         for ent in l:
#             ent = ent.strip().replace('-', '0').replace(',', '')
#             try:
#                 ent = int(ent)
#             except:
#                 pass

#             wlist.append(ent)

#         writer.writerow(wlist)

# change_format('data/test.csv', 'euc-kr', 'data/test.edit.csv', 'utf-16')

# import csv

# f1 = open('data/monsters.csv', encoding='utf-16')
# reader = csv.reader(f1)

# f2 = open('data/req_hp.csv', encoding='utf-8')
# reader2 = csv.reader(f2, delimiter='\t')

# wf = open('data/monsters.edit.csv', 'w', encoding='utf-16', newline='')
# writer = csv.writer(wf, delimiter=',')

# while True:
#     try:
#         l1 = next(reader)
#         l2 = next(reader2)
    
#     except:
#         exit(0)

#     hp, name = l1
#     req_hp = l2[0]

#     hp = int(hp.strip().replace(',', ''))
#     name = name.strip()
#     req_hp = int(req_hp.strip().replace(',', ''))

#     writer.writerow([name, hp, req_hp])

print(2049059.443 // 1)
print(2049059.443 % 1)
print(int(2049059.443))
print(int(2049059.999))
print(list(str(0.999)))
