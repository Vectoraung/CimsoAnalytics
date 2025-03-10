let chartData = {};
let chartsInformation = {};
let savedReports = {};

function redirectData(event, chart_data, js_funtion) {
    let formObject = {};

    const chart_data_json = eval('(' + chart_data + ')');

    if (event != null){
        event.preventDefault(); // ✅ Prevent default form submission
    
        let form = event.target; // ✅ Get the form element
        let formData = new FormData(form);
        
        // Convert FormData to an object
        
        formData.forEach((value, key) => {
            formObject[key] = value;
        });
    }
    else{
            if ('filters' in chart_data_json){
                const filters = chart_data_json.filters;

                if (filters.length != 0) {
                    for (const filter of filters) {
                        formObject[filter.name] = filter.default_value;
                    }
                }
            }

            chartsInformation[chart_data_json.chart_id] = chart_data_json;
            //chartsInformation.push(chart_data_json);
        }

        console.log(formObject);
    
    if (js_funtion != null) {
        js_funtion(formObject, chart_data_json);
    }
}

function eventToObject(event) {
    let formObject = {};
    
    let form = event.target; // ✅ Get the form element
    let formData = new FormData(form);
    
    // Convert FormData to an object
    
    formData.forEach((value, key) => {
        formObject[key] = value;
    });

    return formObject
}

function chartObjectToObject(chart_data_json) {
    let formObject = {};
    if ('filters' in chart_data_json){
        const filters = chart_data_json.filters;

        if (filters.length != 0) {
            for (const filter of filters) {
                formObject[filter.name] = filter.default_value;
            }
        }
    }

    return formObject
}

function createFilterText(formObject) {
    var filterText = ""
    if (formObject != {}){
        for (const key in formObject) {
            if (formObject[key] != null) {
                filterText += `<span class="fw-normal">${key}</span>: <span style="background-color:rgba(65, 159, 227, 0.11);border-radius: 3px;">&nbsp;${formObject[key]}&nbsp;</span>, `
            }
        }
        filterText = filterText.trim().replace(/,$/, '.')
    }
    return filterText
}

function getSingleValueChartText(value) {
    var valueTextHtml = document.createElement('p');
    valueTextHtml.classList.add('m-0', 'fs-1', 'fw-bold', 'lh-1');
    valueTextHtml.style.color = '#419fe3';
    valueTextHtml.innerText = value;
    
    return valueTextHtml
}

// Helper function to get CSRF token (for Django security)
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}

async function requestData(formObject, request_url){
    try {
        let response = await fetch(`/${request_url}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken() // Include CSRF token for security
            },
            body: JSON.stringify(formObject)
        });

        let data = await response.json();
        return data.data_value;
    } catch (error) {
        console.error('Error fetching arrivals data:', error);
        return false;
    }
}

async function requestReport(chart_data, request_url){
    console.log(chartData);
    try {
        // Remove circular references from chart_data
        const sanitizedData = removeCircularReferences(chart_data);

        let response = await fetch(`/${request_url}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken() // Include CSRF token for security
            },
            body: JSON.stringify(sanitizedData)
        });

        let data = await response.json();
        return data.report;
    } catch (error) {
        console.error('Error fetching arrivals data:', error);
        return false;
    }
}


// 🔹 Global dictionary to store reports
let reportsData = {};
let currentDisplayedReport = null; // Track the currently displayed report
let currentFilledReport = []; // Stores reports already displayed

// 🔹 Save report to global variable under a specified chart title
function saveReport(reportData, chart_title) {
    if (!reportsData[chart_title]) {
        reportsData[chart_title] = [];
    }

    // Save the entire report batch (not individual items)
    reportsData[chart_title].push(reportData);
    console.log(`✅ New batch saved under "${chart_title}".`);

    // ✅ Immediately display the report instead of just updating the list
    displayReport(chart_title, true);
}

// 🔹 Refresh the report area UI
function refreshReport() {
    const reportArea = document.getElementById("reportArea");

    // If a report is currently displayed, don't refresh the list
    if (currentDisplayedReport) {
        return;
    }

    console.log("clearing report area");
    reportArea.innerHTML = ""; // Clear previous content

    if (Object.keys(reportsData).length === 0) {
        reportArea.innerHTML = "<p class='text-muted'>No reports available.</p>";
        return;
    }

    // Create the Bootstrap list-group
    let listGroup = document.createElement("div");
    listGroup.classList.add("list-group");

    Object.keys(reportsData).forEach(chart_title => {
        let listItem = document.createElement("button");
        listItem.classList.add("list-group-item", "list-group-item-action");
        listItem.style.backgroundColor = '#20204c';
        listItem.style.color = 'white';
        listItem.classList.add("d-flex");
        listItem.innerHTML = chart_title + ' <span class="ms-auto"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/></svg></span>';

        // When clicked, show reports for this title
        listItem.addEventListener("click", function () {
            displayReport(chart_title, false);
        });

        listGroup.appendChild(listItem);
    });

    reportArea.appendChild(listGroup);
}

// 🔹 Display the report for the given chart title

function displayReport(chart_title, newReport) {
    const reportArea = document.getElementById("reportArea");

    if (currentDisplayedReport !== chart_title) {
        console.log(currentDisplayedReport);
        console.log(chart_title);
        // If a report is already displayed, don't display a new one
        reportArea.innerHTML = "";
    }

    console.log(currentDisplayedReport);
    console.log(chart_title);

    // Store current displayed report
    currentDisplayedReport = chart_title;

    // Get the reports for the selected chart title
    let reportData = reportsData[chart_title];

    // Filter out already displayed reports
    let newReports = reportData.filter(report => !currentFilledReport.includes(report));

    // Append only new reports to the tracking list
    currentFilledReport = [...currentFilledReport, ...newReports];

    // If first time displaying, add the chart title
    if (!document.getElementById("reportTitle")) {
        let title_area = document.createElement("div");
        title_area.id = "title_area";
        title_area.innerHTML=`<h5 class="text-white" style="margin-top: 10px;">${chart_title}</h5>`;
        reportArea.appendChild(title_area);
    }

    if (!document.getElementById("backButton")) {
        let backButton = document.createElement("button");
        backButton.id = "backButton";
        backButton.innerText = "⬅ Back to Reports";
        backButton.classList.add("btn", "btn-secondary", "mt-3");
        backButton.addEventListener("click", function () {
            currentDisplayedReport = null;
            refreshReport(); // Restore report list
            currentFilledReport = []; // Reset reports when going back
        });
        reportArea.appendChild(backButton);
    }

    // Function to apply typewriter effect
    function typeWriterEffect(element, text, speed = 50, callback = null) {
        if (!newReport) {
            element.innerText = text; // If not a new report, set text instantly
            if (callback) callback();
            return;
        }

        let index = 0;
        element.innerText = ""; // Clear text before starting animation

        function type() {
            if (index < text.length) {
                element.innerHTML += text.charAt(index);
                index++;
                setTimeout(type, speed);
            } else if (callback) {
                callback();
            }
        }
        type();
    }

    // Append new reports only
    let reportContainer = document.createElement("div");
    reportContainer.classList.add("p-3", "text-white");

    newReports.forEach((report, reportIndex) => {
        let reportNumber = document.createElement("h6");
        reportNumber.classList.add("fw-bold", "mt-3");
        reportNumber.style.color = "rgba(255, 255, 255, 0.8)";
        reportContainer.appendChild(reportNumber);
        typeWriterEffect(reportNumber, `Report ${currentFilledReport.indexOf(report) + 1}`, 50);

        report.forEach((item) => {
            let paragraphTitle = document.createElement("h6");
            paragraphTitle.classList.add("fw-bold", "mt-2");
            reportContainer.appendChild(paragraphTitle);
            typeWriterEffect(paragraphTitle, item.paragraph_title, 30);

            let paragraphContent = document.createElement("p");
            paragraphContent.classList.add("mb-3");
            reportContainer.appendChild(paragraphContent);
            typeWriterEffect(paragraphContent, item.context, 20);
        });

        // Icon button group
        let buttonGroup = document.createElement("div");
        buttonGroup.classList.add("d-flex", "gap-2", "mt-2");

        let btn1 = document.createElement("button");
        btn1.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-copy" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M4 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1h1v1a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1v1z"/>
        </svg>`;
        btn1.classList.add("btn", "btn-sm", "btn-outline-light");

        buttonGroup.appendChild(btn1);
        reportContainer.appendChild(buttonGroup);

        // Horizontal line after each report
        let hr = document.createElement("hr");
        hr.style.borderTop = "1px solid rgba(255, 255, 255, 0.3)";
        reportContainer.appendChild(hr);
    });

    // Append only new reports to the report area
    reportArea.appendChild(reportContainer);

    // Add back button only once
    
}


// Recursive function to remove circular references
function removeCircularReferences(obj, seen = new Set()) {
    if (seen.has(obj)) return null; // If already seen, return null
    seen.add(obj);

    if (typeof obj !== 'object') return obj; // If not an object, return as is

    for (const key in obj) {
        if (typeof obj[key] === 'object') {
            obj[key] = removeCircularReferences(obj[key], seen);
        }
    }

    return obj;
}

function saveToCache(chart_data_json, formObject, value) {
    if (!(chart_data_json.chart_id in chartData)) {
        chartData[chart_data_json.chart_id] = {
            filters: chart_data_json.filters,
            chart_title: chart_data_json.chart_title,
            data: [{applied_filters: formObject, value: value}],
        };
    } else {
        chartData[chart_data_json.chart_id].data.push({applied_filters: formObject, value: value});
    }

    console.log("✅ Chart data saved to cache.");
    console.log(chart_data_json.chart_title);
    console.log(formObject);
    console.log(value);
}

async function singleValueChart(formObject, chart_data) {
    var chart_content = document.getElementById(`${chart_data.chart_id}-content`);
    var chart_title = document.getElementById(`${chart_data.chart_id}-title`);
    var filter_title = document.getElementById(`${chart_data.chart_id}-filter-title`);

    chart_content.innerHTML = ''
    chart_title.innerHTML = ''
    filter_title.innerHTML = ''

    chart_title.innerText = chart_data.chart_title;
    filter_title.innerHTML = createFilterText(formObject)

    // ✅ Wait for the data before using it
    var data_value = await requestData(formObject, chart_data.request_url);
    chartsInformation[chart_data.chart_id]["data"] = data_value;

    //saveToCache(chart_data.chart_title, {filters: formObject, value: data_value});
    saveToCache(chart_data, formObject, data_value);
    chart_content.appendChild(getSingleValueChartText(data_value));
}

function showLoadingSpinner(chart_content) {
    chart_content.innerHTML = '';
    chart_content.innerHTML = `<div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>`;
}

async function singleValueChart1(event, chart_data) {    
    var chart_content = document.getElementById(`${chart_data.chart_id}-content`);
    var chart_title = document.getElementById(`${chart_data.chart_id}-title`);
    var filter_title = document.getElementById(`${chart_data.chart_id}-filter-title`);

    showLoadingSpinner(chart_content);

    chart_title.innerHTML = ''
    filter_title.innerHTML = ''

    chart_title.innerText = chart_data.chart_title;

    let formObject = {};
    if (event) {
        event.preventDefault(); // ✅ Prevent default form submission
        formObject = eventToObject(event);
    } else {
        formObject = chartObjectToObject(chart_data);
    }
    
    filter_title.innerHTML = createFilterText(formObject)

    // ✅ Wait for the data before using it
    var data_value = await requestData(formObject, chart_data.request_url);
    //chartsInformation[chart_data_json.chart_id]["data"] = data_value;

    //saveToCache(chart_data.chart_title, {filters: formObject, value: data_value});
    saveToCache(chart_data, formObject, data_value);
    chart_content.innerHTML = ''
    chart_content.appendChild(getSingleValueChartText(data_value));
}

async function ageGroupSegmentationChart(event, chart_data) {
    var chart_content = document.getElementById(`${chart_data.chart_id}-content`);
    var chart_title = document.getElementById(`${chart_data.chart_id}-title`);

    showLoadingSpinner(chart_content);
    
    chart_title.innerHTML = '';

    chart_title.innerHTML = chart_data.chart_title;

    // Create the canvas for the bar chart
    var canvas = document.createElement('canvas');
    canvas.id = "ageGroupBarChart"; // Unique ID for the chart
    canvas.style.width = "100%";
    canvas.style.height = "70px"; // Adjust height if necessary

    let formObject = {};
    if (event) {
        event.preventDefault(); // ✅ Prevent default form submission
        formObject = eventToObject(event);
    } else {
        formObject = chartObjectToObject(chart_data);
    }

    var data_value = await requestData(formObject, chart_data.request_url);

    chart_content.innerHTML = ''; // Clear existing content
    chart_content.appendChild(canvas);
    //chartsInformation[chart_data.chart_id]["data"] = data_value;
    saveToCache(chart_data, formObject, data_value);
    const ageGroups = data_value.map(item => item.age_group);
    const counts = data_value.map(item => item.count);

    // Dummy Data for Age Group Segmentation
    createVerticalBarChart(
        "ageGroupBarChart",
        "Age Group Segmentation",
        ageGroups, // Labels
        counts // Dummy data: percentage of bookings
    );
}

function frequentlyBookedUnitsCharts(formObject, chart_data) {
    var chart_content = document.getElementById(`${chart_data.chart_id}-content`);
    var chart_title = document.getElementById(`${chart_data.chart_id}-title`);

    showLoadingSpinner(chart_content);
    chart_title.innerHTML = '';

    chart_title.innerHTML = chart_data.chart_title;

    var data = [
        { ranking: 1, unit: "Premium", bookings: 152 },
        { ranking: 2, unit: "Silver", bookings: 51 },
        { ranking: 3, unit: "Platinum", bookings: 23 },
        { ranking: 4, unit: "Gold", bookings: 18 },
        { ranking: 5, unit: "Economy", bookings: 12 } // Adding more rows to test scrolling
    ];

    //saveToCache(chart_data.chart_title, {filters: formObject, value: data});

    var tableWrapper = document.createElement("div");
    tableWrapper.style.overflowY = "auto"; // Enables scrolling inside container
    tableWrapper.style.maxHeight = "70px"; // Limits height of table to prevent pushing

    var table = document.createElement("table");
    table.classList.add("table", "table-sm", "table-striped", "mb-0");

    var thead = document.createElement("thead");
    thead.innerHTML = `
        <tr>
            <th scope="col">Ranking</th>
            <th scope="col">Unit</th>
            <th scope="col">Bookings</th>
        </tr>
    `;
    table.appendChild(thead);

    var tbody = document.createElement("tbody");
    data.forEach(item => {
        var row = document.createElement("tr");
        row.innerHTML = `
            <th scope="row">${item.ranking}</th>
            <td>${item.unit}</td>
            <td>${item.bookings}</td>
        `;
        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    tableWrapper.appendChild(table);
    chart_content.innerHTML = ''; // Clear existing content
    chart_content.appendChild(tableWrapper);
}

async function clientBirthdaysChart(formObject, chart_data) {
    var chart_content = document.getElementById(`${chart_data.chart_id}-content`);
    var chart_title = document.getElementById(`${chart_data.chart_id}-title`);
    var filter_title = document.getElementById(`${chart_data.chart_id}-filter-title`);

    showLoadingSpinner(chart_content);
    filter_title.innerHTML = '';

    filter_title.innerHTML = createFilterText(formObject);
    chart_title.innerHTML = chart_data.chart_title;

    var people = await requestData(formObject, chart_data.request_url);
    //saveToCache(chart_data.chart_title, {filters: formObject, value: people});

    var tableWrapper = document.createElement("div");
    tableWrapper.style.overflowY = "auto"; // Enables scrolling inside container
    tableWrapper.style.maxHeight = "240px"; // Limits height of table to prevent pushing

    var table = document.createElement("table");
    table.classList.add("table", "table-sm", "table-striped", "mb-0");

    var thead = document.createElement("thead");
    thead.innerHTML = `
        <tr>
            <th scope="col">First Name</th>
            <th scope="col">Last Name</th>
            <th scope="col">Birthday</th>
        </tr>
    `;
    table.appendChild(thead);

    var tbody = document.createElement("tbody");
    people.forEach(person => {
        var row = document.createElement("tr");
        row.innerHTML = `
            <th scope="row">${person.firstName}</th>
            <td>${person.lastName}</td>
            <td>${person.birthday}</td>
        `;
        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    tableWrapper.appendChild(table);
    chart_content.innerHTML = ''; // Clear existing content
    chart_content.appendChild(tableWrapper);
}

function generateYearlyRevenue() {
    let currentYear = 2025; // Set the base year
    let years = [];

    // Generate years (5 years before and 5 years after the current year)
    for (let i = -5; i <= 5; i++) {
        years.push(currentYear + i);
    }

    // Generate random revenue for each year
    let yearlyRevenue = years.map(year => ({
        year: year,
        revenue: Math.floor(Math.random() * 50000) + 50000 // Revenue between 50K - 550K
    }));

    return { years, yearlyRevenue };
}

function renderYearlyChart(formObject, chart_data) {
    var chart_content = document.getElementById(`${chart_data.chart_id}-content`);
    var chart_title = document.getElementById(`${chart_data.chart_id}-title`);

    showLoadingSpinner(chart_content);
    chart_content.innerHTML = '';
    chart_title.innerHTML = "Total income by current month and by current year";

    let canvas = document.createElement("canvas");
    canvas.id = "revenueChart";
    //canvas.style.width = "100%";
    //canvas.style.height = "250px";
    chart_content.appendChild(canvas);

    let { years, yearlyRevenue } = generateYearlyRevenue();

    currentChart = createLineChart(
        "revenueChart",
        years, // X-axis labels
        [{
            label: "Yearly Revenue ($)",
            data: yearlyRevenue.map(y => y.revenue),
            borderColor: "#36A2EB",
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            fill: true
        }]
    );
}

function generateMonthlyBookings2025() {
    let months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ];

    let bookings = months.map(() => Math.floor(Math.random() * 500) + 50); // 50-550 bookings

    return { months, bookings };
}

async function renderBookingsChart(formObject, chart_data) {
    var chart_content = document.getElementById(`${chart_data.chart_id}-content`);
    var chart_title = document.getElementById(`${chart_data.chart_id}-title`);
    var filter_title = document.getElementById(`${chart_data.chart_id}-filter-title`);

    showLoadingSpinner(chart_content);
    filter_title.innerHTML = '';

    filter_title.innerHTML = createFilterText(formObject);
    chart_title.innerHTML = chart_data.chart_title;

    var canvas = document.createElement("canvas");
    canvas.id = "bookingsChart";
    //canvas.style.width = "100%";
    //canvas.style.height = "250px"; // Adjust height for visibility
    

    var data_value = await requestData(formObject, chart_data.request_url);
    //saveToCache(chart_data.chart_title, {filters: formObject, value: data_value});

    chart_content.innerHTML = ''; // Clear previous content
    chart_content.appendChild(canvas);

    createHorizontalBarChart(
        "bookingsChart",
        data_value.months, // Y-axis labels (months)
        data_value.bookings, // X-axis values (booking counts)
        "rgba(54, 162, 235, 0.7)" // Bar color (blue)
    );
}
