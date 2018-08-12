import mysql.connector
import configuration
import repo

conf = configuration.load('config.json')

mydb = mysql.connector.connect(
    host=conf['mysql']['host'],
    user=conf['mysql']['user'],
    passwd=conf['mysql']['passwd'],
    port=conf['mysql']['port'],
    database=conf['mysql']['database']
)

mycursor = mydb.cursor()

mycursor.execute(repo.get_file_contents(conf['github']['token'], 'wnowicki/py', 'example.sql'))

for x in mycursor:
    print(x)
