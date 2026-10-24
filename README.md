<svg xmlns="http://www.w3.org/2000/svg" width="920" height="300" viewBox="0 0 920 300">
  <defs>
    <linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3a3a3a"/>
      <stop offset="45%" stop-color="#141414"/>
      <stop offset="100%" stop-color="#050505"/>
    </linearGradient>
    <linearGradient id="neon" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ff2e63"/>
      <stop offset="50%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#00e5ff"/>
    </linearGradient>
    <filter id="glow" x="-4%" y="-8%" width="108%" height="116%">
      <feGaussianBlur stdDeviation="2.2" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="920" height="300" rx="22" fill="#070707"/>
  <rect x="8" y="8" width="904" height="284" rx="18" fill="url(#metal)" stroke="#2a2a2a" stroke-width="2"/>
  <rect x="16" y="16" width="888" height="268" rx="14" fill="#0c0c0c"/>
  <rect x="16" y="16" width="888" height="268" rx="14" fill="none" stroke="#222" stroke-width="8"/>
  <rect x="16" y="16" width="888" height="268" rx="14" fill="none" stroke="url(#neon)" stroke-width="3" stroke-dasharray="90 220" stroke-linecap="round" filter="url(#glow)">
    <animate attributeName="stroke-dashoffset" from="0" to="-620" dur="2.8s" repeatCount="indefinite"/>
  </rect>

  <circle cx="32" cy="32" r="4" fill="#777"/>
  <circle cx="888" cy="32" r="4" fill="#777"/>
  <circle cx="32" cy="268" r="4" fill="#777"/>
  <circle cx="888" cy="268" r="4" fill="#777"/>

  <text x="460" y="58" text-anchor="middle" fill="#00e5ff" font-size="13" font-family="monospace">ABOUT ME</text>
  <text x="460" y="96" text-anchor="middle" fill="#ffffff" font-size="28" font-family="monospace" font-weight="bold">SAPTAK CHAKI</text>
  <text x="460" y="124" text-anchor="middle" fill="#ff2e63" font-size="15" font-family="monospace">Aspiring Python Full Stack Developer</text>

  <text x="460" y="164" text-anchor="middle" fill="#d5d5d5" font-size="14" font-family="monospace">I build the backend, the interface, and the small details in between.</text>
  <text x="460" y="186" text-anchor="middle" fill="#d5d5d5" font-size="14" font-family="monospace">Focused on Python, HTML, and CSS — learning in public, one commit at a time.</text>
  <text x="460" y="208" text-anchor="middle" fill="#d5d5d5" font-size="14" font-family="monospace">This profile is my garage: streak, commits, and the stack I am shipping.</text>

  <text x="180" y="250" text-anchor="middle" fill="#ff2e63" font-size="12" font-family="monospace" font-weight="bold">FOCUS</text>
  <text x="180" y="270" text-anchor="middle" fill="#ffffff" font-size="12" font-family="monospace">Python Full Stack</text>
  <text x="460" y="250" text-anchor="middle" fill="#ffd54f" font-size="12" font-family="monospace" font-weight="bold">NOW</text>
  <text x="460" y="270" text-anchor="middle" fill="#ffffff" font-size="12" font-family="monospace">Python · HTML · CSS</text>
  <text x="740" y="250" text-anchor="middle" fill="#00e5ff" font-size="12" font-family="monospace" font-weight="bold">GOAL</text>
  <text x="740" y="270" text-anchor="middle" fill="#ffffff" font-size="12" font-family="monospace">Build · Learn · Ship</text>
</svg>
