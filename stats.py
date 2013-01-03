""" A submodule for calculating basic statistics about .csv metadata files
converted from fidl files.  To convert see fidl.convert.fidl_to_csv(). 

Requires pandas (http://pandas.pydata.org/)
"""
import os
from collections import Counter
import pandas as pan


def counts(csvfile, col):
    """ Return the counts for each unique entry in <col>. <col> can be a 
    string, i.e. the <col> name, or an integer (0...N-1), where N
    is the number of cols. """
    
    # Read in the csv
    data = pd.read_csv(csvfile)
    
    # And get the counts
    cnts = None
    try:
        # Try col as the name
        cnts = Counter(data[col])
    except KeyError:
        # then as an index
        cnts = Counter(data.ix[:,col])

    return cnts
    
    
def group_counts(csvfiles, col):
    """ Return the *mean* counts for each unique entry in col 
    for all the files in <csvfiles>. <col> can be a 
    string, i.e. the <col> name, or an integer (0...N-1), where N
    is the number of cols. """
    
    # Use the first entry in csvfiles 
    # to init groupcnt
    groupcnt = counts(csvfiles.pop(), col)
    
    # Loop over csvfiles
    # adding cnts to groupcnt
    # if there is an entry in cnts
    # but not in groupcnt it will
    # die with a KeyError, which
    # is the desired outcome.
    for cf in csvfiles:
        for k, v in counts(cf, col).items():
            groupcnt[k] += v

    return groupcnt
    
    