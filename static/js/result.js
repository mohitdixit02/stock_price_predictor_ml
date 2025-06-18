const predict_result = () => {
    addedCompanies = localStorage.getItem("addedCompanies") ? JSON.parse(localStorage.getItem("addedCompanies")) : [];
    if (addedCompanies.length == 0) {
        alert("No companies added yet. Please add companies to predict the next day's prices.");
        window.location.href = "/";
        return;
    }

    fetch('/api/predict_next_day', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(addedCompanies)
        // body: JSON.stringify(temp_res)
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        document.querySelector('.portfolio_main .portfolio_data_holder_left .data_predicted_portoflio_ul').innerHTML = `
            <div>INR ${data.total_portfolio_value}</div>
            <div>INR ${data.predicted_total_portfolio_value}</div>
        `;
        document.querySelector('.portfolio_right .profit_loss_type').innerText = data.portfolio_net_status;
        document.querySelector('.portfolio_right div:nth-child(2)').innerText = (data.portfolio_net_status === "Profit" ? "+" : "-") + data.portfolio_net_amount;
        document.querySelector('.portfolio_right div:nth-child(2)').className = data.portfolio_net_status === "Profit" ? "profit_theme" : "loss_theme";

        let portfolioIndividualContainer = document.querySelector('.portfolio_individual_holder');
        portfolioIndividualContainer.innerHTML = '';

        data.individual.forEach(company => {
            const companyDiv = document.createElement('div');
            companyDiv.className = 'portfolio_individual';
            companyDiv.innerHTML = `
                <div class="portfolio_individual_left">
                    <div class="company_name_holder">
                        Company
                        <div>${company.company}</div>
                    </div>
                    <div class="company_individual_data_holder_left">
                        <ul type="none">
                            <li>Predicted Stock Close Price: </li>
                            <li>Predicted Total Stocks Price: </li>
                        </ul>
                        <ul type="none" class="data_predicted_portoflio_ul">
                            <div>INR ${company.predicted_close_price}</div>
                            <div>INR ${company.predicted_total_price}</div>
                        </ul>
                    </div>
                </div>
                <div class="portfolio_individual_right">
                    <div>${company.Status}</div>
                    <div class=${company.Status === 'Profit' ? "profit_theme" : "loss_theme"}>${company.Status === 'Profit' ? '+' : '-'}${company.amount}</div>
                </div>
            `;
            portfolioIndividualContainer.appendChild(companyDiv);
        });

        let modelPredictionContainer = document.querySelector('.model_prediction_main_holder');
        modelPredictionContainer.innerHTML = '';  // clear old content

        data.individual.forEach((company, idx) => {
            const modelDiv = document.createElement('div');
            modelDiv.className = 'model_prediction_main';
            modelDiv.innerHTML = `
                <div class="model_prediction_container">
                    <div class="model_predition_text_holder">
                        Company
                        <div>${company.company}</div>
                    </div>
                    <div class="model_predition_r2_score">
                        R2 Score: ${company.r2_score}
                    </div>
                </div>
                <div class="model_prediction_plot">
                    <div>
                        <img style="max-width:49%;" src="data:image/png;base64,${company.plot[1]}">
                        <img style="max-width:49%;" src="data:image/png;base64,${company.plot[2]}">
                    </div>
                    <img style="max-width:49%;" src="data:image/png;base64,${company.plot[0]}">
                </div>
            `;
            modelPredictionContainer.appendChild(modelDiv);
        });
    }).catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
        alert("An error occurred while predicting the next day's prices. Please try again.");
    });
}

predict_result();