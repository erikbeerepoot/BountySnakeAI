# battlesnake-python

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

#### You will need...

* a working Python 2.7 development environment ([getting started guide](http://hackercodex.com/guide/python-development-environment-on-mac-osx/))
* experience [deploying Python apps to Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
* [pip](https://pip.pypa.io/en/latest/installing.html) to install Python dependencies
* redis

## Running the Snake Locally

1) [Fork this repo](https://github.com/sendwithus/battlesnake-python/fork).

2) Clone repo to your development environment:
```
git clone git@github.com:username/battlesnake-python.git
```

3) Install dependencies and set up current dir as a package dir, using [pip](https://pip.pypa.io/en/latest/installing.html):
```
pip install -e . -r requirements.txt
```

4) Run local server:
```
redis-server

python -m bountysnakeai.main
```

5) Test client in your browser: [http://localhost:8080](http://localhost:8080).

5b) Run test suite:
```
nosetests -v
```

## Deploying to Heroku

This snake automatically deploys to heroku from master, and for each pull request. You can find it at:

` http://bsnake.herokuapp.com`

## Phases
The snake has three phases, and are managed in our redis db.

1) hiding - the snake is attempting to hide in on of the corners

2) circle - the snake is currently circling in one of the board corners

3) food - the snake is currently getting food
