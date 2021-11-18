from app import app

def test():
    flask = app.test_client()
    response = flask.get('/', content_type='html/text')
    if response.status_code == 200:
        return True
    else:
        return False
