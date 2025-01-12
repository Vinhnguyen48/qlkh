document.addEventListener("DOMContentLoaded", () => {
  const huy_bt = document.getElementById("bt_huy");
  const add_bt = document.getElementById("add_tk");
  const bt_capnhat = document.getElementById("bt_capnhat");
  const form_tt = document.querySelector(".update_add");

  huy_bt.addEventListener("click", () => {
    form_tt.classList.remove("active");
  });
  add_bt.addEventListener("click", () => {
    form_tt.classList.add("active");
    bt_capnhat.style.display = "none";
  });
});
