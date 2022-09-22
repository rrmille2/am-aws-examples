import sys
import csv
import json

def convert(csv_fname):
  data = []
  file = open(csv_fname, 'r')
  dict_reader = csv.DictReader(file)
  for row in dict_reader:
    q = []
    q.append(row['q'])
    row['q'] = q
    data.append(row)

  #print(data)
  qna = {}
  qna['qna'] = data
  print(json.dumps(qna, indent=4, ensure_ascii=False))


def main(argv):
  convert(argv[1])

if __name__ == "__main__":
  main(sys.argv)


