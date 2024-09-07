import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#import pandas as pd
#import matplotlib.pyplot as plt
import csv
from io import StringIO

@anvil.server.callable
def import_csv_data_to_table():
    # Load the CSV file from assets
    with anvil.media.load_file('_/resources/Female.csv') as csv_file:
        csv_content = csv_file.get_bytes().decode('utf-8')
        csv_reader = csv.reader(StringIO(csv_content))
        
        # Loop through CSV rows and insert them into a Data Table
        for row in csv_reader:
            # Insert each row into a Data Table (adjust columns as per your table schema)
            app_tables.Female.add_row(Age=row[0], Living=row[1])

    return "CSV data successfully inserted into the table!"


      