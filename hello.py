from flask import Flask, render_template
import wowapi
import wowapi.utility

app = Flask(__name__)
app.config.from_object('config')

@app.route("/stats")
def wowStats():
	api = wowapi.API(app.config['WOW_API_KEY'])
	char = api.character('madoran', 'cazzc')
	#print(type(char))
	profilePic = char["thumbnail"]
	profilePic = profilePic.replace("avatar.jpg", "profilemain.jpg")
	money = wowapi.utility.format_currency(9872397)
	return render_template('stats.html', character=char, altImage=profilePic, money=money)
	
if __name__ == "__main__":
	app.run(host='0.0.0.0')
