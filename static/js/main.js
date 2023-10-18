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
