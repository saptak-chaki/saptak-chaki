<div align="center">
<svg width="900" height="450" viewBox="0 0 1000 500" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- নিওন গ্লো ইফেক্ট -->
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="roadGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a1a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#000000;stop-opacity:1" />
    </linearGradient>
  </defs>

  <style>
    @keyframes vibration { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-1.5px); } }
    @keyframes wheelRotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    @keyframes headlightFlicker { 0%, 90%, 100% { opacity: 1; } 92%, 96% { opacity: 0.3; } }
    @keyframes backfirePop { 0%, 90% { opacity: 0; transform: scale(0.5); } 93% { opacity: 1; transform: scale(1.5); fill: #ffec00; } 95% { opacity: 0; } }
    @keyframes dashMove { 0% { stroke-dashoffset: 100; } 50% { stroke-dashoffset: 30; } 100% { stroke-dashoffset: 100; } }
    
    .car-body { animation: vibration 0.12s infinite; }
    .wheel { transform-origin: center; animation: wheelRotate 0.5s linear infinite; }
    .light-glow { animation: headlightFlicker 4s infinite; filter: url(#glow); }
    .exhaust-fire { animation: backfirePop 0.8s infinite; filter: url(#glow); }
    .hud-line { stroke-dasharray: 100; animation: dashMove 3s infinite ease-in-out; }
    .text-cyber { font-family: 'Courier New', monospace; fill: #00ffff; filter: url(#glow); }
  </style>

  <!-- ব্যাকগ্রাউন্ড ও রাস্তা -->
  <rect width="1000" height="500" fill="#050505" />
  <rect x="0" y="350" width="1000" height="150" fill="url(#roadGrad)" />
  <line x1="0" y1="420" x2="1000" y2="420" stroke="#333" stroke-width="2" stroke-dasharray="50,20" />

  <!-- AE86 ভেক্টর কার ডিজাইন -->
  <g class="car-body">
    <!-- বডি -->
    <path d="M200 350 L750 350 L730 280 L550 270 L350 270 L220 320 Z" fill="#ffffff" stroke="#000" stroke-width="2" />
    <path d="M220 320 L740 320 L735 350 L210 350 Z" fill="#1a1a1a" /> <!-- ব্ল্যাক স্ট্রাইপ -->
    
    <!-- জানলা -->
    <path d="M370 280 L540 280 L530 310 L360 310 Z" fill="#003344" opacity="0.7" />
    <path d="M560 280 L680 280 L690 310 L555 310 Z" fill="#003344" opacity="0.7" />

    <!-- হেডলাইট (Flickering) -->
    <rect x="710" y="325" width="30" height="15" fill="#00ffff" class="light-glow" />
    
    <!-- চাকা -->
    <g class="wheel" style="transform: translate(300px, 350px);">
      <circle r="35" fill="#111" stroke="#555" stroke-width="5" />
      <line x1="-25" y1="0" x2="25" y2="0" stroke="#444" stroke-width="3" />
      <line x1="0" y1="-25" x2="0" y2="25" stroke="#444" stroke-width="3" />
    </g>
    <g class="wheel" style="transform: translate(620px, 350px);">
      <circle r="35" fill="#111" stroke="#555" stroke-width="5" />
      <line x1="-25" y1="0" x2="25" y2="0" stroke="#444" stroke-width="3" />
      <line x1="0" y1="-25" x2="0" y2="25" stroke="#444" stroke-width="3" />
    </g>

    <!-- এক্সজস্ট ও ব্যাকফায়ার -->
    <rect x="180" y="340" width="25" height="10" fill="#333" />
    <circle cx="170" cy="345" r="12" fill="#ff4400" class="exhaust-fire" />
  </g>

  <!-- সাইবারপাঙ্ক HUD ইন্টারফেস -->
  <g transform="translate(0, 380)">
    <rect x="0" y="0" width="1000" height="120" fill="rgba(0,20,30,0.95)" stroke="#00ffff" stroke-width="2" />
    
    <!-- স্পিডোমিটার গ্যালারি -->
    <circle cx="120" cy="60" r="45" fill="none" stroke="#1a3333" stroke-width="8" />
    <path d="M85 85 A 45 45 0 1 1 155 85" fill="none" stroke="#00ffff" stroke-width="5" stroke-linecap="round" class="hud-line" />
    <text x="95" y="65" class="text-cyber" font-size="14">RPM: 8.5K</text>

    <!-- ইউজার ইনফো -->
    <text x="220" y="45" class="text-cyber" font-size="24" font-weight="bold">SAPTAK.exe // DRIVER_ID: 001</text>
    <text x="220" y="75" class="text-cyber" font-size="14" opacity="0.8">B.TECH CSE • IoT • CYBER SECURITY • BLOCKCHAIN</text>
    <rect x="220" y="90" width="400" height="4" fill="#1a3333" />
    <rect x="220" y="90" width="320" height="4" fill="#00ffff" class="hud-line" />

    <!-- সিস্টেম স্ট্যাটাস -->
    <text x="750" y="45" class="text-cyber" font-size="14">SYSTEM STATUS: OPTIMAL</text>
    <text x="750" y="70" class="text-cyber" font-size="14">ENGINE: TRUENO-4AGE</text>
    <text x="750" y="95" class="text-cyber" font-size="14">LOCATION: TOKYO-SHIBUYA</text>
  </g>

  <!-- স্ক্যানলাইন ইফেক্ট -->
  <rect width="1000" height="500" fill="none" stroke="rgba(0,255,255,0.05)" stroke-width="1" pointer-events="none" />
</svg>
</div>
