import requests

def test():
	url = 'https://www.imdb.com/showtimes/location'
	try:
		connect = requests.get(url)
		print("CONNECTED")
		return True
	except Exception as e:
		print("OOF")
		return False
