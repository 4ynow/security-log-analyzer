const app = document.getElementById("app");
const allSidebarItems = document.querySelectorAll(".sidebar-item");
const homeBtn = document.getElementById("nav-home");

function setActiveItem(selectedItem) {
    allSidebarItems.forEach((item) => {
        item.classList.remove("active");
    });
    if(selectedItem) {
        selectedItem.classList.add("active");
    }
}

async function loadHomeView() {
    const response = await fetch("home/home.html");
    if (!response.ok) {
        app.textContent = "Failed to load home view.";
        return;
    }
    app.innerHTML = await response.text();
    setActiveItem(homeBtn);

    if (typeof initHome === "function") {
        initHome();
    }
}
allSidebarItems.forEach((item) => {
  item.addEventListener("click", () => {
    setActiveItem(item);
  });
});

homeBtn.addEventListener("click", () => {
  loadHomeView();
});

loadHomeView()
