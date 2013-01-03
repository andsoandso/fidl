""" A suite of functions for file conversion to/from fidl types. All functions
write their results to disk, and return None. """
import os
import re
import csv


def fidl_to_csv(fidlname, csvname):
    """ Convert fidl files (<fidlname>) to a csv file (named <csvname>). 
    
        Column 1: TR
        Column 2: Condition index
        Column 3: Condition name
    """
    
    # Open fidl and the outfile
    fidl = open(fidlname, 'r')
    out = open(csvname, 'w')
    outcsv = csv.writer(out, delimiter=",")
    
    # Get the header and parse it
    header = fidl.next()
    header = header.strip()
        ## Drops any tab or 
        ## \n at the end
        ## of the header
    
    # Header should now be a list of conditions/labs
    # The TR is always the leftmost entry in the header
    header = header.split(' ')
    
    # Create a lookup table of 
    # cond name to integers.
    condlookup = dict()
    for ii, cond in enumerate(header):
        condlookup[ii + 1] = cond   ## Indexing from 1

    # Then open a csv object to read the fidl
    fidlcsv = csv.reader(fidl, delimiter='\t')
    
    # Create a header fo fidlcsv
    outcsv.writerow(['TR', 'condindex', 'condname'])
    
    for row in fidlcsv:
        # Skip empty lines/lists
        if not row:
            continue
        
        # Time is the first col, 
        # Cond is the second
        time = int(row[0])
        condindex = int(row[1])
        
        # And write...
        outcsv.writerow([time, condindex, condlookup[condindex]])
        
    fidl.close()
    out.close()


# TODO - test
def fuzzy_label(csvfile, col, map_dict, name, header=True):
    """ Relabel (possibly by combinding) labels in <col> from <csvfile>.
    based on <conddict>.  
    
    Note: A REGEX IS USED WHEN COMPARING MAP_DICT TO TO ENTRIES IN COL. Hence 
    the fuzzy in the function name.
    
    Input
    ----
    csvfile - name of the csv files to process, should match form produced
            by fidl_to_csv() in this module.
    col - the column number, indexed from 0
    map_dict - a dictionary whose keys may match the entries found in col
            and whose values are strings, the new condition names.
    name - The name of column for the the new label.
    header - if csvfile has a header, set to True (default)
    
    Output
    ----
    A csv file similar to the input but with a new label added to the
    rightmost col.  The old csv file is replaced with the new.
    """
    
    fid = open(csvfile, 'r')
    csv_f = csv.reader(fid, delimiter=',')
    
    tmpfid = open('tmp.txt', 'w')
    tmpcsv = csv.writer(tmpfid, delimiter=',')
    
    # If header add a entry for exp
    if header:
        head = csv_f.next()
        tmpcsv.writerow(head + [name, ])
    
    # Now loop over the csv_f
    # detecting the exp conds.
    for ii, row in enumerate(csv_f):
        lab = row[col]
        
        # Look for a match of lab in map_dict
        newlab = []
        [newlab.append(v) for 
                k, v in map_dict.items() if re.search(k, lab)]

        # If there was no match, "NA"
        # if these was one, add it to the row and 
        # write it, otherwise error.
        #
        # More than 1 match is an undeciable 
        # problem.
        if len(newlab) == 0:
            tmpcsv.writerow(row + ["NA", ])
        elif len(newlab) == 1:
            tmpcsv.writerow(row + [newlab[0], ])
        else:
            raise ValueError(
                    "Multiple matches detected at {0}.".format(ii))

    # Rename tmp.txt to <csvfile>
    os.rename('tmp.txt', csvfile)

    # Cleanup
    tmpfid.close()
    fid.close()


def _increase_tr(row, count):
    """ Increase TR in <row> by <count>. """
    
    newrow = [str(int(row[0]) + count), ] + row[1:]
    return newrow


# TODO - test
def tr_time(csvfile, col, timingdict, drop=True, header=True):
    """ Uses <timingdict>, a dict with keys reflecting condition labs
    and values matching durations, to expand csvfile rows so that every TR 
    in the fMRI data corresponding to the labels in <csvfile> has an entry.

    The .fidl file that csvfile files are derived from do not include 
    this kind of timing info.  Silly fidl.
    
    The TR index (col 0) of the csvfile is updated to match the TR
    of that row.
    
    Input
    ----
    csvfile - name of the csv files to process, should match form produced
            by fidl_to_csv() in this module.
    col - the column number, indexed from 0
    timingdict - a dictionary with keys matching entries in <col> and values
            specifying durations (in TRs).
    drop - if an entry from <col> is not contained in the timingdict should
            that data be dropped.
    header - if csvfile has a header set to True (default)
    
    
    Output
    ----
    A csv file similar to csvfile but with an increased number of rows,
    matching the timingdict's durations. """
    
    # Opening file handles for in 
    # and then out.
    fid = open(csvfile, 'r')
    csv1 = csv.reader(fid)
    
    head, tail = os.path.split(csvfile)
    fidout = open(os.path.join(head, "trtime_" + tail), "w")
    outcsv = csv.writer(fidout, delimiter=",")
    
    # Write the header to 
    # the outfile?
    if header:
        head = csv1.next()
        outcsv.writerow(head)
       
    # Loop over the in file
    for row in csv1:
        # Get the cond
        cond = row[col]
        
        # Using cond try and get a
        # duration from the timingdict
        try:
            duration = timingdict[cond]
        except KeyError:
            # If we're not dropping
            # write this row once, 
            # mirroring the in file
            if not drop:
                outcsv.writerow(row)
            else:
                continue
        else:
            [outcsv.writerow(_increase_tr(row, ii)) for 
                    ii in range(duration)]


def combine_labels(csvfile1, csvfile2, name, header=True):
    """ Combine csv formatted labels files into a new file called <name>. 
    
    NOTE: In combining we assume the first 3 cols of each file are 
    identical.
    
    WARNING: this function has no safeties. If the file have differing row
    numbers, or one has a header and the other does not, the function
    blindly proceeds.  Use with care. """
    
    # Open fids, then open a csv file for reading
    fid1 = open(csvfile1, 'r')
    fid2 = open(csvfile2, 'r')    
    csv1 = csv.reader(fid1, delimiter=",")
    csv2 = csv.reader(fid2, delimiter=",")
    
    # and for writing.
    fid3 = open(name, 'w')
    combinedcsv = csv.writer(fid3, delimiter=",")
    
    if header:
        head1 = csv1.next()[0]
        head1 = head1.split()   ## drop any \n or white space that may have
                                ## creapt in.
        head2 = csv2.next()[0]
        head2 = head2.split()
        combinedcsv.writerow(head1 + head2[3:])

    # Now loop over, combining as we go.
    [combinedcsv.writerow(r1 + r2[3:]) for r1, r2 in zip(csv1, csv2)]
     
    # Cleaning up...
    fid1.close()
    fid2.close()    
    fid3.close()

