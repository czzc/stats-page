from flask import Flask, render_template, jsonify
import wowapi
import wowapi.utility

app = Flask(__name__)
app.config.from_object('config')
app.debug= True

GENDERS = {
	'0' : 'Male',
	'1' : 'Female'
}

FACTIONS = {
	'0' : 'Alliance',
	'1' : 'Horde'
}

@app.route("/stats")
def wowStats():
	api = wowapi.API(app.config['WOW_API_KEY'])
	char = api.character('madoran', 'cazzc', ['titles', 'mounts', 'pets', 'feed'])
	profilePic = char["thumbnail"]
	profilePic = profilePic.replace("avatar.jpg", "profilemain.jpg")
	money = wowapi.utility.format_currency(9872397)
	title = getActiveTitle(char['titles'], char['name'])
	mounts = getTotalMounts(char['mounts'])
	pets = getTotalPets(char['pets'])
	char['gender'] = getGender(char['gender'])
	char['faction'] = getFaction(char['faction'])	
	print(char['faction'])
	return render_template('stats.html', character=char, mounts=mounts, pets=pets, altImage=profilePic, money=money, title=title)


def getActiveTitle(titles, name):
	title = next ((title['name'] for title in titles if 'selected' in title), '%s')
	title = title.replace('%s', name)
	return title

def getTotalMounts(mounts):
	return mounts['numCollected']	

def getTotalPets(pets):
	return pets['numCollected']

def getGender(charGender):
	if str(charGender) not in GENDERS:
			return 'unknown gender: {0}'.format(charGender)
	else:
		for i in GENDERS:
			if str(charGender) == i:
				return GENDERS[i]

def getFaction(charFaction):
	if str(charFaction) not in FACTIONS:
			return 'unknown faction: {0}'.format(charFaction)
	else:
		for i in FACTIONS:
			if str(charFaction) == i:
				return FACTIONS[i]

if __name__ == "__main__":
	app.run(host='0.0.0.0')
