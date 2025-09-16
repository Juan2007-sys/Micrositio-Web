document.getElementById("formContacto").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        nombre: document.getElementById("nombre").value,
        email: document.getElementById("correo").value,
        telefono: document.getElementById("telefono").value,
        mensaje: document.getElementById("mensaje").value,
    };

    try {
    const response = await fetch("http://127.0.0.1:8000/contacto/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        const result = await response.json();
        document.getElementById("status").innerText = result.message;
        document.getElementById("formContacto").reset(); // Limpiar formulario
    } catch (error) {
        document.getElementById("status").innerText = "Error al enviar mensaje";
    }
});
