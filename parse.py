import re

regex = re.compile('([(\d\.)]+) - - '
    '\[(.*?)/(.*?)/(.*?) (.*?)\] '
    '"GET /s/(.*?) HTTP/1.1" (\d+) -')

month_names = [
  "Jan", "Feb", "Mar", "Apr",
  "May", "Jun", "Jul", "Aug",
  "Sep", "Oct", "Nov", "Dec"
  ]

months = {}
for x, y in enumerate(month_names):
    months[y] = x+1

with open('access.log', 'r') as f:
    for line in f.readlines():
        result = regex.match(line)
        if result:
            shorturl = result.groups()[5]
            day = result.groups()[1]
            month = months[result.groups()[2]]
            year = result.groups()[3]
            time = result.groups()[4]
            print "{0},{1}-{2}-{3} {4}".\
                format(shorturl, year, month, day, time)
