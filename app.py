import sys
import csv 
import sqlite3

def main():
    if len(sys.argv) < 2:
        print("Usage: python app.py <imdb_csv_file>")
        return

    flag = 0 #none
    max_lines = -1 #default

    if len(sys.argv) > 2:
        if sys.argv[2] == "--print":
            flag = 1 
        elif sys.argv[2] == "--only-print":
            flag = 2
        else:
            print("Invalid flag. Options --print --only-print\nUsage: python app.py <imdb_csv_file> --flag")
            return
        if len(sys.argv) > 3 and isinstance(int(sys.argv[3]), int):
            if int(sys.argv[3]) <= 0:
                flag = 0
            else:
                max_lines = int(sys.argv[3])



 
    file_input = sys.argv[1]
    
    if not file_input.endswith(".csv"):
        print("Invalid file format, needs to be csv.\nUsage: python app.py <imdb_csv_file>")
        return

    db = sqlite3.connect("movies.db")
    cur = db.cursor()

    create_table(file_input, db, cur)
    data = analyze_results(cur)

    db.close()
    

    if flag != 2: #--only-print
        data_json = tuples_to_json(data)
        with open("favorite-directors.json", "w") as f:
            f.write(str(data_json))

    if flag != 0: #none 
        for i in range(len(data)):
            if i > max_lines and max_lines > 0:
                break

            row = data[i]
            if row[1] > 9:
                print(row[1], "movies with the average rating of", row[2], "  ----  ", row[0])
            else:
                print("", row[1], "movies with the average rating of", row[2], "  ----  ", row[0])



def create_table(file_input, db, cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS imdb (
        Const TEXT,
        Your_Rating INTEGER,
        Date_Rated TEXT,
        Title TEXT,
        Original_Title TEXT,
        URL TEXT,
        Title_Type TEXT,
        IMDb_Rating REAL,
        Runtime_mins INTEGER,
        Year INTEGER,
        Genres TEXT,
        Num_Votes INTEGER,
        Release_Date TEXT,
        Directors TEXT
    )
    """)

    # Read CSV and insert into the table
    with open(file_input, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
            INSERT INTO imdb VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["Const"],
                row["Your Rating"],
                row["Date Rated"],
                row["Title"],
                row["Original Title"],
                row["URL"],
                row["Title Type"],
                row["IMDb Rating"],
                row["Runtime (mins)"],
                row["Year"],
                row["Genres"],
                row["Num Votes"],
                row["Release Date"],
                row["Directors"]
            ))

    db.commit()

def analyze_results(cur):
    cur.execute("""
        SELECT
            CASE 
                WHEN Directors LIKE '%Joel Coen%' OR Directors LIKE '%Ethan Coen%' THEN 'Coen Brothers'
                ELSE Directors
            END AS Director_Group,
            COUNT(DISTINCT Const) AS num_movies,
            ROUND(AVG([Your_Rating]), 1) AS avg_rating
        FROM imdb
        WHERE Directors != ''
        GROUP BY Director_Group
        HAVING num_movies > 2
        ORDER BY num_movies DESC, avg_rating DESC;
        """)

    rows = cur.fetchall()
    #list of tuples: (director name, movie count, avg grade)
    

    return rows

def tuples_to_json(tuple_list):
    json = []
    for row in tuple_list:
        json.append(
                {
                    'director_name': row[0],
                    'movie_count': row[1],
                    'avg_rating': row[2]
                }
            )
    return json


if __name__ == "__main__":
    main()
