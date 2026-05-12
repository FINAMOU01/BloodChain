document.addEventListener('DOMContentLoaded', function () {
  const map = L.map('blood-map').setView([3.8480, 11.5021], 13);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 18,
  }).addTo(map);

  function getColor(units) {
    if (units > 10) return '#16A34A';
    if (units >= 5) return '#EA580C';
    return '#C0392B';
  }

  function getStatus(units) {
    if (units > 10) return 'Available';
    if (units >= 5) return 'Low';
    return 'Critical';
  }

  const hospitals = [
    {
      name: 'Hôpital Central',
      bloodType: 'O+',
      units: 12,
      address: 'Rue de l\'Hôpital, Yaoundé',
      lat: 3.8667,
      lng: 11.5167
    },
    {
      name: 'Clinique de l\'Espoir',
      bloodType: 'A-',
      units: 4,
      address: 'Avenue Kennedy, Yaoundé',
      lat: 3.8500,
      lng: 11.5000
    },
    {
      name: 'CHU de Yaoundé',
      bloodType: 'B+',
      units: 20,
      address: 'Quartier Bastos, Yaoundé',
      lat: 3.8610,
      lng: 11.5050
    },
    {
      name: 'Hôpital Militaire',
      bloodType: 'AB+',
      units: 7,
      address: 'Camp Yaoundé, Yaoundé',
      lat: 3.8400,
      lng: 11.5200
    },
    {
      name: 'Centre de Transfusion Sanguine',
      bloodType: 'O-',
      units: 2,
      address: 'Boulevard du 20 Mai, Yaoundé',
      lat: 3.8550,
      lng: 11.4900
    }
  ];

  hospitals.forEach(function (h) {
    const color = getColor(h.units);
    const status = getStatus(h.units);

    const marker = L.circleMarker([h.lat, h.lng], {
      radius: 16,
      fillColor: color,
      color: '#FFFFFF',
      weight: 2.5,
      opacity: 1,
      fillOpacity: 0.92,
    });

    const popupContent = `
      <div style="min-width:200px;font-family:'Segoe UI',sans-serif">
        <h6 style="margin:0 0 8px;color:#1a1a2e;font-size:14px;
                   font-weight:700">${h.name}</h6>
        <p style="margin:3px 0;font-size:13px;color:#374151">
          📍 ${h.address}
        </p>
        <p style="margin:3px 0;font-size:13px;color:#374151">
          🩸 Blood type: <strong>${h.bloodType}</strong>
        </p>
        <p style="margin:3px 0;font-size:13px;color:#374151">
          📦 Units available: <strong>${h.units}</strong>
        </p>
        <p style="margin:6px 0 10px;font-size:12px">
          <span style="background:${color};color:#fff;
                       padding:2px 10px;border-radius:20px;
                       font-size:11px;font-weight:600">
            ${status}
          </span>
        </p>
        <button onclick="alert('Request sent to ${h.name}')"
                style="width:100%;background:#C0392B;color:#fff;
                       border:none;padding:8px;border-radius:6px;
                       font-size:13px;font-weight:600;cursor:pointer">
          🩸 Request Blood
        </button>
      </div>
    `;

    marker.bindPopup(popupContent, { maxWidth: 240 });
    marker.addTo(map);
  });

  const legend = L.control({ position: 'bottomright' });

  legend.onAdd = function () {
    const div = L.DomUtil.create('div', 'map-legend');
    div.innerHTML = `
      <div class="legend-title">Blood Availability</div>
      <div class="legend-item">
        <span class="legend-dot" style="background:#16A34A"></span>
        Available (&gt; 10 units)
      </div>
      <div class="legend-item">
        <span class="legend-dot" style="background:#EA580C"></span>
        Low (5–10 units)
      </div>
      <div class="legend-item">
        <span class="legend-dot" style="background:#C0392B"></span>
        Critical (&lt; 5 units)
      </div>
    `;
    return div;
  };

  legend.addTo(map);
});
