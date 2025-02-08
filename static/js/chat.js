// Hàm lấy tin nhắn từ server

//lay nguoi gui tin nhan
let id_ds = [];
function listid() {
  document.querySelectorAll(".chatbox").forEach((chatbox) => {
    let id_kh = chatbox.getAttribute("data-id");
    if (!id_ds.includes(id_kh)) {
      id_ds.push(id_kh); // Thêm ID vào mảng nếu chưa có
    } // Thêm vào mảng
  });
}
async function loadmes(id_kh) {
  try {
    const response = await fetch(`/admin/get_messages/${id_kh}`, {
      method: "GET",
    });
    const messages = await response.json();
    const chatboxBody = document.getElementById(`chatbox-body-${id_kh}`);
    const vitri = chatboxBody.scrollTop;
    chatboxBody.innerHTML = "";
    messages.forEach((msg) => {
      const messageElement = document.createElement("div");
      messageElement.innerHTML = `<b>${msg.sender}:</b> ${msg.message} <small>(${msg.timestamp})</small>`;
      chatboxBody.appendChild(messageElement);
    });
    chatboxBody.scrollTop = vitri;
  } catch (error) {
    console.error("Lỗi khi lấy tin nhắn:", error);
  }
}

async function load_ds_mes() {
  listid();
  for (let id_kh in id_ds) loadmes(id_ds[id_kh]);
}

/* gui tin nhan
async function sendMessage(event, id) {
  event.preventDefault(); // Không cho load trang
  const messageInput = document.getElementById(`message-input-${id}`);
 
  const message = messageInput.value.trim();

  if (message) {
    console.log(message);
    try {
      messageInput.value = "";  // Xóa nội dung input sau khi gửi

      const response = await fetch(`/admin/send_mes/${id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",  // Đảm bảo gửi dưới dạng JSON
        },
        body: JSON.stringify({ message }),  // Gửi dữ liệu dưới dạng JSON
      });

      const data = await response.json();  // Giải mã phản hồi JSON từ server
      console.log("Server response:", data);

      if (data.status !== "success") {
        console.error("Lỗi từ server:", data.message);
      }

      load_ds_mes();  // Tải lại danh sách tin nhắn
    } catch (error) {
      console.error("Lỗi khi gửi tin nhắn:", error);
    }
  }
}

*/
async function sendMessage(event, id) {
  event.preventDefault(); // Không làm mới trang sau khi gửi tin nhắn

  // Lấy nội dung tin nhắn từ input
  const messageInput = document.getElementById(`message-input-${id}`);
  const message = messageInput.value.trim();

  if (message) {
    messageInput.value = "";
    try {
      const response = await fetch(`/admin/send_mes/${id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // Đảm bảo gửi dưới dạng JSON
        },
        body: JSON.stringify({ message }), // Gửi dữ liệu dưới dạng JSON
      });

      // Phản hồi từ server
      const data = await response.json();
      load_ds_mes();
    } catch (error) {
      console.error("Lỗi khi gửi tin nhắn:", error);
    }
  }
}

setInterval(load_ds_mes, 1000); // goi ham load tin nhan 1s 1 lan de cap nhat lại tin nhăn mới

document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("customer-list-icon")
    .addEventListener("click", function () {
      window.location.href = "/admin";
    });
});
