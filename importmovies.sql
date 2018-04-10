create table actors (
	"aid" integer primary key not null,
	"actor_name" text,
	"movie_credits" integer,
	"popularity" real
);

create table directors (
	"did" integer primary key not null,
	"director_name" text,
	"movie_credits" integer,
	"popularity" real
);

create table movies (
	"mid" integer primary key not null,
	"title" text, 
	"budget" real, 
	"action" boolean, 
	"adventure" boolean, 
	"animation" boolean, 
	"comedy" boolean,
	"crime" boolean, 
	"documentary" boolean, 
	"drama" boolean, 
	"family" boolean, 
	"fantasy" boolean, 
	"history" boolean, 
	"horror" boolean, 
	"music" boolean, 
	"mystery" boolean, 
	"romance" boolean, 
	"scifi" boolean, 
	"thriller" boolean,
	"war" boolean, 
	"western" boolean, 
	"original_language" text, 
	"production_companies" text,
	"release_date" date, 
	"revenue" real, 
	"runtime" integer, 
	"popularity" real, 
	"average_rating" real, 
	"num_votes" integer, 
	"actor_1" integer, 
	"actor_2" integer, 
	"actor_3" integer, 
	"actor_4" integer, 
	"actor_5" integer, 
	"actor_6" integer, 
	"actor_7" integer, 
	"actor_8" integer, 
	"actor_9" integer, 
	"actor_10" integer, 
	"director_1" integer,
	"director_2" integer, 
	"director_3" integer
);

create table oscars(
	"movie" text,
	"year" integer,
	"category" text,
	"nominee" boolean,
	"winner" boolean
);

.separator ","

/*As with the writing of the table, this is relative to my file stystem.  Replace the path with wherever you put your file.
  If you are on a Mac or Linux machine, start the path with / instead of C:/*/
.import "C:/Users/avg38/Documents/cornell/spring 2018/ds 4100/OscarPredictor/actors.csv" actors
.import "C:/Users/avg38/Documents/cornell/spring 2018/ds 4100/OscarPredictor/directors.csv" directors
.import "C:/Users/avg38/Documents/cornell/spring 2018/ds 4100/OscarPredictor/movies.csv" movies
.import "C:/Users/avg38/Documents/cornell/spring 2018/ds 4100/OscarPredictor/oscarsdata.csv" oscars

.headers on
.mode column

/* The backup command will save the database into the specified file.
   Note that, when I was doing this, I pulled up sqlite with no arguments
   in the command line, so all the actions are put into a temporary "default" database
   called main.  This is lost between sessions, so the backup command will put all
   of our changes into the hw9.db file in the location specified.  as with the 
   import statement above, replace the path with whatever location you like.*/
.backup main "C:/Users/avg38/Documents/cornell/spring 2018/ds 4100/OscarPredictor/moviedata.db"