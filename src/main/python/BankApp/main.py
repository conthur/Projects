from helpers import load_table, reset, save_table 
import datetime

# Global Variables
account_id = None

def main():
  # reset the database when restarting sketch
  # to make changes persistent comment out the next line.
  reset()

  # shows a welcome header
  print("╔" + 48 * "═" + "╗")
  print(f"║{'Welcome to the Bucknell Bank!':^48}║")
  print("╚" + 48 * "═" + "╝")

  # shows the menu with all options
  menu()


"""
Gets the date and the time from the system and returns it.

Returns:
    
"""
def get_date_time():
  current_datetime = datetime.datetime.now()
  iso_format_datetime = current_datetime.isoformat()
  formated_datetime = iso_format_datetime[0:10] + ' ' + iso_format_datetime[11:19]

  return formated_datetime



def menu():

  global account_id

  if account_id:
    choice = None
    print("_" * 50)
    print(f"{'Please select an option:':^50}")
    print("━" * 50)
    print_menu_option(1, "Check account balance")
    print_menu_option(2, "Deposit")
    print_menu_option(3, "Withdraw")
    print_menu_option(4, "Logout")
    print("_" * 50)
    try:
      choice = int(input("Make a choice: "))
      assert choice >= 1 and choice <= 4

    except (ValueError, AssertionError):
      print_centered("Invalid Choice. Please choose a number from 1-4 and hit Enter.")
      print("_" * 50)
      menu()
      return

    print("_" * 50)

    if choice == 1:
      check_balance()

    elif choice == 2:
      deposit()

    elif choice == 3:
      withdraw()

    elif choice == 4:
      logout()

  else:
    account_id = login()
    menu()





def check_balance():

  print(" " * 50)
  print(" " * 50)
  print_centered("BALANCE")
  print("━" * 50)

  accounts = load_table("accounts")
  transactions = load_table("transactions")


  print('Date                           |            Amount')
  print("-" * 50)
  for acc in accounts: 
    if acc["id"] == account_id:
      trans_history = transactions[acc["id"] - 1]
      for i in range(len(trans_history[0])):
        formatString = '{0:^30} | {1:>17}'
        print(formatString.format(str(trans_history[0][i]), str(trans_history[1][i])))

      print("-" * 50)
      formatString = '{0:<30} | {1:>17.2f}'
      print(formatString.format('Current Balance', acc["Balance"]))






    print("_" * 50)
    con = input("Would you like to return to the Menu? (Y or N) ")
    if con == "Y":
      menu()
    if con == "N":
      check_balance()




def deposit():

  print(" " * 50)
  print(" " * 50)
  print_centered("DEPOSIT")
  print("━" * 50)
  deposit_input = input("How much money would you like to deposit? ")
  deposit_value = float(deposit_input)


  date_time = get_date_time()


  transactions = load_table("transactions")
  accounts = load_table("accounts")
  for acc in accounts:
    if acc["id"] == account_id:
      acc["Balance"] += deposit_value
      acc["Balance"] = round(acc["Balance"], 2)
      save_table("accounts", accounts)

      print("Your new account balance is: " + str(acc["Balance"]))

      this_tran = transactions[acc["id"] - 1]   
      this_tran[0].append(date_time)
      this_tran[1].append(str(deposit_value))
      save_table("transactions", transactions)

      print("_" * 50)
      con = input("Would you like to return to the Menu? (Y or N) ")
      if con == "Y":
        menu()
      if con == "N":
        deposit()



def withdraw():

  print(" " * 50)
  print(" " * 50)
  print_centered("WITHDRAWAL")
  print("━" * 50)
  print("There is a transaction fee of $ 3 for withdrawals.")
  withdrawal_input = input("How much money would you like to Withdrawal? ")
  withdrawal_value = float(withdrawal_input)


  date_time = get_date_time()


  transactions = load_table("transactions")
  accounts = load_table("accounts")
  for acc in accounts:
    if acc["id"] == account_id:
      withdrawal_value = withdrawal_value + 3
      acc["Balance"] -= withdrawal_value
      acc["Balance"] = round(acc["Balance"], 2)

      save_table("accounts", accounts)
      if acc["Balance"] >= 0:

        print("Your new account balance is: " + str(acc["Balance"])) 
        transactions[acc["id"] - 1][0].append(date_time)
        transactions[acc["id"] - 1][1].append("-" + str(withdrawal_value))

        save_table("transactions", transactions)

      else:
        print("Insufficient funds, please try again.")
        withdraw()



      print("_" * 50)
      con = input("Would you like to return to the Menu? (Y or N) ")
      if con == "Y":
        menu()
      if con == "N":
        withdraw()







def print_menu_option(option, label):
  print(label + (50 - len(label) - 1) * " " + str(option))

def print_centered(label):
  print(f"{label:^50}")






def login(card_number=None, pin=None):
  """
  Logs the user into the system
  """
  global account_id

  # ask for card input information
  if not card_number:
    card_number = int(input("Please enter your card number: "))
  if not pin:
    pin = int(input("Please enter your PIN: "))

  # check database against a card with the given number and pin, and set login
  cards = load_table("cards")
  for card in cards:
    if card["number"] == card_number and card["pin"] == pin:
      account_id = card["account_id"]
      print_centered("Welcome back!")
      menu() 
      return account_id

  print_centered("Invalid Login. Please try again.")
  return login()






def logout():
  """
  Logs the user out of the system
  """
  global account_id
  account_id = None
  print_centered("Goodbye!")
  login()
  return

# start the program
if __name__ == "__main__":
  main()
