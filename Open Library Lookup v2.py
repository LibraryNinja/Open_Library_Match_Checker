import requests
import json
import pandas as pd
from time import sleep
from random import randint

#Set headers for API call
headers = {"Accept": "application/json"}

#Set up an empty dictionary
dict = {}
dict['notfound isbn'] = []

#Bring in input file from Analytics export
name = input('Name of input Excel file, without extension: ')
df = pd.read_excel(name + '.xlsx')

#Loads input file, sets column headers as 2nd row of the sheet
df.columns = df.iloc[1]
df = df.iloc[2:].reset_index(drop=True)

#Removes duplicates
df.drop_duplicates(subset='isbn', inplace=True)

#Removes string-preserving "s
df['isbn'] = df['isbn'].str.replace("\"","")

#Reindexes again because dropping duplicates messed up the index 
df.reset_index(drop=True, inplace=True)
df.head()

#Makes list from df column
ISBNs = df['isbn']

#Loop to run the ISBNs through the API and add ones with no returned data to a Dictionary
for i, isbn in enumerate(ISBNs, 0):
    #sleep(randint(5,10))    
    isbn = ISBNs[i]    
    getdata = requests.get('http://openlibrary.org/api/volumes/brief/isbn/' + isbn + '.json', headers=headers).json()
    datadump = json.dumps(getdata)
    results=json.loads(datadump)
    
    #If the returned results are empty (False) then add ISBN to dictionary
    if bool(results) == False:
        dict['notfound isbn'].append(isbn)

#Prints dictionary to make sure results make sense
print(dict)

#Makes new dataframe from newly-filled dictionary, renames column and sets index
df2 = pd.DataFrame(dict['notfound isbn'])
df2.columns = ['not found isbn']
df2.set_index(['not found isbn'], inplace=True)
df.set_index(['isbn'], inplace=True)
df2.head()

#Checks against original dataframe and spits out data for the ones from the "not found" list
df_merged = df2.join(df, how='left', lsuffix="left", rsuffix="right")
df_merged.head()
df_merged.to_excel('Books for Open Library.xlsx')
