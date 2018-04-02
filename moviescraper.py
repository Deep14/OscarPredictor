import csv
import tmdbsimple as api
import time

api.API_KEY = '9a49bb89df2752dfce997548a3085631'

with open('directors.csv', 'r', newline='') as creditfile:
	with open('dircredits.csv', 'w', newline='') as cf:
		creditreader = csv.reader(creditfile, delimiter = ",")
		creditwriter = csv.writer(cf, delimiter = ",")
		count = 0
		for row in creditreader:
			count = count + 1
			print(count)
			if(count > 20):
				time.sleep(6)
			row[2] = int(row[2])
			director = api.People(row[2])
			print(director.info()["name"])
			mc = director.movie_credits()
			credits = len(mc["crew"])
			print(credits)
			creditwriter.writerow([row[0]]+[row[1]]+[row[2]]+[credits])
