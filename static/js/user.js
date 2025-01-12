document.addEventListener("DOMContentLoaded", () => {
  const change_pass = document.getElementById("change-password");
  const luu = document.getElementById("button-luu");
  const huy = document.getElementById("button-huy");
  const form_change = document.querySelector(".password-change");

  change_pass.addEventListener("click", () => {
    form_change.classList.add("active");
  });
  huy.addEventListener("click", () => {
    form_change.classList.remove("active");
  });
});
