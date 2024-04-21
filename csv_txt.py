from csv import writer, reader

stageslist = [[] for i in range(20)]
savefname = r'D:\experiment\experiment data\ymj exp data\BPsleep\txtwang_stage.txt'
for idx in range(1):
    filename = r'D:\experiment\experiment data\ymj exp data\BPsleep\rmlwang_refine\refined_Stage_LabelsSLP%03d.csv' % (idx + 1)
    with open(filename, newline='') as f:
        readercsv = reader(f)
        for row in readercsv:
            stageslist[idx].append(row)

t = ''
with open(savefname,'w') as q:
    for i in stageslist:
        for e in range(len(i)):
            t = t + str(i[e]) + ''
            q.write(t.strip('\t'))
            q.write('\n')
            t = ''






