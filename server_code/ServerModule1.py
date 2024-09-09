import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import numpy as np


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
def process_form(Passed_values):
  print(Passed_values)
  Sex, Age, PensionAge, Income,Savings, Death, Return, Inflation, Growth = Passed_values
  Age = int(Age)
  PensionAge = int(PensionAge)
  Death = int(Death)
  Income = int(Income)
  Savings = int(Savings)
  Return = float(Return)/100
  Inflation = float(Inflation)/100
  Growth = float(Growth)/100
  
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
  ProbabilityOfHasDied = 1 - LivingAtDeathAge / LivingAtRetireAge
  
 
  # Calculate savings needed for retirement
  ages = range(PensionAge + 1, Death)
  # Casculate income at PensionAge, i.e. Income adjusted for inflation and wage growth
  IncomePensionAge = Income * (1+Inflation+Growth)**(PensionAge - Age)

  NecessarySavingsAtRetireAge = IncomePensionAge * (1-((1+Growth+Inflation)/(1+Return+Inflation))**(Death - PensionAge))/(1-((1+Growth+Inflation)/(1+Return+Inflation)))
  AnnuitySavings = (NecessarySavingsAtRetireAge * Return)/((1+Return)**(PensionAge - Age) - 1)
  ConstantWageShareSavings = (NecessarySavingsAtRetireAge * (Return - Growth)) / ((1+Return)**(PensionAge - Age) - (1+Growth)**(PensionAge - Age))

  
  output = (IncomePensionAge, NecessarySavingsAtRetireAge, AnnuitySavings, ConstantWageShareSavings, ProbabilityOfHasDied)

  # create dataset
  
  return output
  pass
#    # Create DataFrame
#    df = pd.DataFrame(
#        {'Age': ages, 'SavingsAtRetirementAge': SavingsAtRetirementAge, 
#        'ProbabilityOfHasDiedM': [1 - MaleData.loc[MaleData['Age'] == age, 'Living'].values[0] / MaleData.loc[MaleData['Age'] == RetireAge, 'Living'].values[0] for age in ages],
#        'ProbabilityOfHasDiedF': [1 - FemaleData.loc[FemaleData['Age'] == age, 'Living'].values[0] / FemaleData.loc[FemaleData['Age'] == RetireAge, 'Living'].values[0] for age in ages]
#        })
#    
#    # Plotting the data
#    fig, ax1 = plt.subplots()
    
#    # Plotting savings at retirement age
#    ax1.plot(df['Age'], df['SavingsAtRetirementAge'], color='green', label='Potřebné úspory')
#    ax1.set_xlabel(f'Věk dožití s požadovaným příjmem {ExpectedAnnuityPayment} měsíčně')
#    ax1.set_ylabel(f'Potřebné úspory na dožití s {ExpectedAnnuityPayment} měsíčně')
#    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,.0f}".format(x)))
#    
#    # Creating secondary y-axis
#    ax2 = ax1.twinx()
#    
#    # Plotting probabilities
#    ax2.plot(df['Age'], df['ProbabilityOfHasDiedM'], color='blue', label='Muži')
#    ax2.plot(df['Age'], df['ProbabilityOfHasDiedF'], color='red', label='Ženy')
#    ax2.set_ylabel('Pravděpodobnost, že je člověk v daném věku po smrti')
#    # Add vertical line for DeathAge
#    ax2.axvline(x=DeathAge, color='black', linestyle='--', label=f'Věk dožití s příjmem {ExpectedAnnuityPayment}' )
#    # Add horizontal line for NecessarySavings
#   ax1.axhline(y=NecessarySavings, color='orange', linestyle='--', label=f'Potřebné úspory na příjem {ExpectedAnnuityPayment} měsíčně')
#    
#    # Displaying legend
#    ax1.legend(loc='upper left')
#    # Displaying legend
#    ax2.legend(loc='lower right')
    
    
    # Displaying the plot
#    st.pyplot(fig)
      
    

      
  
 
  