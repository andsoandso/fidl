""" A suite of functions for file conversion to/from fidl types. """


def fidl_to_pymvpa(fidlname, outname):
    """ Convert fidl files (<fidlname>) to a text file (named <outname>) 
    easily read into Python for use as sample attributes inside PyMVPA. """

    import csv
    
    # Open fidl and the outfile
    fidl = open(fidlname, 'r')
    out = open(outname, 'w')
    outcsv = csv.writer(out, delimiter=",")
    
    # Get the header and parse it
    header = fidl.readline()
    header = header.strip()
        ## Drops and tab or /n at the end
        ## of the header; some files have these.
    
    header = header.split(' ')
        ## Header should now be a list of conditions/levels
        
    tr = float(header.pop(0))
        ## The TR is always the leftmost entry in the header
      
    # Create a lookup table of cond name to integers.
    condlookup = dict()
    for ii, cond in enumerate(header):
        condlookup[ii + 1] = cond
            ## Indexing from 1 not 0
    
    # Now use csv to loop over the rows
    fidlcsv = csv.reader(fidl, delimiter='\t')
    for row in fidlcsv:
        print(row)
        
        # Skip empty lines (i.e. empty lists)
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

