# Favorite Directors
A Python app for parsing IMDb ratings csv and generating a favorite director list, based on number of movies watched and average rating.



### How it works:
#### 1. Export your IMDb ratings
Log in to imdb.com and navigate to your ratings page, then click on the export button on the top right corner (the export may take some time to complete).
![imdb ratings page with circled export button](static/imdb-export.png)

When the export is complete, you'll be able to download it as a file named something like e342343c(...).csv.

#### 2. Clone this repository
Standard github cloning, to run the program you'll need to have [Python](https://www.python.org/downloads/) installed.

#### 3. Run the app
```
python <path_to_app.py> <path_to_imdb-export.csv>
```

