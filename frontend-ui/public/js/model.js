const predict = document.querySelector("#predict");

predict.addEventListener("click", (e) => {
  e.preventDefault();
  console.log("Hello from the console");
  const name = document.querySelector("#name").value;
  const age = document.querySelector("#age").value;
  const gender = document.querySelector("#gender").value;
  const race = document.querySelector("#race").value;
  const mentalIllness = document.querySelector("#mental-illness").value;
  const bodyCamera = document.querySelector("#body-camera").value;
  const mannerOfDeath = document.querySelector("#manner-of-death").value;
  const armsCategory = document.querySelector("#arms-categories").value;
  const state = document.querySelector("#state").value;

  const data = {
    instances: [
      parseInt(age),
      race,
      state,
      armsCategory,
      gender,
      mentalIllness,
      mannerOfDeath,
      bodyCamera,
    ],
  };

  console.log(JSON.stringify(data))

  fetch(
    "https://us-central1-kubeflow-292442.cloudfunctions.net/lrc-classifier",
    {
      method: "POST",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }
  ).then((response) => console.log("Hello World"));
});
