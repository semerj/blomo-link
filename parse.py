import re

'''
for use in cron job:

output stdout/stderr to logs.txt every hour

$ crontab -e
* */1 * * *  python ~/bitly-clone/parse.py > ~/bitly-clone/logs/logs.txt 2>&1

'''

access_logs = 'access.log'

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
    months[y] = x + 1

def main():
    with open(access_logs, 'r') as logs:
        for line in logs:
            result = regex.match(line)
            if result:
                shorturl = result.groups()[5]
                day = result.groups()[1]
                month = months[result.groups()[2]]
                year = result.groups()[3]
                time = result.groups()[4]
                print "{0}, {1}-{2}-{3} {4}".\
                    format(shorturl, year, month, day, time)

if __name__ == '__main__':
    main()

