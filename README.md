## Pwn The Jewels
### Usage
#### Pipenv
```
$ sudo apt install python3-pip
$ sudo pip3 install pipenv
$ sudo pipenv install
$ pipenv shell
$ pipenv run bot
```

#### Docker
```
$ sudo apt install docker docker-compose
$ sudo groupadd docker
$ sudo usermod -aG docker ${USER}
$ su -s ${USER}
$ docker build -t pwnthejewels .
$ docker run pwnthejewels &
```
