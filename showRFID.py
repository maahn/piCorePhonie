#!/usr/local/bin/python3

from time import sleep
from pirc522 import RFID



def loop():
  rdr = RFID()

  old_playlist_name = None
  while True:
    rdr.wait_for_tag()
    (error, tag_type) = rdr.request()
    if not error:
      (error, uid) = rdr.anticoll()
      if not error:
        playlist_name = "-".join(str(i) for i in uid)
        print(playlist_name)
    sleep(2)
  # Calls GPIO cleanup
  rdr.cleanup()



def main():
    loop()

if __name__ == "__main__":
  main()
  