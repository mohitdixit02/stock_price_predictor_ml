from flask import Flask, request, jsonify, render_template
from data import load_file_urls
from model import predict_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_next_day')
def result():
    return render_template('result.html')
    
@app.route('/api/data', methods=['GET'])
def get_data():
    data = load_file_urls()
    return data
    
@app.route('/api/predict_next_day', methods=['POST'])
def predict():
    input_data = request.json
    file_urls = load_file_urls()
    input_array = []
    
    for data in input_data:
        input_category = data.get('category').lower()
        input_company = data.get('company').lower()
        input_high = float(data.get('highPrice'))
        input_open = float(data.get('openPrice'))
        input_close = float(data.get('closePrice'))
        input_date = data.get('date')
        input_stocks_no = int(data.get('numberOfStocks'))
    
        path = next((i["path"] for i in file_urls[input_category] if i["name"] == input_company), "")        
        input_array.append({
            "path": path,
            "data": [input_close, input_high, input_open, input_date],
            "stocks_no": input_stocks_no
        })
    
    res = predict_data(input_array)
    return jsonify(res)
    
if __name__ == '__main__':
    app.run(debug=True)