#!/usr/local/bin/python3

from time import sleep, time
from pirc522 import RFID
import yaml
from squeezebox_controller import SqueezeBoxController
import sys
import os

maxWaitTime = 10 # time to wait after playlist is restarted when rfid tag is presented again

def loop(config):

  print(config)

  controller = SqueezeBoxController(config["host"], config["port"])

  startTime = 0
  rdr = RFID()
  rdr.set_antenna_gain(5)
  
  old_playlist_name = None
  while True:
    print("wait", flush=True)
    rdr.wait_for_tag()
    (error, tag_type) = rdr.request()
    if not error:
      (error, uid) = rdr.anticoll()
      if not error:
        playlist_name = "-".join(str(i) for i in uid)
        if playlist_name == old_playlist_name:
          if (time() - startTime) < maxWaitTime:
            print("Playlist unchanged", flush=True)
            sleep(0.25)
            continue
        old_playlist_name = playlist_name
        if playlist_name not in config.keys():
          print(playlist_name, "not found in config", flush=True, file=sys.stderr)
          sleep(0.25)
          continue
        print(playlist_name, config[playlist_name], flush=True)
        params = {
          "player": config["player"],
          "term": config[playlist_name],
          "type": "PLAYLIST"
        }
        try:
          controller.search_and_play(params)
        except:
          print(config[playlist_name], "not found in Spotify", flush=True, file=sys.stderr)
          sleep(0.25)
          continue
        else:
          startTime = time()
    sleep(2)
  # Calls GPIO cleanup
  rdr.cleanup()



def main():



  print(len(sys.argv))
  if len(sys.argv) != 2:
    print("Usage: readRFID.py configfile.yaml", file=sys.stderr)
    sys.exit(1)
  else:
    with open(sys.argv[1], 'r') as stream:
      config = yaml.load(stream, Loader=yaml.Loader)

    if "startsound" in config.keys():
      os.system(f"/usr/local/bin/mpg123 {config['startsound']}")

    loop(config)

if __name__ == "__main__":
  main()
