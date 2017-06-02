"""
 *  Drew McArthur, Geo Engel, Risa Ulinski, Judy Zhou
 *  6/1/17
 *  a script to produce a single datafile from the race and horse information 
    located in the raw data folder (defined in config) for use with an AI
 *  note: use python3
"""

import yaml, os, csv
config = yaml.safe_load(open("config.yml"))

# right way to access config vars
# config['raw_data_path']

# get root folder, as well as pathname and file objects for the final product.
DATA = config['raw_data_path']
ENDFILENAME = config['final_data_filename']
ENDFILE = open(ENDFILENAME, 'w')

# create an object which writes data to files as a csv, using column headers 
# from config.yml and ignoring extra data
ENDFILEWRITER = csv.DictWriter(ENDFILE, fieldnames=config['data_col_headers'], 
                               extrasaction='ignore')

print("column headers: ")
print(config['data_col_headers'].split(','))

# if ENDFILE is empty, then write the header columns to the file.
if os.stat(ENDFILENAME).st_size == 0 and False:
    ENDFILEWRITER.writeheader()

# iterate through files in data directory
for d in os.listdir(DATA):
    for f in os.listdir(DATA + d):
        # if the file is a *.csv file,
        if f.endswith('.csv'):
            # then open the file with a csv reader
            path = DATA + "/" + d + "/" + f
            with open(path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    #print(row)
                    #ENDFILEWRITER.writerow(row)
                    quit()
