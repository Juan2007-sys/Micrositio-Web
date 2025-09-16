const API_URL = 'http://127.0.0.1:8000/ubicaciones';
const map = L.map('map').setView([0, 0], 2);

// Capa base (OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Obtener lugares desde la API
async function cargarPuntos() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error("Error al cargar datos");
        const puntos = await response.json();

        if (!Array.isArray(puntos.data) || puntos.data.length === 0) {
            alert("⚠️ No se encontraron lugares en la API");
            return;
        }

        // Centrar en el primer lugar
        map.setView([puntos.data[0].latitud, puntos.data[0].longitud], 3);

        // Selector
        const selector = document.getElementById('selector');
        selector.innerHTML = "";

        puntos.data.forEach((p, i) => {
            // Agregar opción al selector
            const option = document.createElement('option');
            option.value = i;
            option.textContent = p.nombre;
            selector.appendChild(option);

            // Agregar marcador
            const marker = L.marker([p.latitud, p.longitud]).addTo(map).bindPopup(`<b>${p.nombre}</b><br>${p.descripcion || ""}`);

            marker.on('click', function () {
                map.flyTo([p.latitud, p.longitud], 13, { duration: 2 });
                marker.openPopup();
            });
        });

        // Cambiar vista al seleccionar
        selector.addEventListener('change', function () {
            const idx = this.value;
            map.flyTo([
                puntos.data[idx].latitud,
                puntos.data[idx].longitud
            ], 13, { duration: 2 });
        });

    } catch (error) {
        console.error("❌ Error:", error);
    }
}

// Ejecutar carga
cargarPuntos();