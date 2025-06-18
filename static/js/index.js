const fetch_data = async () => {
    let data = await fetch('/api/data').then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });

    const select = document.getElementById('available_categories_select');
    select.innerHTML = ''; // Clear existing options
    const defaultOption = document.createElement('option');
    defaultOption.value = "--";
    defaultOption.textContent = "Select Category";
    select.appendChild(defaultOption);
    Object.keys(data).forEach(key => {
        const option = document.createElement('option');
        option.value = key;
        option.textContent = key.toUpperCase();
        select.appendChild(option);
    });
    select.addEventListener('change', (event) => {
        const selectedCategory = event.target.value;
        const items = data[selectedCategory] || [];

        const itemsSelect = document.getElementById('available_companies_select');
        itemsSelect.innerHTML = '';
        items.forEach(item => {
            const option = document.createElement('option');
            option.value = item.name;
            option.textContent = item.name.toUpperCase();
            itemsSelect.appendChild(option);
        });
    });
}


let addedCompanies = [];

fetch_data();

document.getElementById("predict-btn").addEventListener("click", (e) => {
    e.preventDefault();

    const category = document.getElementById("available_categories_select").value.toUpperCase();
    const company = document.getElementById("available_companies_select").value.toUpperCase();
    const openPrice = document.querySelector("input[name='open_price']").value;
    const highPrice = document.querySelector("input[name='high_price']").value;
    const closePrice = document.querySelector("input[name='close_price']").value;
    const numberOfStocks = document.querySelector("input[name='number_of_stocks']").value;
    const date = document.querySelector("input[name='date']").value;

    if (company === "--" || !openPrice || !highPrice || !closePrice || !numberOfStocks || !date) {
        alert("Please fill all fields!");
        return;
    }

    const record = {
        category,
        company,
        openPrice,
        highPrice,
        closePrice,
        numberOfStocks,
        date
    };
    addedCompanies.push(record);

    const tbody = document.querySelector("#added-companies-table tbody");
    const tr = document.createElement("tr");
    tr.innerHTML = `
            <td>${category}</td>
            <td>${company}</td>
            <td>${openPrice}</td>
            <td>${highPrice}</td>
            <td>${closePrice}</td>
            <td>${numberOfStocks}</td>
            <td>${date}</td>
        `;
    tbody.appendChild(tr);

    document.querySelector("input[name='open_price']").value = "";
    document.querySelector("input[name='high_price']").value = "";
    document.querySelector("input[name='close_price']").value = "";
    document.querySelector("input[name='number_of_stocks']").value = "";
    document.querySelector("input[name='date']").value = "";
});


document.getElementById("predict-next-day-btn").addEventListener("click", () =>{
    if(addedCompanies.length === 0) {
        alert("Please add at least one company to predict the next day's prices.");
        return;
    }

    localStorage.setItem("addedCompanies", JSON.stringify(addedCompanies));
    window.location.href = "/predict_next_day";
})

