function cs(field) {
  const tt = document.getElementById(`${field}-display`); 
  const input_cs = document.getElementById(field); 
  const bt_cs = document.getElementById(`${field}_btn`); 
  const btn_cs = document.querySelector(`#${field} + button`); 

  tt.style.display = 'none';
  
  input_cs.style.display = "block";
  bt_cs.style.display = "block";
  
  btn_cs.style.display = "none";
}


function huy(field) {
  const tt = document.getElementById(`${field}-display`); 
  const ip_cs = document.getElementById(field); 
  const bt_cs = document.getElementById(`${field}_btn`); 
  const btn_cs = document.querySelector(`#${field} + button`); 

  tt.style.display = 'block';

  ip_cs.style.display = "none";
  bt_cs.style.display = "none";
  btn_cs.style.display = "inline-block";
}

function closeChatbox() {
  document.getElementById("chatbox").style.display = "none";
}

function openChatbox() {
  document.getElementById("chatbox").style.display = "flex";
}