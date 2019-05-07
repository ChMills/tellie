#############################################################################
# get_channel.py                                                            #
# Script to load (T)ELLIE channel information from couchDB                  #
# 1. Prints HW info                                                         #
# 2. Plots calibration (tuning) curves                                      #
#                                                                           #
# Date created: 07/May/2019                                                 #
# Author: M Rigan <m.rigan@sussex.ac.uk> : New file                         #
#############################################################################

# imports
from orca_side import tellie_database
import argparse
import sys
import json
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# text formatting
matplotlib.rcParams.update({'font.size': 13})

# set up access to database
database = tellie_database.TellieDatabase('http://couch.snopl.us', 'telliedb')

# load channel data from couchDBs
def get_channel(channel):
    # key for query
    key = [ int(channel), [ 10870, 2147483647 ], 0, -2 ]
    # load rows (database data)
    rows = database.db.view('_design/channels/_view/channel_by_number', key=key, include_docs=True)
    if len(rows)==0:
        print "No TELLIE data for channel %s" % channel
        return None
    elif len(rows)!=1:
        print "Multiple entries found for channel %s" % channel

    # store data
    for row in rows:
        channel = row.doc['channel']
        cone = row.doc['cone']
        driver = row.doc['driver']
        PIN_board = row.doc['PIN_board']
        fibre_delay = row.doc['fibre_delay']
        m_ipw = row.doc['master_IPW']
        m_photons = row.doc['master_photons']
        m_photons_rms = row.doc['master_photons_rms']
        m_pin = row.doc['master_PIN']
        m_pin_rms = row.doc['master_PIN_rms']
        s_ipw = row.doc['slave_IPW']
        s_photons = row.doc['slave_photons']
        s_photons_rms = row.doc['slave_photons_rms']
        s_pin = row.doc['slave_PIN']
        s_pin_rms = row.doc['slave_PIN_rms']
    return channel, cone, driver, PIN_board, fibre_delay, m_ipw, m_photons, m_photons_rms, m_pin, m_pin_rms, s_ipw, s_photons, s_photons_rms, s_pin, s_pin_rms

# main function
if __name__=="__main__":
    # parser set-up
    parser = argparse.ArgumentParser(description='Load TELLIE channel data from couchDB')
    parser.add_argument("-ch", dest="channel", default=1, help="channel number")
    args = parser.parse_args()

    channel = int(args.channel)

    if (channel > 95):
        print "Check your channel number!!!"
        sys.exit()
    else:

        # call function to load data
        data = get_channel(channel)
        print 'Channel: ', data[0]
        print 'Cone: ', data[1]
        print 'Driver: ', data[2]
        print 'PIN_board: ', data[3]
        print 'fibre_delay: ', data[4]

        # store loaded data
        m_ipw = data[5]
        m_photons = data[6]
        m_photons_rms = data[7]
        m_pin = data[8]
        m_pin_rms = data[9]
        s_ipw = data[10]
        s_photons = data[11]
        s_photons_rms = data[12]
        s_pin = data[13]
        s_pin_rms = data[14]

        # make plots
        fig = plt.figure(figsize=(18, 13))
        fig.add_subplot(1,3,1)
        plt.xlabel('IPW', fontweight='bold')
        plt.ylabel('Photons', fontweight='bold')
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.errorbar(m_ipw, m_photons, xerr=None, yerr=m_photons_rms, fmt='r.')
        plt.errorbar(s_ipw, s_photons, xerr=None, yerr=s_photons_rms, fmt='b.')
        plt.grid(True)
        fig.add_subplot(1,3,2)
        plt.xlabel('IPW', fontweight='bold')
        plt.ylabel('PIN', fontweight='bold')
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.errorbar(m_ipw, m_pin, xerr=None, yerr=m_pin_rms, fmt='r.')
        plt.errorbar(s_ipw, s_pin, xerr=None, yerr=s_pin_rms, fmt='b.')
        plt.grid(True)
        fig.add_subplot(1,3,3)
        plt.xlabel('PIN', fontweight='bold')
        plt.ylabel('Photons', fontweight='bold')
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.errorbar(m_pin, m_photons, xerr=m_pin_rms, yerr=m_photons_rms, fmt='r.')
        plt.errorbar(s_pin, s_photons, xerr=s_pin_rms, yerr=s_photons_rms, fmt='b.')
        plt.grid(True)

        # male legend
        l1 = mpatches.Patch(color='red', label='MASTER')
        l2 = mpatches.Patch(color='blue', label='SLAVE')
        plt.legend(handles=[l1,l2])

        # show plots
        plt.show()
