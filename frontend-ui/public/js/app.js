// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDqkab6DCB-OGQjfv72_0PjoLk8f2TGt58",
  authDomain: "police-shootings-a85ea.firebaseapp.com",
  databaseURL: "https://police-shootings-a85ea.firebaseio.com",
  projectId: "police-shootings-a85ea",
  storageBucket: "police-shootings-a85ea.appspot.com",
  messagingSenderId: "16392688147",
  appId: "1:16392688147:web:890f5b7b7410da56ed25e6",
  measurementId: "G-BTTC4TZR3L",
};

firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();
const storageRef = firebase.storage().ref();
db.settings({ timestampsInSnapshots: true });
const members = document.querySelector("#members-card");
db.collection("team-members").onSnapshot((snapshots) => {
  members.innerHTML = "";
  snapshots.docs.forEach((doc) => {
   
    const imageName = doc.data().image_url.split('/')[7].split('?')[0]
    console.log()
    const data = doc.data();
    const cardDiv = document.createElement("div");
    cardDiv.classList.add("card");
    cardDiv.classList.add("sticky-action");
    cardDiv.classList.add("scale-in");
    const memberDetails = `
 
    <div class="card-image waves-effect waves-block waves-light">
      <img class="activator profile-image" id="${imageName}" src="${data.image_url}" id=${imageName} />
    </div>
    <div class="card-content">
    <span class="card-title activator grey-text text-darken-4">${data.first_name} ${data.last_name}<i class="material-icons right"
    >more_vert</i
    ></span
    >
    <p>${data.hamoye_track}</p>
    </div>
    <div class="card-reveal" id=${doc.id}>
    <span class="card-title grey-text text-darken-4" >${data.first_name} ${data.last_name}<i class="material-icons right">close</i></span>
    <br/>
    <p>
      Track: ${data.hamoye_track}
    </p>
    <p>
      Email: ${data.email}
    </p>

    <a class="waves-effect waves-light btn" onclick="deleteCard(this)"><i id=${imageName} class="material-icons left">delete</i>Delete</a>

    </div>
    <div class="card-action">
    <a href=${data.twitter_id ? `https://twitter.com/${data.twitter_id}`: "#"} target="_blank"
    ><i class="fa fa-twitter fa-lg" aria-hidden="true"></i
    ></a>
    <a href=${data.github_id ? `https://github.com/${data.github_id}`: "#"} target="_blank"
    ><i class="fa fa-github fa-lg" aria-hidden="true"></i
    ></a>
    <a href=${data.linkedin_url ? data.linkedin_url: "#"} target="_blank"
    ><i class="fa fa-linkedin fa-lg" aria-hidden="true"></i
    ></a>
    </div>
  
    `;
    // console.log(data);
    cardDiv.innerHTML = memberDetails;
    members.appendChild(cardDiv);
  });
});



const firstName = document.querySelector("#first_name");
const lastName = document.querySelector("#last_name");
const email = document.querySelector("#email");
const githubID = document.querySelector("#github");
const twitterID = document.querySelector("#twitter");
const linkedInURL = document.querySelector("#linkedin");
const track = document.querySelector("#track");
const hamoyeID = document.querySelector("#hamoye");

const allowedExtensions = ["jpg", "png", "jpeg", "jfif", "tiff"];
let file = {};
document.querySelector("#file").addEventListener("change", (e) => {
  file = e.target.files[0];
});

document.querySelector("#close").addEventListener("click", () => {
  const memberForm = document.querySelector("#add-member-form");
  const modal = document.querySelector("#modal-add-member");
  M.Modal.getInstance(modal).close();
  memberForm.reset();
});

const deleteCard = (data) => {
  console.log(data.childNodes[0].id)
  const deleteRef = storageRef.child(data.childNodes[0].id)
  deleteRef.delete()
  const id = data.parentNode.id;
  db.collection("team-members")
    .doc(id)
    .delete()
    .then(() => alert("Delete Successful"));

};

const upload = document.querySelector("#upload");
upload.addEventListener("click", (e) => {
  e.preventDefault();
  const fileExtension = file.name.split(".")[1];
  console.log(file.name);

  if (allowedExtensions.includes(fileExtension)) {
    let storage = storageRef.child(file.name);
    storage.put(file);

    storage.getDownloadURL().then((url) => {
      db.collection("team-members")
        .doc()
        .set({
          first_name: firstName.value,
          last_name: lastName.value,
          email: email.value,
          twitter_id: twitterID.value,
          github_id: githubID.value,
          hamoye_track: track.value,
          hamoye_id: hamoyeID.value,
          linkedin_url: linkedInURL.value,
          image_url: url,
        })
        .then(() => {
          const memberForm = document.querySelector("#add-member-form");
          const modal = document.querySelector("#modal-add-member");
          M.Modal.getInstance(modal).close();
          memberForm.reset();
        })
        .then(alert("Team member successfully added"));
    });
  } else {
    alert("Invalid Image format");
  }
});

document.addEventListener("DOMContentLoaded", function () {
  var modals = document.querySelectorAll(".modal");
  M.Modal.init(modals);

  var items = document.querySelectorAll(".collapsible");
  M.Collapsible.init(items);
});
