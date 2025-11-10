#! /usr/bin/env python3

import argparse
import sys
import urllib

import db

parser = argparse.ArgumentParser(
  prog="auth",
  description="")

HEADERS = {}

def print_headers():
  global HEADERS

  print("\n".join([f"{name}: {HEADERS[name]}" for name in HEADERS]))
  print()

def auth(email, password, redirect=None):
  conn, cursor = db.conn()
  cursor.execute("SELECT rowid FROM user WHERE email = ? AND password = ?",
                 (email, password))
  row = cursor.fetchone()
  if row:
    if redirect:
      HEADERS["Location"] = redirect
      HEADERS["Status"] = "302 Found"
      print_headers()
    else:
      logged_in(row)
  else:
    create_or_forgot()
    
  
def main():
  args = parser.parse_args()
  params = urllib.parse.parse_qs(sys.stdin.read())
  try:
    auth(email=params.get("email"),
         password=params.get("password"),
         redirect=params.get("redirect"))
  except Exception as e:
    HEADERS["Status"] = "500 Internal Server Error"
    HEADERS["Content-Type"] = "text/html"
    print_headers()
    print("<html><head><title>ERROR</title><link rel=\"stylesheet\" href=\"style.css\"></head>")
    print("<body><pre>")
    print(e)
    print("</pre></body></html>")


if __name__ == "__main__":
  main()
