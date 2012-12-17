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

    