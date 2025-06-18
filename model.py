import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import io
import base64

def predict_close_value(file_path, input_val):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df["is_quarter_end"] = np.where(df['Month']%3 == 0, True, False)
    df['Next_Close'] = df['Close'].shift(-1)
    df = df[:-1]

    x_cord = df[['Close', 'High', 'Open', 'Month', 'is_quarter_end']]
    y_cord = df['Next_Close']

    # Create a Linear Regression model
    print("Training the model...")
    model = LinearRegression()
    x_train, x_test, y_train, y_test = train_test_split(x_cord, y_cord, test_size=0.2, random_state=42)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    img_data = plot_data(y_test, y_pred, df)
    
    # Calculate R-squared score
    r2_score_val = r2_score(y_test, y_pred)
    print(f"R-squared score: {r2_score_val:.4f}")
    
    input_month = int(input_val[-1].split("-")[1])
    is_quarter_end = True if input_month%3 == 0 else False
    
    model_input = input_val[:-1]
    model_input.append(input_month)
    model_input.append(is_quarter_end)
    model_input = pd.DataFrame([model_input], columns = x_cord.columns)
    
    y_user_pred = model.predict(model_input)
    return y_user_pred, img_data, r2_score_val


def plot_data(y_test, y_pred, df):
    # Correlation Heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(df[
        ['High', 'Low', 'Open', 'Close', 'Volume', 'Year', 'Month', 'is_quarter_end', 'Next_Close']].corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Heatmap')
    buf1 = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf1, format='png')
    buf1.seek(0)
    img_bytes_1 = buf1.getvalue()
    img_base64_1 = base64.b64encode(img_bytes_1).decode('utf-8')
    buf1.close()

    # Actual vs Predicted Plot over time
    plt.figure(figsize=(12, 10))
    plt.plot(y_test.values, label = 'Actual Close Price', color='blue', marker='o', linestyle='-')
    plt.plot(y_pred, label = 'Predicted Close Price', color='red', marker='x', linestyle='--')
    plt.title('Actual vs Predicted Close Prices Over Time')
    plt.xlabel('Sample Index')
    plt.ylabel('Close Price')
    plt.legend()
    plt.grid()
    buf2 = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf2, format='png')
    buf2.seek(0)
    img_bytes_2 = buf2.getvalue()
    img_base64_2 = base64.b64encode(img_bytes_2).decode('utf-8')
    buf2.close()

    # plot y_test vs x_test
    plt.figure(figsize=(12, 10))
    plt.scatter(y_test, y_pred, color='blue', alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', lw=2, linestyle='--')
    plt.title('Actual vs Predicted Close Prices')
    plt.xlabel('Actual Close Price')
    plt.ylabel('Predicted Close Price')
    plt.grid()
    buf3 = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf3, format='png')
    buf3.seek(0)
    img_bytes_3 = buf3.getvalue()
    img_base64_3 = base64.b64encode(img_bytes_3).decode('utf-8')
    buf3.close()
    
    return [img_base64_1, img_base64_2, img_base64_3]
    
def predict_data(data):
    res = []
    predicted_total_portfolio_value = 0
    total_portfolio_value = 0
    portfolio_net = 0
    
    for elem in data:
        y_res, img_data, r2_score_val = predict_close_value(elem["path"], elem["data"])
        y_pred_value = y_res.item()
        file_name = elem["path"].split("/")[-1]
        close_val = elem["data"][0]
        number_of_stocks = elem["stocks_no"]
        total_net_change = (y_pred_value - close_val)*number_of_stocks
        predicted_total_portfolio_value += (y_pred_value * number_of_stocks)
        total_portfolio_value += (close_val * number_of_stocks)
        portfolio_net += total_net_change
        res.append({
            "company": file_name.split(".csv")[0],
            "predicted_close_price": f"{y_pred_value:.2f}",
            "predicted_total_price": f"{(y_pred_value*number_of_stocks):.2f}",
            "Status": "Profit" if close_val <= y_pred_value else "Loss",
            "amount": f"{(total_net_change):.2f}",
            "plot": img_data,
            "r2_score": f"{r2_score_val:.4f}"
        })

    return {
        "predicted_total_portfolio_value": f"{predicted_total_portfolio_value:.2f}",
        "total_portfolio_value": f"{total_portfolio_value:.2f}",
        "portfolio_net_amount": f"{portfolio_net:.2f}",
        "portfolio_net_status": "Profit" if portfolio_net > 0 else "Loss",
        "individual": res,
    }