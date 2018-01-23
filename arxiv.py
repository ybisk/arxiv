import sys
import subprocess
import urllib.request
import xml.etree.ElementTree as ET

out = open("download.bib",'w')
base = "http://export.arxiv.org/api/query?id_list="
identifiers = sys.argv[1:]
for identifier in identifiers:
  url = base + identifier
  tree = ET.parse(urllib.request.urlopen(url))
  root = tree.getroot()

  title = ""
  conference = None
  authors = []
  url = "https://arxiv.org/abs/" + identifier
  for child in root:
    for grand in child:
      if "}title" in grand.tag:
        title = grand.text
      elif "}author" in grand.tag:
        for name in grand:
          authors.append(name.text)
      elif "}published" in grand.tag:
        date = grand.text.split("-")
        year = date[0]
        month = date[1]
      elif "}comment" in grand.tag:
        conference = grand.text

  subprocess.call("wget --user-agent=Lynx https://arxiv.org/pdf/" + identifier + ".pdf", shell=True)
  citekey = authors[0].split()[-1] + ":" + year
  if conference is None:
    out.write("@unpublished{" + citekey + ",\n")
  else:
    out.write("@inproceedings{" + citekey + ",\n")
    out.write("\tBooktitle = {" + conference + "},\n")
  out.write("\tAuthor = {" + " and ".join(authors) + " },\n")
  out.write("\tTitle = {{" + title + "}},\n")
  out.write("\tUrl = {" + url + "},\n")
  out.write("\tYear = {" + year + "},\n")
  out.write("\tMonth = {" + month + "},\n")
  out.write("}\n\n")
out.close()
