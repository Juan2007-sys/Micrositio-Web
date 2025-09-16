// Cambia la URL si tu backend no corre en localhost
fetch("http://127.0.0.1:8000/proyectos/")
  .then(res => res.json())
  .then(data => {
    const contenedor = document.getElementById("proyectos");
    contenedor.innerHTML = data.data.map(p => `
      <div class="card">
        <img src="${p.imagen || 'https://via.placeholder.com/300x150'}" alt="${p.nombre}">
        <h3>${p.nombre}</h3>
        <p>${p.descripcion ? p.descripcion.substring(0, 100) + "..." : ''}</p>
        <a href="detalle.html?id=${p.id}" class="btn">🔍 Ver Detalle</a>
      </div>
    `).join('');
  })
  .catch(err => console.error("Error al obtener proyectos:", err));
