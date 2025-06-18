<h1>Next Day Stock Price Predictor</h1>
<p>
    This project enables you to predict the next day's closing prices of multiple companies and calculate the net profit or loss based on your investments. It utilizes a Linear Regression model trained on historical stock price data, taking inputs such as open, close, and high prices along with the corresponding dates.
</p>

### Table of Contents
- [Installation](#installation)
- [Project Overview](#project-overview)
- [Modules used](#modules-used)
- [References](#references)

## Installation

1. Clone the repo

```bash
git clone git@github.com:mohitdixit02/stock_price_predictor_ml.git
```

2. Setup a python (>=3.13) virtual environment (Snippet for Windows)

```bash
cd stock_price_predictor_ml
python -m venv venv
```

3. Activate the environment and install the dependencies

```bash
.\venv\Scripts\activate
pip install -r requirements.txt
```

4. Run the server script. It will start a Flask application.

```bash
python server.py
```

## Project Overview

This project allows users to predict the **next day’s closing price** of multiple companies and analyze potential profit or loss based on their investments.

### How to Use

1. **Select** a stock category and company.
2. **Input** the following details for each company:
    - Open price  
    - Close price  
    - Highest observed price  
    - Number of stocks invested  
    - Date of the recorded prices
3. You can add **multiple companies** as needed.

![Input Demo](Demo/input.png?raw=true "Input Demo")

### Output

1. **Portfolio Analysis**
    - Total invested amount  
    - Predicted total amount for the next day  
    - Overall profit or loss

2. **Individual Company Analysis**  
    - Predicted next day's closing price  
    - Predicted next day total value (predicted close price × number of stocks)  
    - Profit or loss for that company

3. **Model Prediction Analysis**
    - Model R² score (goodness of fit)  
    - Trend comparison between predicted and actual closing prices (from training data)  
    - Correlation heatmap between input features and target variable  
    - *This helps visualize how well the model performs during training before making predictions on user inputs.*

![Output Demo](Demo/portfolio.png?raw=true "Output Demo")
![Output Demo](Demo/individual.png?raw=true "Output Demo")

## Modules Used
<ol>
    <li>Numpy</li>
    <li>Matplotlib</li>
    <li>Scikit-learn</li>
    <li>Flask</li>
    <li>Pandas</li>
    <li>Seaborn</li>
</ol>

## References
Companies stock trend data is taken from the kaggle: <a href="https://www.kaggle.com/datasets/vinayak121/list-of-top-companies-in-its-sectornse-and-bse"><strong>"List of Top companies in its sector(NSE&BSE)"</strong> - By PSI (Vinayak121)</a></li>

<h4>- Thanks -</h4>
For any query, email at: mohit.vsht@gmail.com - Mohit Sharma