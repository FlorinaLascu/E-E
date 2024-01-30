var casuta = document.getElementsByClassName("casuta2")
function predictSalary() {
    var profession = document.getElementById("profession").value;
    var language = document.getElementById("language").value;
    var technology = document.getElementById("technology").value;
    var framework = document.getElementById("framework").value;
    var seniority = document.getElementById("seniority").value;
   

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/predict", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                displayPredictedSalary(profession, seniority, language, framework, technology, response.salary);
            } else {
                console.error("Failed to get a response from the server");
            }
        }
    };
    var data = JSON.stringify({
        "profession": profession,
        "language": language,
        "technology": technology,
        "framework": framework,
        "seniority": seniority
    });
    xhr.send(data);
    console.log("Debugging: ", profession, language, technology, framework, seniority);
}

function displayPredictedSalary(profession, seniority, language, framework, technology, salary) {
    // Update the HTML element with the predicted salary
    var resultElement = document.getElementById("result");
    // Desenați graficul folosind Chart.js
    drawChart(profession, seniority, language, framework, technology, salary);

    // Check if the element exists
    if (resultElement) {
        resultElement.innerHTML = "Predicted Salary for " + profession + " with " + seniority + " years of experience: " + salary;
    } else {
        console.error("Result element not found");
    }
}

function drawChart(profession, seniority, language, framework, technology, salary) {
    var canvas = document.getElementById("salaryChart");

    if (canvas) {
        for (var i = 0; i < casuta.length; i++) {
            casuta[i].style.display = "none";
        }
        var ctx = canvas.getContext("2d");

        var chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ["Profession", "Seniority", "Language", "Framework", "Technology"],
                datasets: [{
                    data: [0.4*seniority, seniority, 0.3*seniority, 0.2*seniority, 0.1*seniority],  // Modificați valorile pentru a se potrivi nevoilor dvs.
                    backgroundColor: ['rgba(255, 170, 0, 0.3)', 'rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 205, 86)', 'rgb(75, 192, 192)'],
                    borderColor: 'rgba(255, 170, 0, 0.7)',
                    borderWidth: 3,
                    hoverOffset: 4
                }]
            },
            options: {
                // Opțiuni specifice pentru diagrama circulară
            }
        });
    } else {
        console.error("Canvas element not found");
    }
}
