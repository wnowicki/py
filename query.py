import database
import configuration
import repo

conf = configuration.load('config.json')

for x in database.Database().fetchall(repo.get_file_contents(conf['github']['token'], 'wnowicki/py', 'example.sql')):
    print(x)
