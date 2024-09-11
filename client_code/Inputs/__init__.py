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

    #button properties
    self.Results_button.background = "blue"
    
    indexace = float(self.Inflation_drop_down.selected_value) + float(self.Growth_drop_down.selected_value)
    
    self.label_Savings.text = "Potřebné úspory upravené o inflaci a růst mezd ke odchodu do důchodu:" 
    self.label_P.text = "Pravděpodobnost, že přežijete cílový věk " + self.Death_drop_down.selected_value + "let:"
    self.label_ConstWageSaving.text = "Investice 1. rok následně zvýšovaná vždy o " + str(indexace) + "%:"
    self.label_Annuity.text = "Rovnoměrné každoroční spoření:"


  
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

    Age = int(Age)
    PensionAge = int(PensionAge)
    Death = int(Death)
    Income = int(Income)*12
    Wealth = int(Savings)
    Return = float(Return)/100
    Inflation = float(Inflation)/100
    Growth = float(Growth)/100
  
    r = Return # real return
    i = Inflation
    g = Growth # real growth
    # nominal return as inflation + return and nominal growth as growth + inflation
    nr = r + i
    ng = g + i
  
    # years in retirement (yr] and years working (yw]
    yr = Death - PensionAge
    yw = PensionAge - Age
    
    # Dictionary of CZ death tables, shows surving number of people by sex from the original population of 100k in year 0 by year of age
    Male_data = {0: 100000, 1: 99774, 2: 99752, 3: 99741, 4: 99730, 5: 99721, 6: 99713, 7: 99706, 8: 99699, 9: 99692, 10: 99685, 11: 99677, 12: 99668, 13: 99657, 14: 99645, 15: 99628, 16: 99606, 17: 99577, 18: 99540, 19: 99493, 20: 99438, 21: 99374, 22: 99306, 23: 99235, 24: 99162, 25: 99090, 26: 99018, 27: 98947, 28: 98874, 29: 98799, 30: 98720, 31: 98636, 32: 98545, 33: 98446, 34: 98341, 35: 98228, 36: 98107, 37: 97978, 38: 97840, 39: 97695, 40: 97541, 41: 97377, 42: 97202, 43: 97014, 44: 96811, 45: 96591, 46: 96351, 47: 96087, 48: 95797, 49: 95475, 50: 95118, 51: 94722, 52: 94284, 53: 93801, 54: 93270, 55: 92689, 56: 92054, 57: 91361, 58: 90603, 59: 89773, 60: 88861, 61: 87859, 62: 86757, 63: 85546, 64: 84220, 65: 82773, 66: 81202, 67: 79506, 68: 77682, 69: 75728, 70: 73643, 71: 71424, 72: 69077, 73: 66607, 74: 64017, 75: 61306, 76: 58469, 77: 55503, 78: 52412, 79: 49202, 80: 45889, 81: 42491, 82: 39030, 83: 35520, 84: 31978, 85: 28431, 86: 24921, 87: 21498, 88: 18222, 89: 15150, 90: 12335, 91: 9821, 92: 7636, 93: 5781, 94: 4253, 95: 3035, 96: 2097, 97: 1401, 98: 903, 99: 561, 100: 336, 101: 194, 102: 108, 103: 58, 104: 30, 105: 15}
    Female_data = {0: 100000, 1: 99797, 2: 99777, 3: 99766, 4: 99754, 5: 99741, 6: 99727, 7: 99715, 8: 99706, 9: 99698, 10: 99691, 11: 99684, 12: 99676, 13: 99668, 14: 99657, 15: 99643, 16: 99628, 17: 99609, 18: 99588, 19: 99565, 20: 99540, 21: 99515, 22: 99489, 23: 99463, 24: 99438, 25: 99413, 26: 99387, 27: 99362, 28: 99336, 29: 99308, 30: 99279, 31: 99247, 32: 99212, 33: 99174, 34: 99133, 35: 99087, 36: 99037, 37: 98982, 38: 98923, 39: 98859, 40: 98790, 41: 98715, 42: 98634, 43: 98546, 44: 98448, 45: 98342, 46: 98224, 47: 98094, 48: 97950, 49: 97791, 50: 97616, 51: 97422, 52: 97208, 53: 96972, 54: 96711, 55: 96424, 56: 96107, 57: 95758, 58: 95374, 59: 94951, 60: 94487, 61: 93979, 62: 93422, 63: 92815, 64: 92152, 65: 91430, 66: 90643, 67: 89784, 68: 88846, 69: 87820, 70: 86693, 71: 85454, 72: 84089, 73: 82584, 74: 80926, 75: 79099, 76: 77089, 77: 74882, 78: 72463, 79: 69818, 80: 66930, 81: 63788, 82: 60381, 83: 56709, 84: 52781, 85: 48618, 86: 44261, 87: 39762, 88: 35186, 89: 30613, 90: 26132, 91: 21839, 92: 17827, 93: 14180, 94: 10966, 95: 8224, 96: 5968, 97: 4181, 98: 2823, 99: 1834, 100: 1145, 101: 686, 102: 394, 103: 218, 104: 115, 105: 59}
  
    # choose the right dataset by sex
    if Sex == 'Muž':
      death_data = Male_data
    else:
      death_data = Female_data
  
    # Calculate the probability of having died by the time of retirement (sex dependent)
    LivingAtRetireAge = death_data[PensionAge]
    LivingAtDeathAge = death_data[Death]
    ProbabilityHasDied = 1 - LivingAtDeathAge / LivingAtRetireAge
    
    # Casculate income at PensionAge, i.e. Income adjusted for inflation and wage growth
    IncomePensionAge = Income * (1 + ng) ** (yw)
  
    # Calculate necessary savings at PensionAge given desired income at pension age
    #NecessarySavingsAtRetireAge = IncomePensionAge * (1- ((1 + ng)/(1 + nr))**(yr))/(1-((1 + ng)/(1 + nr)))
    NecessarySavingsAtRetireAge = IncomePensionAge * (1- ((1 + ng)/(1 + nr)) ** yr)/(nr - ng) - Wealth
    
    try: 
      AnnuitySavings = NecessarySavingsAtRetireAge * (nr / ((1 + nr) ** yw - 1)) 
    except: AnnuitySavings = 9999999999
  
  
    try:
      ConstantWageShareSavings = NecessarySavingsAtRetireAge * ((nr - ng) / ((1 + nr)** yw - (1 + ng)** yw))
    except:
      ConstantWageShareSavings = 99999999

    if NecessarySavingsAtRetireAge < 0:
      self.label_NecessarySavings.text = "Již máš našetřeno"
      self.label_AnnuitySaving.text = ""
      self.label_IndexedSaving.text = ""
      self.label_PDied.text = ""
    else:
      self.label_NecessarySavings.text = str(f"{NecessarySavingsAtRetireAge:,.0f}")
      self.label_AnnuitySaving.text = str(f"{AnnuitySavings:,.0f}") + "/ rok"
      self.label_IndexedSaving.text = str(f"{ConstantWageShareSavings:,.0f}") + "/ rok"
      self.label_PDied.text = str(f"{1-ProbabilityHasDied:,.0%}")
  
    # savings build-up
    # prepare list to fill in with calculated ages and savings in each age
    WorkYears = [Age]
    SavingsCumul = []
    Deposits = []
    Savings = []
    Saving = Wealth
    Deposit = ConstantWageShareSavings
    i = 0
    for WorkYear in range (Age+1, PensionAge+1):
      # increase savings by interest
      Saving = Saving * (1 + nr) 
      # deposit new money
      Deposit = Deposit * (1 + ng) 
      # add up
      Saving = Saving + Deposit
      i = i + 1
      # add calculated saving and year in lists
      WorkYears.append(WorkYear)
      SavingsCumul.append(Saving)
      Deposits.append(Deposit)
      Savings.append(Saving)
    # prepare savings build-up in dictionary
    SavingsBuildup = {
      "Age" : WorkYears,
      "Saved" : SavingsCumul,
      "Deposits:" : Deposits,
      "Savings:" : Savings
    }
  
    # Create and display labels for the variables
    return NecessarySavingsAtRetireAge, AnnuitySavings, ConstantWageShareSavings, ProbabilityHasDied 
   
# Plot
    #self.plot_1.data = [
    #go.Scatter(
    #    x=SavingsBuildup['Age'],  # x-axis data
    #    y=SavingsBuildup['Saved'],  # y-axis data
    #    mode='lines',  # Line chart
    #    name='Savings Buildup'
    #)
    #]
    
    # Optionally, customize the layout (axis labels, title, etc.)
    #self.plot_1.layout = {
    #    'title': 'Savings Buildup Over Time',
    #    'xaxis': {'title': 'Age'},
    #    'yaxis': {'title': 'Amount Saved (in $)'}
    #}
   


  



