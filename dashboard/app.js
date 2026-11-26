const app = document.getElementById("app");

async function loadHomeView() {
  const response = await fetch("home/home.html");
  if (!response.ok) {
    app.textContent = "Failed to load home view.";
    return;
  }

  app.innerHTML = await response.text();

  if (typeof initHome === "function") {
    initHome();
  }
}

loadHomeView();
