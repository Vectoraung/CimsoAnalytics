let currentOpenedReport = null;
let generatedReports = {};

function addExistingReports(chartTitle) {
    const element = document.getElementById('report-area');
    if (!element) return;

    // If the chartTitle is new, clear the content before adding new data
    if (currentOpenedReport !== chartTitle) {
        element.innerHTML = '';

        // Add back button
        const buttonHtml = `<button type="button" class="btn btn-outline-light" onclick="goBack();">Back</button>`;
        element.innerHTML += buttonHtml;

        // Add the chart title
        element.innerHTML += `<h5 class="text-white" style="margin-top: 10px;">${chartTitle}</h5>`;
    }

    if (generatedReports[chartTitle] && generatedReports[chartTitle].length > 0) {
        generatedReports[chartTitle].forEach((item) => {
          item.forEach((paragraph) => {
            let paragraphContainer = document.createElement("div"); // Create a container for each paragraph
            let titleElement = document.createElement("h6");
            let paragraphElement = document.createElement("p");
      
            titleElement.innerHTML = paragraph.paragraph_title; // Set title
            paragraphElement.innerHTML = paragraph.context; // Set context
      
            paragraphContainer.appendChild(titleElement);
            paragraphContainer.appendChild(paragraphElement);
            element.appendChild(paragraphContainer); // Append new paragraph
          });

          element.innerHTML += `<div class="btn-group me-2" role="group" aria-label="First group">
          <button type="button" class="btn btn-outline-secondary">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-copy" viewBox="0 0 16 16">
          <path fill-rule="evenodd" d="M4 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1h1v1a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1v1z"/>
          </svg>
          </button>
          </div>`;

            let hr = document.createElement("hr");
            element.appendChild(hr);
        });
    }

    // Update the current opened report
    currentOpenedReport = chartTitle;
}

function goBack() {
    const reportArea = document.getElementById("report-area");
    if (!reportArea) return;

    reportArea.innerHTML = ''; // Clear existing content

    const keys = Object.keys(generatedReports);

    // Create the list-group container
    const listGroup = document.createElement("div");
    listGroup.classList.add("list-group");

    keys.forEach((key, index) => {
        let listItem = document.createElement("a");
        listItem.href = "#";
        listItem.classList.add("list-group-item", "list-group-item-action");

        if (index === 0) {
            listItem.setAttribute("aria-current", "true");
        }

        listItem.textContent = key;

        // Set an onclick event to open the report when clicked
        listItem.onclick = function () {
            // Load the selected report (use typeWriterEffect if you want the typing animation)
            addExistingReports(key);
        };

        listGroup.appendChild(listItem);
    });

    reportArea.appendChild(listGroup);
    currentOpenedReport = null;
}

function typeWriterEffect(elementId, data, chartTitle, speed = 20, delayBetween = 500) {
    const element = document.getElementById(elementId);
    if (!element) return;

    // If the chartTitle is new, clear the content before starting animation
    if (currentOpenedReport !== chartTitle) {
        element.innerHTML = '';

        const buttonHtml = `<button type="button" class="btn btn-outline-light" onclick="goBack();">Back</button>`;
        element.innerHTML += buttonHtml;
        element.innerHTML += `<h5 class="text-white" style="margin-top: 10px;">${chartTitle}</h5>`;

        addExistingReports(chartTitle);
    } else {
        if (generatedReports[chartTitle]) {
            
        }
        
    }

    let index = 0;

    function typeParagraph() {
        if (index >= data.length) {
            element.innerHTML += `<div class="btn-group me-2" role="group" aria-label="First group">
            <button type="button" class="btn btn-outline-secondary">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-copy" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M4 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1h1v1a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1v1z"/>
            </svg>
            </button>
            </div>`;
            
            // If it's the same title, add a horizontal line to separate new content
            let hr = document.createElement("hr");
            element.appendChild(hr);
            return;
        } // Stop if all data is processed

        const title = data[index].paragraph_title;
        const context = data[index].context;

        let paragraphContainer = document.createElement("div"); // Create a new container for this paragraph
        let titleElement = document.createElement("h6");
        let paragraphElement = document.createElement("p");

        titleElement.innerHTML = title; // Set title instantly
        paragraphContainer.appendChild(titleElement);
        paragraphContainer.appendChild(paragraphElement);
        element.appendChild(paragraphContainer); // Append new paragraph to the container

        let i = 0;
        function type() {
            if (i < context.length) {
                paragraphElement.innerHTML = context.substring(0, i + 1); // Append text gradually
                i++;
                setTimeout(type, speed);
            } else {
                index++; // Move to the next paragraph
                setTimeout(typeParagraph, delayBetween); // Delay before next paragraph starts
            }
        }

        type();
    }

    typeParagraph();

    // Update the current opened report
    currentOpenedReport = chartTitle;
}

async function generateReport(chartTitle){
    var selectedValue = document.getElementById("report-lang-btn").textContent;
    try {
        await fetch('/generate-report-plotly/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken() // Include CSRF token for security
            },
            body: JSON.stringify({title: chartTitle, language: selectedValue}),
        })
        .then(response => response.json())
        .then(data => {
            const collapseElement = document.getElementById('reportAreaCollapse');
            if (!collapseElement.classList.contains('show')) {
                const collapse = new bootstrap.Collapse(collapseElement);
                collapse.show();
            }

            typeWriterEffect("report-area", data.report.report, chartTitle);

            if (!(chartTitle in generatedReports)) {
                generatedReports[chartTitle] = [data.report.report];
            } else {
                generatedReports[chartTitle].push(data.report.report);
            }
        })
        .catch(error => console.error('Error fetching arrivals data:', error));
    } catch (error) {
        console.error('Error fetching arrivals data:', error);
    }
}
