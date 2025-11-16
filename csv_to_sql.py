import sqlite3
import csv
import os.path
import sys


def createtable(handle, header, sqlfile, stripfilename):
    ##Create SQL table based on CSV filename
    tablestring = "DROP TABLE IF EXISTS " + stripfilename + ";\nCREATE TABLE " + stripfilename + " (\n    "
 
    for i in range(len(header)):
        if i == len(header) - 1:
            tablestring = tablestring + header[i] + " TEXT"
        else:
            tablestring = tablestring + header[i] + " TEXT,\n    " 
    
    tablestring = tablestring + "\n);"

    conn = sqlite3.connect(sqlfile)
    cur = conn.cursor()
    cur.executescript(tablestring)
    return True

def inputdata(handle, header, stripfilename, sqlfile):
    ##Read CSV file and insert rows from CSV file into appropriate table
    conn = sqlite3.connect(sqlfile)
    cur = conn.cursor()    
    for line in handle:

        line = line.strip();
        pieces = line.split(',')
        
        for i in range(0, len(pieces)):
            pieces[i] = pieces[i].replace('"', '')
        
        columnlist = list()
        indata = "INSERT OR REPLACE INTO " + stripfilename + "\n("
        for i in range(len(header)):
            if i < len(header) -1:
                indata = indata + header[i] + ", "
                columnlist.append(pieces[i])
            else:    
                indata = indata + header[i]
                columnlist.append(pieces[i])
        indata = indata  + ")\n"
        
        indata = indata + "VALUES ( "
        for i in range(len(header)):
            if i < len(header) -1:
                indata = indata + "?, "
            else:
                indata = indata + "? )"
        cur.execute(indata,columnlist)
    #print(indata,columnlist)
    conn.commit()
    conn.close()    
    return True



inputfile = input("please enter a file: ")
sqlfile = input("Please enter an SQL file: ") + '.sqlite'

fullfile = inputfile + ".csv"
if not os.path.exists(fullfile):
    print("file not found")
    sys.exit()
print("  CSV Filename:", fullfile, "\n  SQL filename:",sqlfile)
handle = open(fullfile)

count = 0
for char in inputfile:
    if char == "/":
        count = count + 1
stripfilenames = inputfile.split("/")
stripfilename =stripfilenames[count]

reader = csv.reader(handle)
header = next(reader)

if createtable(handle, header, sqlfile, stripfilename):
    print("success!")

if inputdata(handle, header, stripfilename, sqlfile):
    print("success!")

