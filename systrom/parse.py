import csv
import re
import sys
from datetime import datetime

import wikitextparser as wtp


parsed = wtp.parse(sys.stdin.read())
# Simple heuristic to check the tables are in the assumed order.
assert 'cases' in parsed.tables[0].caption
assert 'deaths' in parsed.tables[1].caption

for out, table in zip(sys.argv[1:], parsed.tables):
    writer = csv.writer(open(out, 'w'))
    data = table.data()

    header = data[1]
    assert header[56] == 'Date'
    header = [re.search(r'\b[A-Z]{2}\b', h).group()  # extract state
              for h in header[1:56]]
    header.insert(0, 'Date')
    writer.writerow(header)

    for row in data[2:]:
        if row[0] == 'Date':
            continue
        if row[0] == 'Total':
            break
        row = row[:56]
        row = [re.sub('<[^>]*>', '', x).strip() for x in row]
        date = re.search(r'\b\d\d?-[A-Z][a-z]{2}-\d\d\b', row[0]).group()
        row[0] = datetime.strptime(date, '%d-%b-%y').date().isoformat()
        row[1:] = [x.replace(',', '') for x in row[1:]]
        writer.writerow(row)
