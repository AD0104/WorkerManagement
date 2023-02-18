document.
    getElementById("nav-burger").
    addEventListener("click", (event) => {
        document.getElementById("nav-burger").classList.toggle("is-active");
        document.getElementsByClassName("navbar-menu")[0].classList.toggle("is-active");
    });
    