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
#we are limiting the credits to just the top 6 billed actors.
#I would experiment and get all of the actors' credits, but even modest estimates
#of the number of api calls puts the total scraping time at about 52 hours.

with open('movies.csv', 'w', newline='') as moviefile:
	moviewriter = csv.writer(moviefile, delimiter = ",")
	headings = ["mid", "title", "budget", "action", "adventure", "animation", "comedy",
	            "crime", "documentary", "drama", "family", "fantasy", "history", 
	            "horror", "music", "mystery", "romance", "scifi", "thriller", 
	            "war", "western", "original_language", "production_companies",
	            "release_date", "revenue", "runtime", "popularity", "average_rating", 
	            "num_votes", "directors", "total_movie_credits_directors", "actors", "total"]
	moviewriter.writerow(headings)
	#For each year in in the range [2001,2018)
	for year in range(2001, 2018):
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
				mid = movies[movie]['id']
				movieurl = "https://api.themoviedb.org/3/movie/"+str(mid)+"?api_key=228cf3748fd87af5cbdcc0249cb68440&language=en-US"
				payload = "{}"
				response = requests.get(movieurl, params = payload)
				time.sleep(.25)
				mdata = json.loads(response.text)
				creditsurl = "https://api.themoviedb.org/3/movie/"+str(mid)+"/credits?api_key=228cf3748fd87af5cbdcc0249cb68440"
				payload = "{}"
				response = requests.get(credits, params = payload)
				time.sleep(.25)
				cdata = json.loads(response.text)
				print(mdata['title'])
				print(movie)

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
					[mrelease]+[mrevenue]+[mruntime]+[mpop]+[mvoteavg]+[mvotes])
			nexturl = "https://api.themoviedb.org/3/discover/movie?api_key=228cf3748fd87af5cbdcc0249cb68440&language=en-US&region=US&certification_country=US&certification.lte=R&include_adult=false&include_video=false&page="+str(page)+"&primary_release_year="+str(year)+"&year="+str(year)
			payload = "{}"
			response = requests.get( nexturl, params=payload)
			time.sleep(.25)
			data = json.loads(response.text)
			movies = data['results']