import csv
import itertools
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


# TODO MI jumps to 334; interpolate fractional start day
def since100(state_day_count):
    start = None
    for _, day, count in state_day_count:
        if start is None and count >= 100:
            start = day
        if start is not None:
            yield day - start, count


_, root = sys.argv
os.mkdir(root)

for state, data in itertools.groupby(sorted(cumulative(sys.stdin)), lambda x: x[0]):
    data = list(since100(data))
    if not data:
        continue
    category = 'small' if data[-1][1] < 1000 else 'big'
    writer = csv.writer(open(f'{root}/{state}.csv', 'w'))
    for row in data:
        writer.writerow(row)
