from ._anvil_designer import ResultsTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Results(ResultsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def Inputs_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Inputs')

  def Back_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Inputs')
