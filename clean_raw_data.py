import csv

names = ['workforce', 'citizen', 'fertility']
moderations = ['h', 'l']
heterogeneities = ['1', '2', '3']
for name in names:
    for moderation in moderations:
        for heterogeneity in heterogeneities:
            csvread = open('datasets/' + moderation + 'm' + heterogeneity +
                           '_' + name + '.csv', encoding="utf8")
            reader = csv.reader(csvread)
            csvwrite = open('datasets/' + moderation + 'm' + heterogeneity +
                           '_' + name + '_cleaned.csv', 'a+', encoding="utf8")
            writer = csv.writer(csvwrite)

            for idx, row in enumerate(reader):
                if idx > 13:
                    writer.writerow(row)
