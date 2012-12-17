""" A suite of functions for file conversion to/from fidl types. """
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
    header = fidl.readline()
    header = header.strip()
        ## Drops any tab or 
        ## \n at the end
        ## of the header
    
    # Header should now be a list of conditions/levels
    # The TR is always the leftmost entry in the header
    header = header.split(' ')
    tr = float(header.pop(0))
    
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
        time = int(float(row[0]) / tr)     ## convert to tr units
        condindex = int(row[1])
    
        # And write...
        outcsv.writerow([time, condindex, condlookup[condindex]])
        
    fidl.close()
    out.close()


def combine_labels(csvfile1, csvfile2, name):
    """ Combine csv formatted labels files into a new file called
    <name>. 
    
    WARNING: this function has no safeties. If the file have differing row
    numbers, or one has a header and the other does not, the function
    blindly proceeds with no errors.  Use with care. """
    
    # Open fids, then open a csv file for reading
    fid1 = open(csvfile1, 'r')
    fid2 = open(csvfile2, 'r')    
    csv1 = csv.reader(fid1, delimiter=",")
    csv2 = csv.reader(fid2, delimiter=",")
    
    # And for writing
    fid3 = open(name, 'w')
    combinedcsv = csv.writer(fid3, delimiter=",")
    
    # Now loop over and, combining as we go.
    [combinedcsv.writerow(r1 + r2) for r1, r2 in zip(csv1, csv2)]
     
    # Cleaning up...
    fid1.close()
    fid2.close()    
    fid3.close()

