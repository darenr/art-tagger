import csv
import sys
import re
import collections

l = []
with open('data/genes.csv', mode="r") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
      if 'normalized_type' in row:
        l.append(row['normalized_type'])

print collections.Counter(l)
      
    
