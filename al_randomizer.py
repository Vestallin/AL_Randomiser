import csv
from pymongo import MongoClient
from random import choice

"""
Author: Watcharapon Thossaruksa (Vestallin)

This file is mainly used for those who seek thrills in building fleet(s) in Azur Lane only.
Please do not take this seriously for building a meta fleet, you have been warned.

Please run MongoDB server first before proceeding to run this file

Credit for datamined stats:
    https://docs.google.com/spreadsheets/d/1aK_5AtCw_DnlOMoIQjZHU2SUGboQ9VpX-7gDVRufBF0/edit#gid=1495731855

"""
def initialize():
    ''' 
    The initializer of this program where it loads the data from a given csv file.
    Then it inserts the data from previous step into a MongoDB database to create a collection "azur"
    which will be used in randomisation.

    '''
    headers = []
    result = []
    data = []
    try:
        client = MongoClient('localhost', 27017)
        db = client.test
        with open("ALStats.csv", 'r') as al:
            files = csv.reader(al)
            headers = next(files)
            for row in files:
                result.append(row)
        print("Successfully loaded the data")
        
        for rows in result:
            record = {}
            for i in range(len(rows)):
                if rows[i]:
                    record[headers[i]] = rows[i]
            data.append(record)            
        print("Successfully created the data for insertion")

        col = db.azur
        query = col.delete_many({})
        query = col.insert_many(data)
        print("Successfully created the collection with given data")
        
        while True:
            print("Your result is: ")
            print(fleet_randomizer(col))
            if(input("\n Re-roll the current fleet?: Y/N").lower() == "n"):
                print("\n GOOD LUCK ON COMBAT, COMMANDER!")
                break
    except Exception as e:
        print(e)
        
def fleet_randomizer(col):
    '''
    The main function of randomising a full fleet with 3 Vanguard units and 3 Main Fleet units.
    
    Parameter:
        col: a collection from MongoDB database
    Return:
        A tuple that represents the 6 randomised (and unique) ships with 3 Main Fleet, and 3 Vanguards
    '''
    vanguard_lst = ["DD", "CL", "CA", "CB", "DDG", "AE"]
    main_lst = ["BB", "CVL", "BC", "CV", "BM"]
    v_result = []
    m_result = []
    final_van = []
    final_main = []
    
    vanguard = col.find({"Type": {"$in": list(vanguard_lst)}}, {"Ship": 1, "_id": 0, "Type": 1})
    main_fleet = col.find({"Type": {"$in": list(main_lst)}}, {"Ship": 1, "_id": 0, "Type": 1})

    for v_row in vanguard:
        v_result.append(v_row)
    for m_row in main_fleet:
        m_result.append(m_row)

    while len(final_van) < 3:
        v_rand = choice(v_result)
        if v_rand not in final_van:
            final_van.append(v_rand)
    
    while len(final_main) < 3:
        m_rand = choice(m_result)
        if m_rand not in final_main:
            final_main.append(m_rand)
    
    return (final_main, final_van)

if __name__ == "__main__":
    initialize()
 
 