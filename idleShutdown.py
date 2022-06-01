#!/usr/local/bin/python3

import time
import datetime
import sys
import os
from pathlib import Path

import yaml
from squeezebox_controller import SqueezeBoxController


def loop(config):

  print(config)

  controller = SqueezeBoxController(config["host"], config["port"])
  modeFile = Path('/tmp/SqueezeBoxRunning.txt')
  modeFile.touch()

  while True:

    params = {
      "player": config["player"],
      "query": "RAW"
    }
    mode = controller.simple_query(params)['mode']
    if mode == "play":
      modeFile.touch()
      print(datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S"), "RUNNING", flush=True)
    else:
      lastPlayed = time.time()-modeFile.stat().st_ctime
      if lastPlayed > config["timeout"]:
        print(datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S"), "SHUTDOWN", flush=True)
        os.system("/usr/bin/exitcheck.sh shutdown")
      else:
        print(datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S"), "KEEP ALIVE", flush=True)
    time.sleep(60)

def main():



  print(len(sys.argv))
  if len(sys.argv) != 2:
    print("Usage: idlehutdown.py configfile.yaml", file=sys.stderr)
    sys.exit(1)
  else:
    with open(sys.argv[1], 'r') as stream:
      config = yaml.load(stream, Loader=yaml.Loader)

    loop(config)

if __name__ == "__main__":
  main()