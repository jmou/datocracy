import csv
import itertools
import math
import os
import sys
from datetime import date


def cumulative(infile):
    reader = csv.reader(infile)
    header = next(reader)
    cml = [0] * len(header)
    lastdate = None
    day = 0
    for row in reader:
        thisdate = date.fromisoformat(row[0])
        if lastdate:
            day += (thisdate - lastdate).days
        lastdate = thisdate
        for i in range(1, len(header)):
            if row[i]:
                cml[i] += int(row[i])
                yield(header[i], day, cml[i])


def since100(state_day_count):
    start = None
    last_count = 0
    for _, day, count in state_day_count:
        if start is None and count >= 100:
            # Linear interpolate partial day when count was 100. Imprecise but
            # helps like with MI that jumps to 334. Also staggers points.
            start = day - (count - 100) / (count - last_count)
            if count > 100:
                yield 0, 100
        if start is not None:
            yield day - start, count
        last_count = count


_, root = sys.argv
os.makedirs(root, exist_ok=True)

for state, data in itertools.groupby(sorted(cumulative(sys.stdin)), lambda x: x[0]):
    data = list(since100(data))
    if not data:
        continue
    category = 'small' if data[-1][1] < 1000 else 'big'
    writer = csv.writer(open(f'{root}/{state}.csv', 'w'))
    for row in data:
        writer.writerow(row)
