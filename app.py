import sys
import csv 
import sqlite3

def main():
    if len(sys.argv) < 2:
        print("Usage: python app.py <imdb_csv_file>")
        return
    
    file_input = sys.argv[1]
    
    db = sqlite3.connect("movies.db")
    cur = db.cursor()

    create_table(cur, db, file_input)
    data = analyze_results(cur)

    db.close()


def create_table(cur, db, file_input):
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

    # for row in rows:
    #     #print(row)
    #     if row[1] > 9:
    #         print(row[1], "movies with the average rating of", row[2], "  ----  ", row[0])
    #     else:
    #         print("", row[1], "movies with the average rating of", row[2], "  ----  ", row[0])


if __name__ == "__main__":
    main()