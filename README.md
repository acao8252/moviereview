
Movie Review is a movie score aggregator that pulls movie scores of movies currently playing in theaters from various websites:

- Rotten Tomatoes
- IMDB
- TMDB
- Metacritic

---

### Screenshots

##### Home Page

![homepage](/static/screenshots/homepage.png)

##### Contact Page

![contactpage](/static/screenshots/contactpage.png)

---

### Flask Help

Make sure to run the following in the terminal to prep the flask server:

Bash:

```bash
export FLASK_APP=app
export FLASK_ENV=development
```

Powershell:

```powershell
$env:FLASK_APP = "app"
$env:FLASK_ENV = "development"
```

Then run the following to start flask:

```bash
flask run
```

---

### Python Virtual Environment

This will help with making sure we are using the right version of the right package and keep things portable.

First install virtualenv:

```bash
pip install virtualenv
```

Then create a virtual environment:

```bash
virtualenv venv
```

Next activate it:

```bash
source venv/bin/activate
```

And while it's activated, install the packages (if you haven't already done so):

```bash
pip install -r requirements.txt
```

Deactivating the virtual environment is as simple as:

```bash
deactivate
```
