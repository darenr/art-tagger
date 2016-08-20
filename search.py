import csv
import sys
import re

if len(sys.argv) > 1:
  with open('genes.csv', mode="r") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
      if re.search(sys.argv[1], row['name'], re.I):
        print 'Category', row['name']
        print 'Definition', row['Definition']
else:
  print "Usage: <pattern>"
