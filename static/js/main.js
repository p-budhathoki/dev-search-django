// get search form and page links
let searchForm = document.getElementById("searchForm");
let pageLinks = document.getElementsByClassName("page-links");

// ensure search form exists
if (searchForm) {
  for (let i = 0; pageLinks.length > i; i++) {
    pageLinks[i].addEventListener("click", function (e) {
      e.preventDefault();
      console.log("Button Click");

      // get the data attribute
      let page = this.dataset.page;
      console.log("PAGE : ", page);

      // add hidden search input to form
      searchForm.innerHTML += `<input  name = "page" hidden value = "${page}" />`;

      // submit form
      searchForm.submit();
    });
  }
}

let tags = document.getElementsByClassName("project-tag");

for (let i = 0; tags.length > i; i++) {
  tags[i].addEventListener("click", (e) => {
    let tagId = e.target.dataset.tag;
    let projectId = e.target.dataset.project;
    console.log("Tag Id: ", tagId);
    console.log("Project Id: ", projectId);

    fetch("http://127.0.0.1:8000/api/remove-tag/", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ project: projectId, tag: tag }),
    })
      .then((response) => response.json())
      .then((data) => {
        e.target.remove();
      });
  });
}
