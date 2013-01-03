""" A submodule for calculating basic statistics about .csv metadata files
converted from fidl files.  To convert see fidl.convert.fidl_to_csv(). 

Requires pandas (http://pandas.pydata.org/).
"""
import os
import pandas as pd


def counts(csvfile, col):
    """ Return the counts for each unique entry in <col>. <col> can be a 
    string, i.e. the <col> name, or an integer (0...N-1), where N
    is the number of cols. 
    
    The returned counts are in a pandas.Series objects, which
    can be treated a lot like a dictionary. """
    
    # Read in the csv
    data = pd.read_csv(csvfile, na_values=['NA',])
    
    # And get the counts
    cnts = None
    try:
        # Try col as the name
        cnts = pd.Series.value_counts(data[col])
    except KeyError:
        # then as an index
        cnts = pd.Series.value_counts(data.ix[:,col])

    return cnts
    
    
def group_counts(csvfiles, col):
    """ Return the *mean* counts for each unique entry in col 
    for all the files in <csvfiles>. <col> can be a 
    string, i.e. the <col> name, or an integer (0...N-1), where N
    is the number of cols.
    
    The returned counts are in a pandas.Series objects, which
    can be treated a lot like a dictionary. """
    
    groupcnt = counts(csvfiles.pop(), col)
    # Loop over csvfiles
    # adding cnts to groupcnt
    for cf in csvfiles:
        for k, v in counts(cf, col).iteritems():
            groupcnt[k] += v
    
    return groupcnt
    
    