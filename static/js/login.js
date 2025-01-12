document.addEventListener("DOMContentLoaded", () => {
  const login_bt = document.getElementById("login-bt");
  const signup_bt = document.getElementById("sign-bt");
  const exit_bt = document.getElementById("exit-f");
  const exit_bts = document.getElementById("exit_f");
  const login_f = document.querySelector(".login-f");
  const signup_f = document.querySelector(".signup-f");
  const login_signup = document.querySelector(".login-signup");
  const login_link = document.getElementById("login-links");
  const signup_link=document.getElementById("signup-links");

  login_bt.addEventListener("click", () => {
    login_f.classList.add("active");
    login_signup.classList.add("active");
    signup_f.classList.remove("active");
  });

  signup_bt.addEventListener("click", () => {
    signup_f.classList.add("active");
    login_signup.classList.add("active");
    login_f.classList.remove("active");
  });
  exit_bt.addEventListener("click", () => {
    signup_f.classList.remove("active");
    login_f.classList.remove("active");
    login_signup.classList.remove("active");
  });
  exit_bts.addEventListener("click", () => {
    signup_f.classList.remove("active");
    login_f.classList.remove("active");
    login_signup.classList.remove("active");
  });

  login_link.addEventListener("click", (event) => {
    event.preventDefault();
    signup_f.classList.remove("active"); 
    login_f.classList.add("active"); 
    login_signup.classList.add("active"); 
  });
  signup_link.addEventListener("click", (event) => {
    event.preventDefault();
    signup_f.classList.add("active");
    login_signup.classList.add("active");
    login_f.classList.remove("active");
  });

    const alerts = document.querySelectorAll('.alert');


    alerts.forEach((alert) => {
      setTimeout(() => {
        alert.style.opacity = '0'; //giam do mo cua thong bao
        setTimeout(() => alert.remove(), 500); // xoa thong bao
      }, 3000); // 
    });
  
});



