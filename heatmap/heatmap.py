import openmeteo_requests
import requests_cache
from retry_requests import retry
import colorsys
from ansi.color.rgb import rgb256
from ansi.colour.fx import reset

class Heatmap:
	def __init__(self, topLeft, bottomRight, resolution):
		self.res = resolution

		self.x1, self.y1 = topLeft
		self.x2, self.y2 = bottomRight

	def genGrid(self):
		xDiff = self.x2 - self.x1
		yDiff = self.y2 - self.y1

		self.lats = []
		self.longs = []

		for i in range(self.res):
			for j in range(self.res):
				lat = self.y1 + (yDiff / self.res) * i
				long = self.x1 + (xDiff / self.res) * j
				self.lats.append(lat)
				self.longs.append(long)


	def fetchData(self):
		n = 120
		pairs = list(zip(self.lats, self.longs))
		requests = [pairs[i:i + n] for i in range(0, len(pairs), n)]

		self.responses = []
		for index, chunk in enumerate(requests):
			print(f"fetching {index}/{len(requests)}{" " * 5}", end="\r")
			cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
			retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
			openmeteo = openmeteo_requests.Client(session=retry_session)
			lats, longs = zip(*chunk)
			params = {
				"latitude": lats,
				"longitude": longs,
				"current": "temperature_2m",
			}
			self.responses.extend(openmeteo.weather_api("https://api.open-meteo.com/v1/forecast", params=params))
			# TODO: space requests to avoid rate limiting

	def renderMap(self):
		for i, response in enumerate(self.responses):
			if i % (self.res) == 0 and i != 0:
				print()
			cTemp = response.Current().Variables(0).Value()
			fTemp = cTemp * 9/5 + 32

			hlsColor = (cTemp / 10, 0.5, 0.5)
			rgbColor = colorsys.hls_to_rgb(*hlsColor)

			cell = (rgb256(*(round(c * 100) for c in rgbColor)), '██', reset)
			# cell = (rgb256(*(round(c * 100) for c in rgbColor)), f"[{round(cTemp)}]", reset)
			print(''.join(map(str, cell)), end="")
