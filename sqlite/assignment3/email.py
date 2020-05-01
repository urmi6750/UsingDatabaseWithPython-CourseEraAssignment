import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS Counts''')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')


fh = open('mbox.txt')

list=[]
for line in fh:


    if not line.startswith('From: ') : continue
    pieces = line.split()
    email = pieces[1]
    dom=email.find('@')
    org=email[dom+1:len(email)]
    


    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org, ))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count) 
                VALUES ( ?, 1 )''', ( org, ) )
    else : 
        cur.execute('UPDATE Counts SET count=count+1 WHERE org = ?', 
            (org, ))

conn.commit()


sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'
print ("Counts:")
for row in cur.execute(sqlstr) :
    print (str(row[0]), row[1])

#Closing the DB
cur.close()

