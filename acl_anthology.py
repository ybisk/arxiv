import os
import sys
import subprocess
import urllib.request
import xml.etree.ElementTree as ET

out = open("download.bib",'w')
base = "https://www.aclweb.org/anthology"
identifiers = sys.argv[1:]
for idx in identifiers:
  bib = "{}/{}.bib".format(base, idx)
  pdf = "{}/{}.pdf".format(base, idx)
  
  bibtex = str(urllib.request.urlopen(bib).read(), 'utf-8')
  print(bibtex)
  out.write(bibtex + "\n")
  subprocess.call("wget --user-agent=Lynx {}".format(pdf), shell=True)
out.close()

os.system("open .")
