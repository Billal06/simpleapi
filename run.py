from flask import *
from bs4 import BeautifulSoup as bs
import requests, os, re, json
app = Flask(__name__)

# Var Status
sukses = "success"
gagal = "failed"
error = "error"

# FREE PROXY
@app.route("/api/freeproxy")
def freeproxy():
	config = {}
	config2 = {}
	r = requests.get("https://api.getproxylist.com/proxy").text
	j = json.loads(r)
	ip = j["ip"]
	port = j["port"]
	pro = j["protocol"]
	speed = j["downloadSpeed"]
	# Menampung Data Json 2
	config2["ip"] = ip
	config2["port"] = port
	config2["protocol"] = pro
	config2["speedDownload"] = speed

	# Menampung Data Json 1
	config["status"] = sukses
	config["result"] = json.loads("".join(json.dumps(config2)))
	return "".join(json.dumps(config))

# YOUTUBE MP3 DOWNLOADER
@app.route("/api/ytmp3")
def ytmp3():
	config = {}
	config2 = {}
	url = request.args.get("url")
	if not url:
		config["status"] = error
		config["pesan"] = "Parameter URL tidak di temukan"
	else:
		if "warch?v=" in url:
			id = re.findall('v=(.*)$',url)
		elif "youtube.com" in url:
			id = re.findall('.com/(.*)$',url)
		elif "youtu.be" in url:
			id = re.findall(".be/(.*)$",url)
		else:
			config["status"] = error
			config["pesan"] = "Sepertinya URL tidak mensupport"
			return "".join(json.dumps(config))
		get = requests.get('https://www.download-mp3-youtube.com/api/?api_key=NDI2ODYyNzU4&format=mp3&logo=1&video_id='+id[0])
		b = bs(get.text, "html.parser")
		f = b.find('a',{'id':'downloadButton'})['href']
		# Menampung data json 2
		config2["url"] = url
		config2["mp3"] = f

		# Menampung data json 1
		config["status"] = sukses
		config["result"] = json.loads("".join(json.dumps(config2)))
	return "".join(json.dumps(config))

# FACEBOOK VIDEO DOWNLOADER
@app.route("/api/fbvid")
def fbvid():
	config = {}
	config2 = {}
	url = request.args.get("url")
	if not url:
		config["status"] = error
		config["pesan"] = "Parameter URL tidak ditemukan"
	else:
		try:
			r = requests.get(url)
			f = re.search(r'\"(http[s]\:\/\/video.*?\.mp4\?.*?)\"',r.text)
			if f:
				urlvid = f.group(1).replace(";","&")
				config2["url"] = url
				config2["urlvid"] = urlvid
				config["status"] = sukses
				config["result"] = json.loads("".join(json.dumps(config2)))
			else:
				config["status"] = gagal
				config["pesan"] = "Sepertinya Video tidak ditemukan"
		except requests.exceptions.MissingSchema:
			config["status"] = error
			config["pesan"] = "Silahkan Masukna URL dengan benar"
	return "".join(json.dumps(config))
# IP TRACK
@app.route("/api/track")
def track():
	config = {}
	config2 = {}
	config3 = {}
	ip = request.args.get("ip")
	key = ["2388107e74e7fe5424554967771b568b","7a1afbf9b63efdf5bdb30a08a736673c229b3ea738e667e0d259c135"]
	urls = ["http://api.ipstack.com/","http://ip-api.com/json/","http://free.ipwhois.io/json/","https://api.ipdata.co/"]
	r = requests.get(urls[0]+ip+"?access_key="+key[0]).text
	j = json.loads(r)
	# INFO IP
	try:
		type = j["type"]
	except:
		type = None
	try:
		negara = j["country"]
	except:
		negara = None
	try:
		code = j["country_code"]
	except:
		code = None
	try:
		benua = j["continent_name"]
	except:
		benua = None
	try:
		telp = j["location"]["calling_code"]
	except:
		telp = None
	r2 = requests.get(urls[1]+ip+"?fields=mobile").text
	j2 = json.loads(r2)
	try:
		mobile = j2["mobile"]
	except:
		mobile = None
	# INFO TELP
#	zona = j3["timezone"]
#	gmt = j3["timezone_gmt"]
	config2["type"] = type
	config2["country"] = negara
	config2["code"] = code
	config2["continent_name"] = benua
	config2["calling_code"] = telp
	# Tampilkan
	js = json.loads(json.dumps(config2))
	config["status"] = sukses
	config["result"] = js
	return "".join(json.dumps(config))

# INSTAGRAM VIDEO DOWNLOADER
@app.route("/api/igdown")
def igdown():
	config = {}
	config2 = {}
	url = request.args.get("url")
	if not url:
		config["status"] = error
		config["pesan"] = "Parameter URL tidak ditemukan"
	else:
		try:
			r = requests.get(url)
#		if r.status_code == 200:
			b = bs(r.text, "html.parser")
			for f in b.findAll("meta"):
				if f.get("property") == "og:video:secure_url":
					config2["url"] = url
					config2["urlvid"] = f.get("content")
					config["status"] = sukses
					config["result"] = config2
					config["pesan"] = "Video Di Temukan"
					del config["pesan"]
					break
				else:
					config["status"] = gagal
					config["pesan"] = "Sepertinya video tidak ditemukan"
		except requests.exceptions.MissingSchema:
			config["status"] = error
			config["pesan"] = "Silahkan Masukan URL dengan benar"
	j = json.dumps(config)
	return j

# JIKA PAGE ERROR MAKA:
@app.errorhandler(404)
def not_found(e):
	return render_template("error.html")

# JIKA KLIK TOOLS MAKA:
@app.route("/tools")
def tools():
	return render_template("tools.html")

# JIKA KLIK ABOUT MAKA:
@app.route("/about")
def about():
	return render_template("about.html")

# JIKA KLIK TUTORIAL MAKA:
@app.route("/tutorial")
def tutorial():
	return render_template("tutor.html")

# INDEX AWAL
@app.route("/")
def index():
	return render_template("index.html")

if __name__ == '__main__':
	app.run(host="0.0.0.0",port=os.environ.get("PORT"),debug=True)
