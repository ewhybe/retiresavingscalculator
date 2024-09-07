from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go




class Form1(Form1Template):
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