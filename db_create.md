### Create Dababase and User/Password
```bash
$ mysql -u root -p
mysql> create database apps character set utf8 collate utf8_bin;
mysql> create user 'apps'@'localhost' identified by 'password';
mysql> grant all privileges on apps.* to 'apps'@'localhost';
mysql> flush privileges;
mysql> quit;
```

### Assign Database to App
```bash
# Set environment variable
$ DATABASE_URL=mysql://apps:password@localhost/apps ./db_create.py
```

### Start MySQL Locally
```bash
# Mac
$ sudo /usr/local/mysql/support-files/mysql.server start
$ sudo /usr/local/mysql/support-files/mysql.server stop

# Linux
$ /etc/init.d/mysqld start
# or service mysqld start
# or service mysql start
```

### Testing MySQL in Python
```python
from app import db, models
import datetime

# add users
u = models.User(username='john', email='john@email.com')
db.session.add(u)
db.session.commit()

u = models.User(username='susan', email='susan@email.com')
db.session.add(u)
db.session.commit()

users = models.User.query.all()
for u in users:
    print u.id, u.username, u.timestamp

# add link
u = models.User.query.get(1)
l = models.Link(longurl='mylongurl', shorturl='myshorturl', timestamp=datetime.datetime.utcnow(), author=u)
db.session.add(l)
db.session.commit()

u = models.User.query.get(1)

links = u.links.all()
for l in links:
    print l.id, l.author.username, l.long_url, l.short_url
```