function zoomIn(chartId) {
    Plotly.relayout(chartId, {
        'xaxis.range': [0.5, 3.5], // Adjust these values dynamically based on data range
        'yaxis.range': [500, 2000]  // Adjust zoom level
    });
}

function zoomOut(chartId) {
    Plotly.relayout(chartId, {
        'xaxis.autorange': true,  // Reset to default range
        'yaxis.autorange': true
    });
}

function saveChartAsImage(chartId) {
    Plotly.downloadImage(chartId, {
        format: 'png',  // You can change this to 'jpeg', 'svg', or 'webp'
        filename: 'chart_snapshot',
    });
}

function resetChart(chartId) {
    Plotly.relayout(chartId, { "xaxis.autorange": true, "yaxis.autorange": true });
}