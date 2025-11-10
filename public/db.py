import sqlite

def conn():
  c = sqlite.connect("/var/local/eric/pmauth.sqlite")
  return c, c.cursor()
