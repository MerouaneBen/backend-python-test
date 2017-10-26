"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
from docopt import docopt
from db_insert_sample_data import FillData

from alayatodo import app

if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        FillData().insert_data()
        print "AlayaTodo: Database initialized."
    else:
        app.run(use_reloader=True,host='0.0.0.0') # the host argument allow connection from any machine
