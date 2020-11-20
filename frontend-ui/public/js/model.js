const predict = document.querySelector("#predict");
let isLoading = false;
const reset = document.querySelector("#reset");

reset.addEventListener("click", () => {
  document.querySelector("#age").value = "";
  document.querySelector("#gender").value = "";
  document.querySelector("#race").value = "";
  document.querySelector("#mental-illness").value = "";
  document.querySelector("#body-camera").value = "";
  document.querySelector("#manner-of-death").value = "";
  document.querySelector("#arms-categories").value = "";
  document.querySelector("#state").value = "";
  predict.style.width = "70%";
  result.style.width = "0";
  result.innerHTML = "";
});

const result = document.querySelector("#result");

predict.addEventListener("click", (e) => {
  e.preventDefault();
  const progress = document.createElement("div");
  progress.classList.add("progress");
  const indeterminate = document.createElement("div");
  indeterminate.classList.add("indeterminate");
  progress.appendChild(indeterminate);
  result.appendChild(progress);

  predict.style.width = "60%";
  result.style.width = "40%";

  const age = document.querySelector("#age").value;
  const gender = document.querySelector("#gender").value;
  const race = document.querySelector("#race").value;
  const mentalIllness = document.querySelector("#mental-illness").value;
  const bodyCamera = document.querySelector("#body-camera").value;
  const mannerOfDeath = document.querySelector("#manner-of-death").value;
  const armsCategory = document.querySelector("#arms-categories").value;
  const state = document.querySelector("#state").value;

  if (
    !age ||
    !gender ||
    !race ||
    !mentalIllness ||
    !bodyCamera ||
    !mannerOfDeath ||
    !armsCategory ||
    !state
  ) {
    alert("All fields must have a value");
    predict.style.width = "70%";
    result.style.width = "0";
    result.innerHTML = "";
  } else {
    const data = {
      instances: [
        [
          parseInt(age),
          race,
          state,
          armsCategory,
          gender,
          mentalIllness,
          mannerOfDeath,
          bodyCamera,
        ],
      ],
    };

    fetch(
      "https://us-central1-police-shootings-295915.cloudfunctions.net/lrc-classifier",
      {
        method: "POST",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }
    )
      .then((response) => response.json())
      .then((data) => {
        progress.classList.remove("progress");
        // result.innerHTML = ''
        let resultText = `
        <div>
          <h1>The shooting was <span class="blue">${data.predictions[0]}</span> according to the model</h1>
          <canvas id="chart" width="400" height="400"></canvas>
        </div>`;

        let resultNode = document.createElement("div");
        resultNode.style.paddingLeft = "20px";
        resultNode.innerHTML = resultText;
        result.innerHTML = "";
        result.appendChild(resultNode);
        // result.replaceChild()

        const context = document.querySelector("#chart").getContext("2d");
        const resultChart = new Chart(context, {
          type: "bar",
          data: {
            labels: ["Justified", "Unjustified"],
            datasets: [
              {
                data: data.probabilities[0],
                backgroundColor: [
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(255, 99, 132, 0.2)",
                ],
                borderColor: [ "rgba(54, 162, 235, 1)", "rgba(255, 99, 132, 1)",],
                borderWidth: 1,
                barThickness: 50,
              },
            ],
          },
          options: {
            legend: {
              display: false
            },
            scales: {
              yAxes: [
                {
                  ticks: {
                    beginAtZero: true,
                    min: 0.0,
                    max: 1.0,
                  },
                },
              ],
              xAxes: [
                {
                  type: "category",
                  labels: ["Justified", "Unjustified"]
                },
              ],
            },
          },
        });
      })
      .catch((error) => {
        progress.classList.remove("progress");
        console.log(error);
      });
  }
});
