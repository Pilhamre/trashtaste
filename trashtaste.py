from flask import Flask, redirect, render_template, request, url_for

import anime_images_api

import requests

import mal_scraper as mal

import random


users = {}


app = Flask(__name__)

@app.route('/')
def main():
	# WALLPAPER
	wallpaperImages = anime_images_api.Anime_Images()
	wallpaper = wallpaperImages.get_sfw('hug')

	return render_template('index.html', wallpaper=wallpaper)


@app.route('/critics/', methods=['GET', 'POST'])
def criticPost():
	global users

	uuid = request.args.get('client_id')

	if request.method == 'POST':
		user = request.form['user']
		users[uuid] = user
	else:
		user = users[uuid]

	anime = getAnime(user)
	
	# VIDEO
	video = getVideo(anime)
	while video == None:
		anime = getAnime(user)
		video = getVideo(anime)

	# WALLPAPER
	wallpaperImages = anime_images_api.Anime_Images()
	wallpaper = wallpaperImages.get_sfw('slap')

	return render(anime, wallpaper, video, user)


@app.route('/results/')
def results():
	return render_template('results.html')


def getAnime(user):
	data = mal.get_user_anime_list(user)

	i = random.randrange(0, len(data))
	anime = data[i]
	while anime['score'] == 0:
		i = random.randrange(0, len(data))
		anime = data[i]
	
	return anime


def getVideo(anime):
	animeId = anime['id_ref']

	url = f'https://api.jikan.moe/v4/anime/{animeId}/videos'

	r = requests.get(url)
	json = r.json()

	data = json['data']

	if len(data['promo']) == 0:
		return None
	promo = data['promo'][0]
	trailer = promo['trailer']

	ytId = trailer['youtube_id']

	videoURL = f'https://www.youtube.com/embed/{ytId}?controls=0&loop=1&playlist={ytId}&autoplay=1&mute=1&enablejsapi=1'

	return videoURL


def render(anime, wallpaper, video, user):
	return render_template('critics.html', anime=anime, wallpaper=wallpaper, video=video, user=user)


if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0')