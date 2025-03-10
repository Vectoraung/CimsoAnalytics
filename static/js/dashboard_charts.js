function createPieChart(chartId, label, labels, data, backgroundColors, borderColors = null) {
    const ctx = document.getElementById(chartId).getContext("2d");
    return new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: backgroundColors,
                borderColor: borderColors || backgroundColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: "white", font: { size: 14 } }
                },
                title: {
                    display: false,
                    text: label,
                    color: "white",
                    font: { size: 18 }
                }
            }
        }
    });
}

/*
Example usage
createPieChart("chart6", "Sales Distribution", [12, 19, 3, 5, 2], [
    "rgba(255, 99, 132, 0.6)",
    "rgba(54, 162, 235, 0.6)",
    "rgba(255, 206, 86, 0.6)",
    "rgba(75, 192, 192, 0.6)",
    "rgba(153, 102, 255, 0.6)"
]);
*/

function createVerticalBarChart(chartId, label, labels, data) {
    const ctx = document.getElementById(chartId).getContext("2d");
    return new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: "rgba(65,159,227,255)",
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: "white", font: { size: 10 } },
                    grid: { color: "rgba(255, 255, 255, 0)" }
                },
                x: {
                    ticks: { color: "white", font: { size: 10 } },
                    grid: { color: "rgba(255, 255, 255, 0)" }
                }
            },
            plugins: {
                legend: {
                    display: false // Hide default legend for a cleaner look
                },
                title: {
                    display: false,
                    text: label,
                    color: "white",
                    font: { size: 18 }
                }
            }
        }
    });
}


function createStackedBarChart(chartId, labels, datasets) {
    const ctx = document.getElementById(chartId).getContext("2d");

    return new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels, // X-axis labels
            datasets: datasets // Multiple datasets for stacking
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    stacked: true, // ✅ Enable stacking on X-axis
                    ticks: {
                        color: "white" // ✅ X-axis label color
                    },
                    grid: {
                        display: false // ✅ Hide X-axis grid
                    }
                },
                y: {
                    stacked: true, // ✅ Enable stacking on Y-axis
                    ticks: {
                        color: "white" // ✅ Y-axis label color
                    },
                    grid: {
                        display: false // ✅ Hide Y-axis grid
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: "white", // ✅ Legend label color
                        font: { size: 14 }
                    }
                },
                title: {
                    display: false, // Change to true if needed
                    text: "Stacked Bar Chart",
                    color: "white",
                    font: { size: 18 }
                }
            }
        }
    });
}

/*
Example Usage
createStackedBarChart("chart7", ["Jan", "Feb", "Mar", "Apr", "May"], [
    {
        label: "Product A",
        data: [10, 20, 30, 40, 50],
        backgroundColor: "rgba(255, 99, 132, 0.6)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 1
    },
    {
        label: "Product B",
        data: [15, 25, 35, 45, 55],
        backgroundColor: "rgba(54, 162, 235, 0.6)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1
    },
    {
        label: "Product C",
        data: [5, 15, 25, 35, 45],
        backgroundColor: "rgba(255, 206, 86, 0.6)",
        borderColor: "rgba(255, 206, 86, 1)",
        borderWidth: 1
    }
]);
*/

function createSideBySideBarChart(chartId, labels, datasets) {
    const ctx = document.getElementById(chartId).getContext("2d");

    return new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels, // X-axis labels
            datasets: datasets // Multiple datasets for side-by-side bars
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    stacked: false, // ✅ Side-by-side bars (not stacked)
                    ticks: {
                        color: "white" // ✅ X-axis label color
                    },
                    grid: {
                        display: false // ✅ Hide X-axis grid
                    }
                },
                y: {
                    stacked: false, // ✅ Side-by-side (not stacked)
                    ticks: {
                        color: "white" // ✅ Y-axis label color
                    },
                    grid: {
                        display: false // ✅ Hide Y-axis grid
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: "white", // ✅ Legend label color
                        font: { size: 14 }
                    }
                },
                title: {
                    display: false, // Set to true if needed
                    text: "Side-by-Side Bar Chart",
                    color: "white",
                    font: { size: 18 }
                }
            }
        }
    });
}

/*
createSideBySideBarChart("chart8", ["Jan", "Feb", "Mar", "Apr", "May"], [
    {
        label: "Product A",
        data: [10, 20, 30, 40, 50],
        backgroundColor: "rgba(255, 99, 132, 0.6)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 1
    },
    {
        label: "Product B",
        data: [15, 25, 35, 45, 55],
        backgroundColor: "rgba(54, 162, 235, 0.6)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1
    },
    {
        label: "Product C",
        data: [5, 15, 25, 35, 45],
        backgroundColor: "rgba(255, 206, 86, 0.6)",
        borderColor: "rgba(255, 206, 86, 1)",
        borderWidth: 1
    }
]);

*/
function createLineChart(chartId, labels, datasets) {
    const ctx = document.getElementById(chartId).getContext("2d");

    return new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    ticks: { color: "white" },
                    grid: { display: false }
                },
                y: {
                    ticks: { color: "white" },
                    grid: { color: "rgba(255, 255, 255, 0.2)" }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: "white",
                        font: { size: 14 }
                    }
                },
                tooltip: { mode: "index", intersect: false }
            }
        }
    });
}

function createHorizontalBarChart(chartId, labels, data, backgroundColor) {
    const ctx = document.getElementById(chartId).getContext("2d");

    return new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels, // Y-axis labels (months)
            datasets: [{
                data: data, // Booking numbers
                backgroundColor: backgroundColor, // Single color for all bars
                borderWidth: 1,
                //barThickness: 7,
                categoryPercentage: 1, // ✅ Adjusts space per category (default 1.0)
                barPercentage: 0.5 // ✅ Adjusts individual bar width inside category
            }]
        },
        options: {
            indexAxis: 'y', // ✅ Converts it into a horizontal bar chart
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    ticks: { color: "white", font: { size: 12 } },
                    grid: { color: "rgba(255, 255, 255, 0.2)" }
                },
                y: {
                    ticks: { color: "white", font: { size: 12 } },
                    grid: { display: false }
                }
            },
            plugins: {
                legend: { display: false }, // ✅ Hide legend for cleaner look

            }
        }
    });
}
