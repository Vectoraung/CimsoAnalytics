function createChart(chartId, title, data, titles) {
    var data = data;

    var layout = {
        title: title,
        xaxis: { title: titles.x_axis_title, color: "#fff" },
        yaxis: { title: titles.y_axis_title, color: "#fff" },
        plot_bgcolor: "#20204c",
        paper_bgcolor: "#20204c",
        font: { color: "#fff" },
        margin: { 
            t: 40,  // Top margin
            l: 80,  // Left margin
            r: 10,  // Right margin
            b: 40,  // Bottom margin
            pad: 0 // Extra padding around the plot
        },
        autosize: true
    };

    Plotly.newPlot(chartId, data, layout, {
        displayModeBar: false,  // Hide the default mode bar
        responsive: true
    });
}