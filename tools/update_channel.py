#############################################################################
# update_channel.py                                                         #
# Script to update (T)ELLIE channel hardware information to couchDB         #
#                                                                           #
# Date created: 07/May/2019                                                 #
# Author: M Rigan <m.rigan@sussex.ac.uk> : New file                         #
#############################################################################

# imports
from orca_side import tellie_database
import sys
import argparse
import json

# set up access to database
database = tellie_database.TellieDatabase('http://couch.snopl.us', 'telliedb')

# main function
if __name__=="__main__":
    # parser set-up
    parser = argparse.ArgumentParser(description='Update TELLIE channel hardware data to couchDB')
    args = parser.parse_args()

    # ask for new data
    channel = raw_input('Channel (INT): ')
    cone = raw_input('Cone: ')
    driver = raw_input('Driver (INT): ')
    PIN_board = raw_input('PIN board: ')
    fibre_delay = raw_input('Fibre delay (FLOAT): ')
    print channel, cone, driver, PIN_board, fibre_delay

    # get the correct doc
    key = [ int(channel), [ 10870, 2147483647 ], 0, -2 ]
    rows = database.db.view('_design/channels/_view/channel_by_number', key=key, include_docs=True)
    if len(rows)==0:
        print "No TELLIE data for channel %s" % channel
        sys.exit()
    elif len(rows)!=1:
        print "Multiple entries found for channel %s" % channel
        sys.exit()
    for row in rows:
        tellie_doc = row.doc

    # update relevant data
    tellie_doc['channel'] = int(channel)
    tellie_doc['cone'] = cone
    tellie_doc['driver'] = int(driver)
    tellie_doc['PIN_board'] = PIN_board
    tellie_doc['fibre_delay'] = float(fibre_delay)

    # save file
    check = raw_input('Sure to rewrite ?! (Y/N): ')
    if check == 'Y':
        database.save(tellie_doc)
    else:
        print 'No changes made!'
