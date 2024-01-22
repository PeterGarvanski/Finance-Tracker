document.addEventListener('DOMContentLoaded', function () {
    // Collects data from html element
    let nameContainer = document.getElementById("asset-name-container");
    let assetNamesString = nameContainer.getAttribute("data");
    let assetNames = JSON.parse(assetNamesString.replace(/'/g, '"'));

    let valueContainer = document.getElementById("asset-value-container");
    let assetValuesString = valueContainer.getAttribute("data");
    let assetValues = JSON.parse(assetValuesString.replace(/'/g, '"'));

    // Creates chart with database values
    var assetCtx = document.getElementById("asset-chart").getContext("2d");
    new Chart(assetCtx, {
        type: "doughnut",
        data: {
            labels: assetNames,
            datasets: [{
                data: assetValues,
                borderColor: "#edf0f2",
                backgroundColor: [ "#b4b5c6", "#4f4480", "#2d2354"],
                borderWidth: 5,
            }]
        },
        options: {
            display: false,
        }
    });
});
