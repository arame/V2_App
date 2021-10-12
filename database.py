import sqlite3 as lite
import sys
import pandas as pd
from helper import Helper
from config import Hyper

class Data:
    TABLE_PARAMETER = "{TABLE_PARAMETER}"
    DROP_TABLE_SQL = f"DROP TABLE {TABLE_PARAMETER};"
    GET_TABLES_SQL = "SELECT name FROM sqlite_master WHERE type='table';"
    display_tweet_table = "select * from tweets;"
        
    def __init__(self) -> None:
        self.country_file = Hyper.countries_file
        self.db = Hyper.db
        self.create_connection()
        Helper.printline("Database opened successfully")  

    def create_schema(self):
        try:
            self.df_countries = pd.read_csv('Countries.csv', encoding='latin-1', index_col=False, dtype='unicode')
        except Exception as e:
            sys.exit(f"Error with reading the file: {e}")   
                  
        if Hyper.IsStartAgain:
            self.delete_all_tables()
                
        self.create_all_tables()
        if Hyper.IsLoadCountries:
            table_name = "countries"
            self.load_table(self.df_countries, table_name)
            self.display_table(self.display_country_table, table_name)
        if Hyper.IsLoadUserLocations:
            table_name = "user_locations"
            self.df_user_locations = self.df_countries.copy(deep=True)
            self.df_user_locations = self.df_user_locations.rename(columns = {"country": "user_location"})
            self.load_table(self.df_user_locations, table_name)
            self.display_table(self.display_user_locations_table, table_name)
            
    def create_all_tables(self):
        self.create_countries_table_on_database()
        self.create_user_locations_table_on_database()
        self.create_tweet_table_on_database() 
         
    def delete_all_tables(self):
        tables = self.get_tables()
        self.delete_tables(tables)
    
    def get_tables(self):
        c = self.con.cursor()
        c.execute(Data.GET_TABLES_SQL)
        tables = c.fetchall()
        c.close()
        return tables

    def delete_tables(self, tables):
        c = self.con.cursor()
        for table, in tables:
            sql = Data.DROP_TABLE_SQL.replace(Data.TABLE_PARAMETER, table)
            c.execute(sql)
        c.close()
    
    def create_user_locations_table_on_database(self):
        self.sql_create_user_locations_table = """ CREATE TABLE IF NOT EXISTS user_locations (
                                id integer PRIMARY KEY,
                                code text NOT NULL,
                                user_location text NOT NULL
                            ); """
        self.create_table(self.sql_create_user_locations_table)
        Helper.printline("User Locations table successfully created")
        self.display_user_locations_table = "select * from user_locations;"

    def create_countries_table_on_database(self):
        self.sql_create_country_table = """ CREATE TABLE IF NOT EXISTS countries (
                                id integer PRIMARY KEY,
                                code text NOT NULL,
                                country text NOT NULL
                            ); """
        self.create_table(self.sql_create_country_table)
        Helper.printline("Countries table successfully created")
        self.display_country_table = "select * from countries;" 
        
    def create_tweet_table_on_database(self):
        self.sql_create_tweet_table = """ CREATE TABLE IF NOT EXISTS tweets (
                                tweet_id integer  PRIMARY KEY,
                                lang text NOT NULL,
                                created_at timestamp NOT NULL,
                                place_country_code text NULL,
                                user_location text NULL,
                                country_code text NULL,
                                full_text text NOT NULL,
                                clean_text text NOT NULL,
                                sentiment float NULL,
                                retweet_cnt integer NOT NULL,
                                favourite_cnt integer NOT NULL,
                                is_facemask boolean NOT NULL,
                                is_lockdown boolean NOT NULL, 
                                is_vaccine boolean NOT NULL
                            ); """
        self.create_table(self.sql_create_tweet_table) 
        Helper.printline("Tweets table successfully created")
      
    def create_connection(self):
        """ create a database connection to the SQLite database
            :param:
            :return:
        """
        self.con = None
        try:
            self.con = lite.connect(self.db, 
                            detect_types=lite.PARSE_DECLTYPES | lite.PARSE_COLNAMES)
        except Exception as e:
            sys.exit(f"Error with database connection: {e}")

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.con.cursor()
            c.execute(create_table_sql)
        except Exception as e:
            sys.exit(f"Error with table creation: {e}")
        
    def load_table(self, df, table_name):
        """ load the countries from the csv file into the database
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            df.to_sql(table_name, self.con, if_exists="replace", index=True)
            self.con.commit()
        except Exception as e:
            sys.exit(f"Error with inserting {table_name}: {e}")
            
    def display_table(self, sql_script, table_name):
        # Show countries table
        try:
            c = self.con.cursor()
            c.execute(sql_script)
    
            # View result
            result = c.fetchall()
        except Exception as e:
            sys.exit(f"Error with retreiving {table_name}: {e}")
            
        Helper.printline(f"Contents of {table_name} table")
        for row in result:
            print(row)
    
        # Commit work and close connection
        c.close()
        
    def save_tweet(self, row):
        df_tweet = pd.DataFrame([row])
        try:
            df_tweet.to_sql("tweets", self.con, if_exists='append', index=False)
            self.con.commit()
        except Exception as e:
            sys.exit(f"Error inserting into tweets the row - '{row}': {e}")
       