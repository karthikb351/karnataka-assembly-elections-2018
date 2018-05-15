import json

with open('src/api/trend.json', 'r') as file:
    data = json.load(file)

headers = [
'constituency_name', # 0
'constituency_number', # 1
'leading_candidate', # 2
'leading_party', # 3
'trailing_candidate', # 4
'trailing_party', # 5
'margin', # 6
'status', # 7
'2013_winning_candidate', # 8
'2013_winning_party', # 9
'2013_margin' # 10
]
# for row in data:
#     if (row['Leading Party'] == 'Bharatiya Janata Party' and int(row['Margin']) < 500):
#         print row['Constituency Name'], row['Margin']

res = sorted((f for f in data if f['leading_party'] == 'Bharatiya Janata Party'), key=lambda x: int(x['margin']), reverse=True)
for r in res:
    print r['constituency_name'], r['margin'], "||", r['2013_winning_party'], "with", r['2013_margin']
