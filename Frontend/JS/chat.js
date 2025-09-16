const form = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");
const toggleBtn = document.getElementById("toggle-chat");
const chatLateral = document.getElementById("chat-lateral");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const tipo = document.getElementById("tipo").value;
  const input = document.getElementById("input-chat").value;

  let url = "";
  let body = null;
  let userLabel = "Yo";
  let iaLabel = "IA";

  if (tipo === "significado") {
    url = "http://127.0.0.1:8000/significado-nombre";
    body = new URLSearchParams({ nombre: input });
    iaLabel = "Significado";
  } else if (tipo === "sentimiento") {
    url = "http://127.0.0.1:8000/analizar-sentimiento";
    body = new URLSearchParams({ mensaje: input });
    iaLabel = "Sentimiento";
  } else {
    url = "http://127.0.0.1:8000/chat-simple";
    body = new URLSearchParams({ mensaje: input });
    iaLabel = "IA";
  }

  chatBox.innerHTML += `<p><strong>${userLabel}:</strong> ${input}</p>`;
  form.reset();

  try {
    const res = await fetch(url, {
      method: "POST",
      body: body,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      }
    });
    const data = await res.json();

    if (tipo === "significado" && data.significado) {
      chatBox.innerHTML += `<p><strong>${iaLabel}:</strong> ${data.significado}</p>`;
    } else if (tipo === "sentimiento" && data.sentimiento) {
      chatBox.innerHTML += `<p><strong>${iaLabel}:</strong> ${data.sentimiento}</p>`;
    } else if (tipo === "general" && data.respuesta) {
      chatBox.innerHTML += `<p><strong>${iaLabel}:</strong> ${data.respuesta}</p>`;
    } else if (data.error) {
      chatBox.innerHTML += `<p style="color:red;"><strong>Error:</strong> ${data.error}</p>`;
    } else {
      chatBox.innerHTML += `<p style="color:red;"><strong>Error:</strong> Respuesta inesperada del servidor</p>`;
    }
    chatBox.scrollTop = chatBox.scrollHeight;
  } catch (err) {
    chatBox.innerHTML += `<p style="color:red;">Error de conexión con el servidor</p>`;
  }
});

if (toggleBtn && chatLateral) {
  toggleBtn.addEventListener("click", () => {
    if (chatLateral.style.display === "none") {
      chatLateral.style.display = "flex";
    } else {
      chatLateral.style.display = "none";
    }
  });
}
