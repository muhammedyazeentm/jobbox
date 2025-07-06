document.addEventListener("DOMContentLoaded", function () {
    
    const shopSignupButton = document.querySelector(".btn1");
    const workerSignupButton = document.querySelector(".btn2");

    if (shopSignupButton) {
        shopSignupButton.addEventListener("click", function () {
            window.location.href = "shop_individual_signup.html";
        });
    }

    if (workerSignupButton) {
        workerSignupButton.addEventListener("click", function () {
            window.location.href = "worker_signup.html";
        });
    }
});
