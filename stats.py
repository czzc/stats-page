from flask import Flask, render_template, jsonify
import wowapi
import wowapi.utility
import json 

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
def getStats():
	# WoW API Stats
	wowData = {}
	api = wowapi.API(app.config['WOW_API_KEY'])
	#char = api.character('madoran', 'cazzc', ['titles', 'mounts', 'pets', 'feed'])
	with open('cazzcInfo.json') as data_file:
		char = json.load(data_file)
	wowData['name'] = char['name']
	wowData['realm'] = char['realm']
	wowData['class'] = char['class']
	wowData['gender'] = getGender(char['gender'])
	wowData['level'] = char['level']
	wowData['achievements'] = char['achievementPoints']
	wowData['mounts'] = getTotalMounts(char['mounts'])
	wowData['pets'] = getTotalPets(char['pets'])
	wowData['title'] = getActiveTitle(char['titles'], wowData['name'])
	wowData['profilePic'] = char['thumbnail']
	wowData['miscStats'] = getMiscStats(char['statistics']['subCategories'])
	wowData['pronoun'] = genPronoun(wowData['gender'])
	print(wowData)

	return render_template('stats.html', character=wowData)


def getActiveTitle(titles, name):
	title = next ((title['name'] for title in titles if 'selected' in title), '%s')
	title = title.replace('%s', name)
	return title

def getMiscStats(stats):
	miscStats = {}
	for stat in stats:
		if stat['id'] == 130:
			for stat1 in stat['subCategories']:
				if stat1['id'] == 147:
					miscStats['exaltedFactions'] = stat1['statistics'][0]['quantity']
				if stat1['id'] == 145:
					for stat2 in stat1['statistics']:
						if stat2['id'] == 812:
							miscStats['healthstonesUsed'] = stat2['quantity']
		
		if stat['id'] == 15253:
			for stat1 in stat['statistics']:
				if stat1['id'] == 10181:
					miscStats['garrisonMissions'] = stat1['quantity']

		if stat['id'] == 134:
			for stat1 in stat['statistics']:
				if stat1['id'] == 349:
					miscStats['flightPathsTaken'] = stat1['quantity']
		if stat['id'] == 133:
			for stat1 in stat['statistics']:
				if stat1['id'] == 98:
					quests = stat1['quantity']
				if stat1['id'] == 97:
					dailyQuests = stat1['quantity']

		if stat['id'] == 122:
			for stat1 in stat['subCategories']:
				if stat1['id'] == 127:
					for stat2 in stat1['statistics']:
						if stat2['id'] == 801:
							miscStats['rezdBySoulstone'] = stat2['quantity']

	totQuests = quests + dailyQuests
	miscStats['totalQuests'] = totQuests
	return miscStats

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

def genPronoun(charGender):
	if charGender == 'Male':
		return 'he'
	else:
		return 'she'

def getFaction(charFaction):
	if str(charFaction) not in FACTIONS:
			return 'unknown faction: {0}'.format(charFaction)
	else:
		for i in FACTIONS:
			if str(charFaction) == i:
				return FACTIONS[i]

if __name__ == "__main__":
	app.run(host='0.0.0.0')

