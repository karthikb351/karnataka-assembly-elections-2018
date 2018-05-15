from bs4 import BeautifulSoup
import grequests
import json

dataAll = []
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

urls = [
'http://eciresults.nic.in/StatewiseS10.htm',
'http://eciresults.nic.in/StatewiseS101.htm',
'http://eciresults.nic.in/StatewiseS102.htm',
'http://eciresults.nic.in/StatewiseS103.htm',
'http://eciresults.nic.in/StatewiseS104.htm',
'http://eciresults.nic.in/StatewiseS105.htm',
'http://eciresults.nic.in/StatewiseS106.htm',
'http://eciresults.nic.in/StatewiseS107.htm',
'http://eciresults.nic.in/StatewiseS108.htm',
'http://eciresults.nic.in/StatewiseS109.htm',
'http://eciresults.nic.in/StatewiseS1010.htm',
'http://eciresults.nic.in/StatewiseS1011.htm',
'http://eciresults.nic.in/StatewiseS1012.htm',
'http://eciresults.nic.in/StatewiseS1013.htm',
'http://eciresults.nic.in/StatewiseS1014.htm',
'http://eciresults.nic.in/StatewiseS1015.htm',
'http://eciresults.nic.in/StatewiseS1016.htm',
'http://eciresults.nic.in/StatewiseS1017.htm',
'http://eciresults.nic.in/StatewiseS1018.htm',
'http://eciresults.nic.in/StatewiseS1019.htm',
'http://eciresults.nic.in/StatewiseS1020.htm',
'http://eciresults.nic.in/StatewiseS1021.htm',
]


requests = (grequests.get(u) for u in urls)
responses = grequests.map(requests)
for i, response in enumerate(responses):
    soup = BeautifulSoup(response.text, 'html.parser')
    trs = soup.findAll("tr", {"style" : "font-size:12px;"})
    for tr in trs:
        results = tr.findChildren(recursive=False)
        data = {}
        for idx, result in enumerate(results):
            isTable = result.findAll("table") != []
            if isTable:
                data[headers[idx]]=result.find("table").find('td').text.strip()
            else:
                data[headers[idx]]=result.text.strip()
        dataAll.append(data)
with open('src/api/trend.json', 'w') as file:
    file.write(json.dumps(dataAll))
    print "Saved trend data"


const_urls = []
for i in range(1, 225):
    if i not in [173, 154]:
        const_urls.append('http://eciresults.nic.in/ConstituencywiseS10'+str(i)+'.htm?ac='+str(i))

requests = (grequests.get(u) for u in const_urls)
responses = grequests.map(requests)

const_headers = [
'candidate_name',
'candidate_party',
'votes'
]

all_const_data = []

for i, response in enumerate(responses):
    soup = BeautifulSoup(response.text, 'html.parser')
    trs = soup.findAll("tr", {"style" : "font-size:12px;"})
    all_votes = []
    for tr in trs:
        results = tr.findChildren(recursive=False)
        votes_data = {}
        results = results if len(results) == 3 else results[2:]
        for idx, result in enumerate(results):
            votes_data[const_headers[idx]] = result.text.strip()
        all_votes.append(votes_data)
    metas = soup.findAll("td", {"colspan": "3"})
    const_data = {
        'constituency_name': metas[0].text.strip().split(" - ")[1],
        'status': metas[1].text.strip(),
        'votes': all_votes
    }
    all_const_data.append(const_data)
with open('src/api/constituency.json', 'w') as file:
    file.write(json.dumps(all_const_data))
    print "Saved constituency data"
