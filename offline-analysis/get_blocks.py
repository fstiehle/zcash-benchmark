import requests
import json
import sys, getopt
import csv
"""
Parse file of block and timings generated from our benchmark, call getBlock of the zcash RPC interface for each block hash
Create a new enriched CSV file for analysis containing:
- blockNumber, blockSize, blockVersion, numberTx, numberVin, numberVout, numberJoinSplit
"""
inputfile = ''
outputfile = ''
CLIENT_URL = 'http://127.0.0.1:8232/'

def main(argv):
  global inputfile, outputfile 
  try:
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
  except getopt.GetoptError:
    print(' -i <inputfile> -o <outputfile>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
        print(' -i <inputfile> -o <outputfile>')
        sys.exit()
    elif opt in ("-i", "--ifile"):
        inputfile = arg
    elif opt in ("-o", "--ofile"):
        outputfile = arg
  print('Input file is ', inputfile)
  print('Output file is ', outputfile)
  
  with open(inputfile, newline='') as f:
    reader = csv.reader(f)
    blocks = list(reader)

  for block in blocks:
    blockNumber = block[0]
    blockTime = block[1]
    payload = {
        "method": "getblock",
        "params": [blockNumber, 2],
        "jsonrpc": "1.0",
        "Content-Type": "text/plain"
    }
    response = requests.post(CLIENT_URL, json=payload, headers={"Content-Type": "text/plain"}, auth=("bitcoin", "bitcoin")).json()
    if (response['error']):
      print(response['error']['message'], ": ",  blockNumber)
      continue

    processBlock(blockNumber, blockTime, response['result'])

def processBlock(blockNumber, blockTime, data):
  global outputfile
  blockSize = data['size']
  blockVersion = data['version']
  numberTx = len(data['tx'])
  numberVin = 0
  numberVout = 0
  numberJoinSplit = 0
  numbervShieldedSpend = 0
  numbervShieldedOutput = 0

  for tx in data['tx']:
    if 'vin' in tx:
      numberVin = numberVin + len(tx['vin'])
    if 'vout' in tx:
      numberVout = numberVout + len(tx['vout'])
    if 'vjoinsplit' in tx:
      numberJoinSplit = numberJoinSplit + len(tx['vjoinsplit'])
    if 'vShieldedSpend' in tx:
      numbervShieldedSpend = numbervShieldedSpend + len(tx['vShieldedSpend'])
    if 'vShieldedOutput' in tx:
      numbervShieldedOutput = numbervShieldedOutput + len(tx['vShieldedOutput'])

  with open(outputfile, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([blockNumber, blockSize, blockVersion, numberTx, numberVin, numberVout, numberJoinSplit, numbervShieldedSpend, numbervShieldedOutput, blockTime])

if __name__ == "__main__":
  main(sys.argv[1:])