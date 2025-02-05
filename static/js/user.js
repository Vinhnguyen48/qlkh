function cs(field) {
  const tt = document.getElementById(`${field}-display`);
  const input_cs = document.getElementById(field);
  const bt_cs = document.getElementById(`${field}_btn`);
  const btn_cs = document.querySelector(`#${field} + button`);

  tt.style.display = "none";

  input_cs.style.display = "block";
  bt_cs.style.display = "block";

  btn_cs.style.display = "none";
}

function huy(field) {
  const tt = document.getElementById(`${field}-display`);
  const ip_cs = document.getElementById(field);
  const bt_cs = document.getElementById(`${field}_btn`);
  const btn_cs = document.querySelector(`#${field} + button`);

  tt.style.display = "block";

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
async function fetchMessages() {
  try {
   
    const response = await fetch("/customer/get_messages", { method: "GET" });
    const messages = await response.json();
    const chatboxBody = document.getElementById("chatbox-body");
    const vitri = chatboxBody.scrollTop;
    chatboxBody.innerHTML = ""; 
    messages.forEach((msg) => {
      const messageElement = document.createElement("div");
      messageElement.innerHTML = `<b>${msg.sender}:</b> ${msg.message} <small>(${msg.timestamp})</small>`;
      chatboxBody.appendChild(messageElement);
    });

    
    chatboxBody.scrollTop = vitri; // lưu vi tri khi cuon xem tin nhan
  } catch (error) {
    console.error("Lỗi khi lấy tin nhắn:", error);
  }
}

async function sendMessage(event) {

  event.preventDefault(); // khong cho load trang
  const messageInput = document.getElementById("message-input");
  const message = messageInput.value.trim();
  if (message) {
    try {
      messageInput.value = ""; 
      const response = await fetch("/customer/send_mes", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });
      fetchMessages(); 
    } catch (error) {
      console.error("Lỗi khi gửi tin nhắn:", error);
    }
  }
}

setInterval(fetchMessages, 1000); // goi ham load tin nhan 1s 1 lan de cap nhat lại tin nhăn mới
