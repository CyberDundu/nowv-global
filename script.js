

// NOWV INTERACTIVE CHINA-NIGERIA TRADE GLOBE
document.addEventListener("DOMContentLoaded", () => {
  const hero = document.querySelector(".hero");
  if (!hero || document.querySelector(".nowv-globe-wrap")) return;

  const wrap = document.createElement("div");
  wrap.className = "nowv-globe-wrap";
  wrap.innerHTML = `
    <svg viewBox="0 0 500 500" width="100%" height="100%" xmlns="http://w3.org">
      <defs>
        <radialGradient id="globeGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#F86800" stop-opacity="0.22"/>
          <stop offset="55%" stop-color="#159b63" stop-opacity="0.10"/>
          <stop offset="100%" stop-color="#090d16" stop-opacity="0"/>
        </radialGradient>
        <linearGradient id="tradeArc" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#159b63"/>
          <stop offset="50%" stop-color="#fbbf24"/>
          <stop offset="100%" stop-color="#F86800"/>
        </linearGradient>
      </defs>

      <!-- Outer Ambient Halo -->
      <circle cx="250" cy="250" r="235" fill="url(#globeGlow)"/>

      <!-- Main Wireframe Sphere -->
      <g stroke="rgba(255,255,255,0.13)" stroke-width="1.1" fill="none">
        <circle cx="250" cy="250" r="185" stroke="rgba(248,104,0,0.32)" stroke-width="1.5"/>
        <!-- Latitude Rings -->
        <ellipse cx="250" cy="250" rx="185" ry="52"/>
        <ellipse cx="250" cy="250" rx="185" ry="118"/>
        <ellipse cx="250" cy="185" rx="162" ry="38"/>
        <ellipse cx="250" cy="315" rx="162" ry="38"/>
        <!-- Longitude Meridians -->
        <ellipse cx="250" cy="250" rx="52" ry="185"/>
        <ellipse cx="250" cy="250" rx="118" ry="185"/>
        <ellipse cx="250" cy="250" rx="158" ry="185" transform="rotate(-22 250 250)"/>
        <ellipse cx="250" cy="250" rx="158" ry="185" transform="rotate(22 250 250)"/>
      </g>

      <!-- Glowing Orbit Ring -->
      <ellipse cx="250" cy="250" rx="222" ry="74" fill="none" stroke="rgba(248,104,0,0.28)" stroke-width="1.2" stroke-dasharray="6 6" transform="rotate(-18 250 250)"/>

      <!-- Trade Corridor Arc: Nigeria (Left-Bottom) to China (Right-Top) -->
      <path d="M 185 278 Q 255 135 342 196" fill="none" stroke="url(#tradeArc)" stroke-width="3" stroke-linecap="round"/>
      <path d="M 185 278 Q 255 135 342 196" fill="none" stroke="#ffffff" stroke-width="2" stroke-dasharray="8 12" stroke-linecap="round">
        <animate attributeName="stroke-dashoffset" from="40" to="0" dur="1.8s" repeatCount="indefinite"/>
      </path>

      <!-- Nigeria Hub Node (Green) -->
      <circle cx="185" cy="278" r="14" fill="rgba(21,155,99,0.25)">
        <animate attributeName="r" values="10;20;10" dur="2.4s" repeatCount="indefinite"/>
      </circle>
      <circle cx="185" cy="278" r="5.5" fill="#159b63" stroke="#ffffff" stroke-width="1.5"/>
      <text x="142" y="304" fill="#6ee7b7" font-size="11" font-weight="700" font-family="sans-serif" letter-spacing="1">NIGERIA</text>

      <!-- China Hub Node (Orange) -->
      <circle cx="342" cy="196" r="14" fill="rgba(248,104,0,0.28)">
        <animate attributeName="r" values="10;20;10" dur="2.4s" repeatCount="indefinite"/>
      </circle>
      <circle cx="342" cy="196" r="5.5" fill="#F86800" stroke="#ffffff" stroke-width="1.5"/>
      <text x="348" y="182" fill="#fdba74" font-size="11" font-weight="700" font-family="sans-serif" letter-spacing="1">CHINA</text>
    </svg>
  `;
  hero.appendChild(wrap);
});
