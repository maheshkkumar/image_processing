from PIL import Image
from PIL.ExifTags import TAGS

class Geocode():

	def __init__(self, url):
		self.url = url

	def get_exif(self):
		rootUrl = "/home/mahesh/visual_lifelog/image_processing/static/images/"
		image_url = rootUrl+self.url
		image = Image.open(image_url)
		image_info = image._getexif()
		image_geodata = {}
			
		for tag, value in image_info.items():
			decoded = TAGS.get(tag, tag)
			image_geodata[decoded] = value
		return image_geodata

	def get_latitude_and_longitude(self, image_geodata):
		lat = [float(x)/float(y) for x, y in image_geodata['GPSInfo'][2]]
		latref = image_geodata['GPSInfo'][1]
		lon = [float(x)/float(y) for x, y in image_geodata['GPSInfo'][4]]
		lonref = image_geodata['GPSInfo'][3]
		lat = lat[0] + lat[1]/60 + lat[2]/3600
		lon = lon[0] + lon[1]/60 + lon[2]/3600
		if latref == 'S':
				lat = -lat
		if lonref == 'W':
				lon = -lon
		return lat, lon, latref, lonref