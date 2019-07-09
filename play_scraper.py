#import required dependencies
import play_scraper as ps
import sqlite3 as sql

#Enter location of your database eg: 'C:\Your_Folder_Name'
#and establish connection with it
conn = sql.connect(r'location_of_your_database')

#insert statement is used to make it easier typing in the values as there are 30 variables in application data grabbed
#from playstore
insert_statement = ("INSERT INTO Apps VALUES " + str(('?',)*30).replace("'", ''))

#Game Categories of playstore as found in the documentation of play_scraper library
game_categories = {"GAME": "GAME",
    "GAME_ACTION": "GAME_ACTION",
    "GAME_ADVENTURE": "GAME_ADVENTURE",
    "GAME_ARCADE": "GAME_ARCADE",
    "GAME_BOARD": "GAME_BOARD",
    "GAME_CARD": "GAME_CARD",
    "GAME_CASINO": "GAME_CASINO",
    "GAME_CASUAL": "GAME_CASUAL",
    "GAME_EDUCATIONAL": "GAME_EDUCATIONAL",
    "GAME_MUSIC": "GAME_MUSIC",
    "GAME_PUZZLE": "GAME_PUZZLE",
    "GAME_RACING": "GAME_RACING",
    "GAME_ROLE_PLAYING": "GAME_ROLE_PLAYING",
    "GAME_SIMULATION": "GAME_SIMULATION",
    "GAME_SPORTS": "GAME_SPORTS",
    "GAME_STRATEGY": "GAME_STRATEGY",
    "GAME_TRIVIA": "GAME_TRIVIA",
    "GAME_WORD": "GAME_WORD",}

#Collections as found in the documentation of play_scraper library
collections = {'NEW_FREE': 'topselling_new_free',
    'NEW_PAID': 'topselling_new_paid',
    'TOP_FREE': 'topselling_free',
    'TOP_PAID': 'topselling_paid',
    'TOP_GROSSING': 'topgrossing',
    'TRENDING': 'movers_shakers',}


#replace ENTER_COLLECTION with any of the collections specified above to search 
#eg: NEW_FREE
current_collection = 'ENTER_COLLECTION'

#following loop enters into the database the information of application one-by-one
#30 variables of information is entered into the database
for _category in game_categories.values():
    _results = 120
    _page = 1
    while(_page <= 5):
        _results = 500 // _page
        if(_results > 120):
            _results = 120
        for x in ps.collection(collection=current_collection,category=_category,results=_results,page=_page, detailed=True):
            cursor = conn.execute("SELECT title from Apps where title = ?", (x['title'],))
            if(len(cursor.fetchall()) is 0):
                x['installs'] = x['installs'].replace('+', '')
                conn.execute(insert_statement, tuple([str(y) for y in x.values()]))
                conn.commit()
        print(_results, _page)
        _page += 1

#close the connection with database
conn.close()