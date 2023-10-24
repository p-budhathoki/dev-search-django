// console.log("infinity and beyond");
let loginBtn = document.getElementById("login-btn");
let logoutBtn = document.getElementById("logout-btn");

let token = localStorage.getItem("token");

if (token) {
  loginBtn.remove();
} else {
  logoutBtn.remove();
}

logoutBtn.addEventListener("click", (e) => {
  e.preventDefault();
  localStorage.removeItem("token");
  window.location = "file:///C:Users/alysi/Desktop/frontend/login.html";
});

let projectsUrl = "http://127.0.0.1:8000/api/projects/";
let getProjects = () => {
  fetch(projectsUrl)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      buildProjects(data);
    });
};

let buildProjects = (projects) => {
  let projectsWrapper = document.getElementById("projects--wrapper");
  console.log(projectsWrapper);
  projectsWrapper.innerHTML = "";

  for (let i = 0; projects.length > i; i++) {
    let project = projects[i];
    console.log(project);

    // <p>${project.title}</p>
    let projectCard = `
    <div class="project--card">
        <img src="http://127.0.0.1:8000${project.featured_image}" alt="" />;
        <div>
            <div className="card--header">
                <h3>${project.title}</h3>
                <strong class="vote--option" data-vote="up" data-project="${
                  project.id
                }">&#43;</strong>
                <strong class="vote--option" data-vote="down" data-project="${
                  project.id
                }">&#8722;</strong>
            </div>
            <i>${project.vote_ratio}% Positive Feedback</i>;
            <p>${project.description.substring(0, 150)}</p>;
            </div>
            </div>
            `;
    projectsWrapper.innerHTML += projectCard;
  }
  addVoteEvents();
};

// add an event listener
let addVoteEvents = () => {
  let voteBtns = document.getElementsByClassName("vote--option");
  console.log("Vote Buttons : ", voteBtns);

  for (let i = 0; voteBtns.length > i; i++) {
    voteBtns[i].addEventListener("click", (e) => {
      console.log("Vote was clicked : ", i);
      let token = localStorage.getItem("token");
      let vote = e.target.dataset.vote;
      let project = e.target.dataset.project;
      console.log("Project : ", project, "Vote : ", vote);
      console.log("Token : ", token);

      fetch(`http://127.0.0.1:5500/api/projects/${project}/vote/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        Authorization: "Bearer ${token}",
        body: JSON.stringify({ value: vote }),
      })
        .then((response) => {
          response.json();
        })
        .then((data) => {
          console.log("Success : ", data);
          getProjects();
        });
    });
  }
};
getProjects();
