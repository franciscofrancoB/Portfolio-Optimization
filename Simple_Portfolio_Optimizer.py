#############################################################
#                                                           #
#     Simple Portfolio Optimizer (© Francisco Boudagh)       #
#                                                           #
#  This code is copyrighted by Francisco Boudagh. You are  #
#  free to use and modify the code for personal and         #
#  non-commercial purposes. However, you are not allowed     #
#  to sell or distribute the code without explicit          #
#  permission from the author.                             #
#  Please check the README and LICENSE files.               #
#                                                            #
##############################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import yfinance as yf
import datetime

##########################################################
# Data Importation Section
selected_stocks = input("Enter the stocks (ticker symbols separated by commas) you want to optimize the portfolio for (e.g.: AAPL, GOOG): ")
# Modifying the input (if needed)
selected_stocks = [stock.strip().upper() for stock in selected_stocks.split(",")]

assets_data = {}

# Change the start date for the downloaded historical data as desired
# End date is set to today
end_date = datetime.date.today()
start_date = '2010-01-01'

# Loop through the selected stocks
for stock in selected_stocks:
    # Download historical data from Yahoo Finance
    data = yf.download(stock, start=start_date, end=end_date)

    # Extract Close prices
    close_prices = data['Close']
    assets_data[stock] = close_prices

assets_data = pd.DataFrame(assets_data)

##########################################################
# Optimization Section
returns = assets_data.pct_change().dropna()
volatility = returns.std()

def objective(weights):
    portfolio_returns = np.dot(returns, weights)
    portfolio_volatility = np.sqrt(np.dot(weights, np.dot(returns.cov(), weights)))
    # Adjust the risk aversion parameter, values from 0 to 1
    # Low value means high returns and high risk, and vice versa
    risk_aversion = 0.5
    utility = portfolio_returns - risk_aversion * portfolio_volatility
    return -utility.sum()

def constraint(weights):
    return np.sum(weights) - 1

num_assets = len(returns.columns)
init_weights = np.array([1/num_assets] * num_assets)
bounds = [(0, 1)] * num_assets

opt_problem = {'type': 'eq', 'fun': constraint}
opt_result = minimize(objective, init_weights, method='SLSQP', bounds=bounds, constraints=opt_problem)

optimized_weights = opt_result.x

##########################################################
# 3D Plotting Section, remove this section if you don't want 3D plot
n_points = 100
returns_range = np.linspace(returns.min().min(), returns.max().max(), n_points)
volatility_range = np.linspace(volatility.min().min(), volatility.max().max(), n_points)
returns_grid, volatility_grid = np.meshgrid(returns_range, volatility_range)

utility_grid = np.zeros_like(returns_grid)
for i in range(n_points):
    for j in range(n_points):
        weights = np.array([1/num_assets] * num_assets)
        weights[0] = returns_grid[i, j]
        weights[1] = volatility_grid[i, j]
        utility_grid[i, j] = -objective(weights)

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
obj_plot = ax.plot_surface(returns_grid, volatility_grid, utility_grid, cmap='inferno')
plt.colorbar(obj_plot)
ax.set_xlabel('Portfolio Returns')
ax.set_ylabel('Portfolio Volatility')
ax.set_zlabel('Objective Function')
ax.set_title('Objective Function (Allocation Attractiveness)')
plt.show()

##########################################################
# Print Portfolio Allocation
for i, asset in enumerate(returns.columns):
    print(f"{asset}: {optimized_weights[i] * 100:.2f}%")

portfolio_returns = (np.dot(returns + 1, optimized_weights) - 1).cumsum()
portfolio_volatility = np.sqrt(np.dot(optimized_weights, np.dot(returns.cov(), optimized_weights)))

print(f"Portfolio Volatility: {portfolio_volatility * 100:.2f}%")