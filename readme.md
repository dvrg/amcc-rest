# How To

## Installation

```
git clone https://github.com/dvrg/amcc-rest.git
cd amcc-rest
virtualenv venv
pip install -r requirements.txt
```

## Preparation

make env variable, and assign value based config.py

```
touch .env
```

## Create Database

```
flask shell
db.create_all()
ctrd + D
flask deploy
```

## Upgrade & Run

```
flask run
```
