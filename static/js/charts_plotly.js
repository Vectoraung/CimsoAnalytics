function showLoadingSpinner(chartId) {
    document.getElementById(chartId).innerHTML ='';
    document.getElementById(chartId).innerHTML = `<div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>`;
}

function createChart(chartId, title, data, titles, additional_layout_config) {
    var data = data;

    var layout = {
        /*title: {
            text: title,
            font: {
                size: 16,
                color: "#fff",
                bold: true,
                margin: {
                    b: 0, // bottom margin
                    l: 10, // left margin
                    r: 10, // right margin
                    t: 10  // top margin
                  }
            }
        },*/
        xaxis: {
            //title: titles.x_axis_title,
            color: "#fff",
            zerolinecolor: "#3b3e61",
            zerolinewidth: 0.5,
            tickcolor: 'rgba(255, 255, 255, 0)' ,
            ticklen: 5
        },
        yaxis: {
            //title: titles.y_axis_title,
            color: "#fff",
            zerolinecolor: "#3b3e61",  // Change baseline color
            zerolinewidth: 0.5,
            tickcolor: 'rgba(255, 255, 255, 0)',
            ticklen: 5
        },
        plot_bgcolor: "#20204c",
        paper_bgcolor: "#20204c",
        font: { color: "#fff" },
        margin: { 
            t: 5,  // Top margin
            l: 45,  // Left margin
            r: 10,  // Right margin
            b: 25,  // Bottom margin
            pad: 0 // Extra padding around the plot
        },
        autosize: true
    };

    layout = { ...layout, ...additional_layout_config };

    var chart = document.getElementById(chartId);
    chart.innerHTML = '';

    Plotly.newPlot(chartId, data, layout, {
        displayModeBar: false,  // Hide the default mode bar
        responsive: true
    });
}

function createSingleValueChart(titleElementId, valueElementId, title, value) {
    const titleElement = document.getElementById(titleElementId);
    const valueElement = document.getElementById(valueElementId);
  
    titleElement.innerText = '';
    valueElement.innerText = '';
  
    titleElement.innerText = title;
    valueElement.innerText = value;
  }

  function createTable(parentElementId, data) {
    const parentElement = document.getElementById(parentElementId);
    parentElement.innerHTML = '';
    // Create the table element
    const table = document.createElement('table');
    table.classList.add('chart-table'); // Add a class for styling
  
    // Create the table header
    const headerRow = document.createElement('tr');
    const headers = ['First Name', 'Last Name', 'Birthday'];
    headers.forEach(header => {
      const th = document.createElement('th');
      th.textContent = header;
      headerRow.appendChild(th);
    });
    table.appendChild(headerRow);
  
    // Create the table rows
    data.forEach(person => {
      const row = document.createElement('tr');
      const cells = [
        document.createElement('td'),
        document.createElement('td'),
        document.createElement('td')
      ];
      cells[0].textContent = person.firstName;
      cells[1].textContent = person.lastName;
      cells[2].textContent = person.birthday;
      cells.forEach(cell => row.appendChild(cell));
      table.appendChild(row);
    });
  
    // Append the table to the parent element
    parentElement.appendChild(table);
  }