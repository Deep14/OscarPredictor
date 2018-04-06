import csv
import requests
import time
import json

#api.API_KEY = '228cf3748fd87af5cbdcc0249cb68440'

#We will use the api wrapper tmdbsimple to scrape the tmdb api for data.
#Note that, while the Academy awards have been around since 1927,
#The Animated Feature Film category has only existed since 2001 (the 75th awards).  Thus,
#We will use this year as our oldest year for consideration of movies.
#Furthermore, we will limit our data to only movies with ratings of R or lower - 
#Only 4 X or NC-17 rated movies have been nominated to any award category since
#the inception of the Academy awards - Midnight Cowboy(1970), A Clockwork Orange(1972),
#Last Tango In Paris(1974), and Blue Valentine (2010).  Of these, only Last Tango
#In Paris retains its NC-17 rating - all other were downgraded to an R rating.
#In fact, Blue Valentine was almost denied its Oscar nomination, only entering
#the nomination list after its rating was downgraded.  Note that the api
#parameter for the certification also requires a certification country.  A side effect
#of using this field means that we will limit our scraping to only films reviewed
#by the MPAA - which is exactly what we want. 
#Since we are also getting number of movie credits for directors and actors, we
#are looking at a looot of requests to the api.
#just to keep the amount of time this thing has to run to a reasonable amount,
#we are limiting the credits to just the top 10 billed actors.
#I would experiment and get all of the actors' credits, but even modest estimates
#of the number of api calls puts the total scraping time at about 52 hours.
#Furthermore, for most movies, after 10 actors you begin getting into 
#one-off characters and bit roles, so there is a bit of a diminishing return here.
#Most movies are not on the scale of the Avengers, so this should be a safe bet.

actorids = []
directorids = []

with open('movies.csv', 'w', newline='') as moviefile:
	moviewriter = csv.writer(moviefile, delimiter = ",")
	#write the headings to the movies csv
	headings = ["mid", "title", "budget", "action", "adventure", "animation", "comedy",
	            "crime", "documentary", "drama", "family", "fantasy", "history", 
	            "horror", "music", "mystery", "romance", "scifi", "thriller", 
	            "war", "western", "original_language", "production_companies",
	            "release_date", "revenue", "runtime", "popularity", "average_rating", 
	            "num_votes", "actor_1", "actor_2", "actor_3", "actor_4", "actor_5", 
	            "actor_6", "actor_7", "actor_8", "actor_9", "actor_10", "director_1",
	            "director_2", "director_3"]
	moviewriter.writerow(headings)
	#For each year in in the range [2001,2018)
	for year in range(2001, 2018):
		#discover movies fitting the criteria in the current year
		initurl = "https://api.themoviedb.org/3/discover/movie?api_key=228cf3748fd87af5cbdcc0249cb68440&language=en-US&region=US&certification_country=US&certification.lte=R&include_adult=false&include_video=false&page=1&primary_release_year="+str(year)+"&year="+str(year)
		payload = "{}"
		response = requests.get(initurl, params=payload)
		time.sleep(.25)
		data = json.loads(response.text)
		numpages = data['total_pages']
		numresults = data['total_results']
		movies = data['results']
		#for each page of data that matches the search
		for page in range(2, numpages+1):
			reslimit = numresults%20 if page == numpages else 20
			#for each result on the page
			for movie in range(0, reslimit):
				#get data for a specific movie, given by mid
				mid = movies[movie]['id']
				movieurl = "https://api.themoviedb.org/3/movie/"+str(mid)+"?api_key=228cf3748fd87af5cbdcc0249cb68440&language=en-US"
				payload = "{}"
				response = requests.get(movieurl, params = payload)
				time.sleep(.25)
				mdata = json.loads(response.text)
				#get credits for that movie
				creditsurl = "https://api.themoviedb.org/3/movie/"+str(mid)+"/credits?api_key=228cf3748fd87af5cbdcc0249cb68440"
				payload = "{}"
				response = requests.get(creditsurl, params = payload)
				time.sleep(.25)
				cdata = json.loads(response.text)
				castmems = cdata['cast']
				crewmems = cdata['crew']
				print(mdata['title'])
				print(movie)

				#First add in actor and director ids into a list of discovered ids
				maids = []
				castsize = 10 if len(castmems) > 10 else len(castmems)
				for cast in range(0,castsize):
					aid = castmems[cast]['id']
					if not aid in actorids:
						actorids.append(aid)
					maids.append(aid)

				if len(maids) < 10:
					for empty in range(len(maids), 10):
						maids.append(-1)

				daids = []
				for crew in crewmems:
					if(crew['job']=="Director" and len(daids) < 3):
						did = crew['id']
						if not did in directorids:
							directorids.append(did)
						daids.append(did)
				if len(daids) < 3:
					for empty in range(len(daids), 3):
						daids.append(-1)

				mtitle = mdata['title']
				mbudget = mdata['budget']
				mgenres = ""
				for g in mdata['genres']:
					mgenres = mgenres+g['name']+", "
				maction = 1 if "Action" in mgenres else 0
				madventure = 1 if "Adventure" in mgenres else 0
				manimation = 1 if "Animation" in mgenres else 0
				mcomedy = 1 if "Comedy" in mgenres else 0
				mcrime = 1 if "Crime" in mgenres else 0
				mdocumentary = 1 if "Documentary" in mgenres else 0
				mdrama = 1 if "Drama" in mgenres else 0
				mfamily = 1 if "Family" in mgenres else 0
				mfantasy = 1 if "Fantasy" in mgenres else 0
				mhistory = 1 if "History" in mgenres else 0
				mhorror = 1 if "Horror" in mgenres else 0
				mmusic = 1 if "Music" in mgenres else 0
				mmystery = 1 if "Mystery" in mgenres else 0
				mromance = 1 if "Romance" in mgenres else 0
				mscifi = 1 if "Science Fiction" in mgenres else 0
				mthriller = 1 if "Thriller" in mgenres else 0
				mwar = 1 if "War" in mgenres else 0
				mwestern = 1 if "Western" in mgenres else 0
				if("TV Movie" in mgenres):
					continue #Straight to TV movies aren't considered for Oscars
				moriglang = mdata['original_language']
				mprodcos = ""
				for p in mdata['production_companies']:
					mprodcos = mprodcos + p['name']+ " and "
				mrelease = mdata['release_date']
				mrevenue = mdata['revenue']
				mruntime = mdata['runtime']
				mpop = mdata['popularity']
				mvoteavg = mdata['vote_average']
				mvotes = mdata['vote_count']
				moviewriter.writerow([mid]+[mtitle]+[mbudget]+[maction]+[madventure]+
					[manimation]+[mcomedy]+[mcrime]+[mdocumentary]+[mdrama]+[mfamily]+
					[mfantasy]+[mhistory]+[mhorror]+[mmusic]+[mmystery]+[mromance]+
					[mscifi]+[mthriller]+[mwar]+[mwestern]+[moriglang]+[mprodcos]+
					[mrelease]+[mrevenue]+[mruntime]+[mpop]+[mvoteavg]+[mvotes]+[maids]+[daids])
			nexturl = "https://api.themoviedb.org/3/discover/movie?api_key=228cf3748fd87af5cbdcc0249cb68440&language=en-US&region=US&certification_country=US&certification.lte=R&include_adult=false&include_video=false&page="+str(page)+"&primary_release_year="+str(year)+"&year="+str(year)
			payload = "{}"
			response = requests.get( nexturl, params=payload)
			time.sleep(.25)
			data = json.loads(response.text)
			movies = data['results']

with open('directors.csv', 'w', newline='') as dirfile:
	dirwriter = csv.writer(dirfile, delimiter = ",")
	headings = ["did", "director_name", "movie_credits", "popularity"]
	dirwriter.writerow(headings)
	for director in directorids:
		personurl = "https://api.themoviedb.org/3/person/"+str(director)+"?api_key=228cf3748fd87af5cbdcc0249cb68440&language=en-US"
		payload = "{}"
		response = requests.get(personurl, params = payload)
		time.sleep(.25)
		ddata = json.loads(response.text)
		dname = ddata['name']
		dpop = ddata['popularity']
		pcreditsurl = "https://api.themoviedb.org/3/person/"+str(director)+"/movie_credits?api_key=228cf3748fd87af5cbdcc0249cb68440&language=en-US"
		payload = "{}"
		response = requests.get(pcreditsurl, params = payload)
		time.sleep(.25)
		creditsdata = json.loads(response.text)
		crewcredits = len(creditsdata['crew'])
		dirwriter.writerow([director]+[dname]+[crewcredits]+[dpop])

with open('actors.csv', 'w', newline='') as actorfile:
	actorwriter = csv.writer(actorfile, delimiter = ",")
	headings = ["aid", "actor_name", "movie_credits", "popularity"]
	dirwriter.writerow(headings)
	for actor in actorids:
		personurl = "https://api.themoviedb.org/3/person/"+str(actor)+"?api_key=228cf3748fd87af5cbdcc0249cb68440&language=en-US"
		payload = "{}"
		response = requests.get(personurl, params = payload)
		time.sleep(.25)
		adata = json.loads(response.text)
		aname = adata['name']
		apop = adata['popularity']
		pcreditsurl = "https://api.themoviedb.org/3/person/"+str(actor)+"/movie_credits?api_key=228cf3748fd87af5cbdcc0249cb68440&language=en-US"
		payload = "{}"
		response = requests.get(pcreditsurl, params = payload)
		time.sleep(.25)
		creditsdata = json.loads(response.text)
		castcredits = len(creditsdata['cast'])
		dirwriter.writerow([actor]+[aname]+[castcredits]+[apop])