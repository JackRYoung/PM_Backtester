

# User defined strategy function.
# Add global variables to this file, import libraries and be as creative as
# you like, as long as the file returns a list of orders to be executed.
def strategy(date, data, portfolio, capital, orders, error):
  # If error == True, it means that the same date and data as last time will be
  # coming in, the capital and portfolio will be unchanged, and the orders
  # coming in will be the same as the orders sent out on the last iteration.
  # If this error is not adressed there will be infinite recursion.
    return orders
