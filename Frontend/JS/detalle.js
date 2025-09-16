// Leer ID desde la URL (ej: detalle.html?id=2)
const params = new URLSearchParams(window.location.search);
const id = params.get("id");

if (id) {
  fetch(`http://127.0.0.1:8000/proyectos/${id}`)
    .then(res => res.json())
    .then(p => {
      document.getElementById("detalle").innerHTML = `
        <h1>${p.nombre}</h1>
        <img src="${p.imagen || 'https://via.placeholder.com/400x200'}" alt="${p.nombre}" width="400">
        <p>${p.descripcion}</p>

        ${p.url ? `
          <a href="${p.url}" target="_blank" class="btn-github">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" alt="GitHub">
            Ver en GitHub
          </a>
        ` : ''}

        ${p.video ? `
          <div class="video-container">
            <iframe width="560" height="315" src="${p.video}" frameborder="0" allowfullscreen></iframe>
          </div>
        ` : ''}

        <br>
        <a href="index.html" class="btn">⬅️ Volver al listado</a>
      `;
    })
    .catch(err => {
      console.error("Error al obtener el proyecto:", err);
      document.getElementById("detalle").innerHTML = "<p>Error al cargar el proyecto.</p>";
    });
} else {
  document.getElementById("detalle").innerHTML = "<p>No se especificó un proyecto.</p>";
}
