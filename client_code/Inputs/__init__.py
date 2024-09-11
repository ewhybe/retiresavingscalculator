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
    year_list = [str(x) for x in range(20,66)]
    # Set the items of the dropdown to be the years
    self.Age_drop_down.items = year_list
    self.Age_drop_down.selected_value = '40'


    # Define age of pension
    pension_age_list = [str(x) for x in range(50,76)]
    self.PensionAge_drop_down.items = pension_age_list
    self.PensionAge_drop_down.selected_value = '65'

    # Define expected death age 
    death_age_list = [str(x) for x in range(70,100)]
    self.Death_drop_down.items = death_age_list
    self.Death_drop_down.selected_value = '85'
    
    # Define return on savings
    return_list = [str(x * 0.5) for x in range(-2,20)]
    self.Return_drop_down.items = return_list
    self.Return_drop_down.selected_value = '1.0'

    # Define inflation 
    inflation_list = [str(x * 0.5) for x in range(0,8)]
    self.Inflation_drop_down.items = inflation_list
    self.Inflation_drop_down.selected_value = '3.0'

    # Define growth
    growth_list = [str(x * 0.5) for x in range(0,6)]
    self.Growth_drop_down.items = growth_list
    self.Growth_drop_down.selected_value = '1.5'

    self.
    
    
  def Results_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    Sex = self.Sex_drop_down.selected_value
    Age = self.Age_drop_down.selected_value
    PensionAge = self.PensionAge_drop_down.selected_value
    Income = self.Income_box.text
    Savings = self.Savings_box.text
    Death = self.Death_drop_down.selected_value
    Return = self.Return_drop_down.selected_value
    Inflation = self.Inflation_drop_down.selected_value
    Growth = self.Growth_drop_down.selected_value

    
    #Pass values to server
    Passed_values = [Sex, Age, PensionAge, Income,Savings, Death, Return, Inflation, Growth]
    # call the server and "process_form" function with Passed_values, return outputr
    output = anvil.server.call('process_form',Passed_values)
    #unpack output 
    IncomePensionAge, NecessarySavingsAtRetireAge, AnnuitySavings, ConstantWageShareSavings, ProbabilityHasDied, SavingsBuildup = output
    # Create and display labels for the variables
    print ('IncomePensionAge ', IncomePensionAge, 'NecessarySavingsAtRetireAge ', NecessarySavingsAtRetireAge, AnnuitySavings, ConstantWageShareSavings, ProbabilityHasDied, SavingsBuildup)
 
    # Plot
    self.plot_1.data = [
    go.Scatter(
        x=SavingsBuildup['Age'],  # x-axis data
        y=SavingsBuildup['Saved'],  # y-axis data
        mode='lines',  # Line chart
        name='Savings Buildup'
    )
    ]
    
    # Optionally, customize the layout (axis labels, title, etc.)
    self.plot_1.layout = {
        'title': 'Savings Buildup Over Time',
        'xaxis': {'title': 'Age'},
        'yaxis': {'title': 'Amount Saved (in $)'}
    }
   


  



