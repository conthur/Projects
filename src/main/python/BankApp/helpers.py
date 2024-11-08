import json

def reset():
  """
  Reverts the database to it's original state.
  MODIFY AS NEEDED
  """
  accounts = [
    {"id": 1, "owner": "Sam Adams", "Balance": 500},
    {"id": 2, "owner": "Connor Thurston", "Balance": 1000}
  ]

  cards = [
    {"account_id": 1, "number": 111111, "pin": 1111},
    {"account_id": 2, "number": 222222, "pin": 2222},

  ]


  transactions = [
    [[],[]],
    [[],[]]
  ]


  save_table("accounts", accounts)
  save_table("cards", cards)
  save_table("transactions", transactions)

def save_table(table, data):
  """
  Saves data into <table>.json.
  DO NOT CHANGE THIS FUNCTION
  """
  with open(f"{table}.json", "w") as f:
    f.write(json.dumps(data, indent=2))

def load_table(table):
  """
  Loads and returns data from <table>.json.
  DO NOT CHANGE THIS FUNCTION
  """
  with open(f"{table}.json", "r") as f:
    return json.loads(f.read())


