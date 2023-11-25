const modal_login = document.querySelector(".modal-login");
const trigger_login1 = document.querySelector(".login-click1");
const trigger_login2 = document.querySelector(".login-click2");
const modal_signup = document.querySelector(".modal-signup");
const trigger_signup = document.querySelector(".signup-click");
const closeButton = document.getElementsByClassName("close-button");

function toggleModal(event) {
    // console.log(modal_login.classList);
    if(event.target === trigger_login1)
    modal_login.classList.toggle("show-modal");

    if(event.target === trigger_login2)
    modal_login.classList.toggle("show-modal");

    if(event.target === trigger_signup)
    modal_signup.classList.toggle("show-modal");
}

function windowOnClick(event) {
    if (event.target === modal_login) {
        modal_login.classList.toggle("show-modal");
        console.log("entered");
    }
    else if(event.target === modal_signup)
    {
        modal_signup.classList.toggle("show-modal");
        console.log("entered");
    }
}



trigger_login1.addEventListener("click", toggleModal);
trigger_login2.addEventListener("click", toggleModal);
trigger_signup.addEventListener("click", toggleModal);
closeButton[0].addEventListener("click", function(){modal_login.classList.toggle("show-modal")});
closeButton[1].addEventListener("click", function(){modal_signup.classList.toggle("show-modal")});
window.addEventListener("click", windowOnClick);