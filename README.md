# Virtual Crypto Trading System

### Primary Language: Python 3.6

### Highlight: 

#### 1.Data storage in MongoDB, NoSQL Database System;   
#### 2.Pandas Dataframes applied throughout the project;   
#### 3.Crypto Currency API (specifically GDAX) used to pull real-time and historical prices;   
#### 4.Data visualization: moving average and volatility graphs;     
#### 5.Financial concepts included.  

### Procedure:

When the program is execuated, a list of 4 selection would be shown which are Trade, Show Blotter, Show P/L and Exit.

1. Trade is the platform for user to enter the ticker of an interested crypto currency, evaluate the performance of the currency (given a series of valuable analytics and visualization tools), and execuate the trade by entering the quantity. Any execuated trade will be permanently stored in MongoDB as long as a collection is set.

2. Show Blotter would pull and display all trade history from MongoDB and print in an neat form.

3. Similarly, Show P/L function would display P/L information for each currency bought. 

4. The program will not terminated untill Exit option is selected.

*detailed information and explanation are presented as comments along with the program.
