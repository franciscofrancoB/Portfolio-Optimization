# Portfolio-Optimization
Welcome to the Simple Portfolio Optimizer!

I want to emphasize that I'm far from being a finance expert. This tool was created purely as a hobby project.
Please keep in mind that any investment decisions you make based on the results are your responsibility.
I cannot be held liable for any financial gains or losses resulting from the use of this tool.

Here's how it works:

1. You choose the stocks you want to include in your portfolio.
2. The optimizer retrieves historical data (5 yrs., you can change it) for those stocks.
3. It calculates the returns and volatility (risk) for each stock.
4. Using the SLSQP optimization algorithm and the mathematical model of Markowitz portfolio optimization theory,
   it finds the best combination of stocks that maximizes returns while minimizing risk
   (weighting them equally, aversion parameter = 0.5, you can adjust this).
5. The optimizer generates the optimized portfolio allocation, indicating the recommended percentage for each stock.

You can use this allocation as a guide to structure your investment portfolio.
Even though the optimizer uses Markowitz portfolio optimization theory, it is done by a simplified approach.
It's essential to conduct your own research before making any investment decisions.

Note: This is not a unique idea, and similar portfolio optimizers have been implemented by several people in different ways.

You are free to use and modify the code for personal and non-commercial purposes.
However, you are not allowed to sell or distribute the code without explicit permission from the author.
