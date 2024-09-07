from ._anvil_designer import InputsTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import plotly.graph_objects as go




class Inputs(InputsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    
    # Define a list of years from 1954 to 2005
    year_list = [str(x) for x in range(20,60)]
    # Set the items of the dropdown to be the years
    self.Age_drop_down.items = year_list


    # Define age of pension
    pension_age_list = [str(x) for x in range(50,75)]
    self.PensionAge_drop_down.items = pension_age_list

    # Define expected death age 
    death_age_list = [str(x) for x in range(70,100)]
    self.Death_drop_down.items = death_age_list
    
    # Define return on savings
    return_list = [str(x * 0.5) for x in range(-2,20)]
    self.Return_drop_down.items = return_list

    # Define inflation 
    inflation_list = [str(x * 0.5) for x in range(0,8)]
    self.Inflation_drop_down.items = inflation_list

    # Define growth
    growth_list = [str(x * 0.5) for x in range(0,6)]
    self.Growth_drop_down.items = growth_list

  def Results_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    print("click")
    open_form('Results')

  def CSV_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('import_csv_data_to_table')
  