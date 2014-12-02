# bitly-clone

## Features
* **User profiles:** Users can create accounts with usernames and passwords, and can also track the number of clicks per link. Users can also create links without having to create an account.

* **MySQL database:** We've implemented a MySQL database with two linked tables : `user` and `link`.

* **Wayback machine API integration:** When creating a link, users will also get a link to visit their url from a random point in the past.

* **Mobile ready:** Yes.


## Setup

**0. Create virtualenv, clone repo/checkout branch, install requirements:**

```bash
$ mkvirtualenv bitly

$ git clone git@github.com:semerj/bitly-clone.git
$ cd bitly-clone
$ git checkout project_2

$ pip install -r requirements.txt
```

**1. Initialize database:** create the `apps` database (1st instance) and `apps` user with password `password`.

```bash
$ mysql -u root -p
mysql> create database apps character set utf8 collate utf8_bin;
mysql> create user 'apps'@'localhost' identified by 'password';
mysql> grant all privileges on apps.* to 'apps'@'localhost';
mysql> flush privileges;
mysql> quit;
```

**2. Set database environment variable:** if using different username/password in previous step, substitute username (1st instance) and password in `config.py`.

```bash
$ DATABASE_URL=mysql://apps:password@localhost/apps ./db_create.py
```

**3. Start MySQL Locally**
```bash
# Mac
$ sudo /usr/local/mysql/support-files/mysql.server start
# or Linux
$ /etc/init.d/mysqld start
```

**4. Execute run.py script:** 
```bash
$ ./run.py
```
Then go to localhost:5000 (or 127.0.0.1:5000) in browser.

### Group members:
* Wenqin Chen
* Daniel Brenners
* Bryan Morgan
* John Semerdjian

