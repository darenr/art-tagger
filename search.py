import csv
import sys
import re

if len(sys.argv) > 1:
  with open('data/genes.csv', mode="r") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
      if re.search(sys.argv[1], row['name']+' '+row['Definition']+' ' + row['normalized_type'], re.I):
        print 'Category:', row['name'], '/', row['normalized_type']
        print '   Definition:', row['Definition']
        print '-'*70
else:
  print "Usage: <pattern>"
