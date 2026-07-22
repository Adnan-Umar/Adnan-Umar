"""
_build_svgs.py  -  Generates dark.svg, light.svg, info-card.svg
with the real photo embedded as base64.
Run from repo root:  python scripts/_build_svgs.py
"""
import pathlib

# ── Load photo base64 URI ─────────────────────────────────────────────────────
B64 = pathlib.Path("scripts/pic-b64.txt").read_text().strip()

# ── Shared palette tokens ─────────────────────────────────────────────────────
DARK = dict(
    bg="#030712", panel="rgba(15,23,42,0.58)", panel2="rgba(15,23,42,0.45)",
    border="rgba(255,255,255,0.07)", text1="#F8FAFC", text2="#94A3B8",
    muted="#64748B", accent1="#7C3AED", accent2="#22D3EE", accent3="#10B981",
    pill1="rgba(34,211,238,0.12)", pill1s="rgba(34,211,238,0.35)",
    pill2="rgba(124,58,237,0.12)", pill2s="rgba(124,58,237,0.35)",
    pill3="rgba(16,185,129,0.12)", pill3s="rgba(16,185,129,0.35)",
    code_bg="rgba(3,7,18,0.7)", code_border="rgba(255,255,255,0.06)",
    lnum="#374151", kw="#7C3AED", ty="#22D3EE", str_="#10B981", sym="#94A3B8",
    ring1="#7C3AED", ring2="#22D3EE",
)
LIGHT = dict(
    bg="#F8FAFC", panel="rgba(248,250,252,0.72)", panel2="rgba(248,250,252,0.55)",
    border="rgba(15,23,42,0.08)", text1="#0F172A", text2="#475569",
    muted="#94A3B8", accent1="#2563EB", accent2="#06B6D4", accent3="#059669",
    pill1="rgba(6,182,212,0.1)", pill1s="rgba(6,182,212,0.3)",
    pill2="rgba(37,99,235,0.1)", pill2s="rgba(37,99,235,0.3)",
    pill3="rgba(16,185,129,0.1)", pill3s="rgba(16,185,129,0.3)",
    code_bg="rgba(241,245,249,0.9)", code_border="rgba(15,23,42,0.08)",
    lnum="#CBD5E1", kw="#7C3AED", ty="#0891B2", str_="#059669", sym="#64748B",
    ring1="#2563EB", ring2="#06B6D4",
)


def defs(t, noise_opacity, scan_opacity):
    """Shared <defs> block for hero SVGs."""
    a1, a2, a3 = t['accent1'], t['accent2'], t['accent3']
    r1, r2 = t['ring1'], t['ring2']
    return f"""  <defs>
    <linearGradient id="accentG" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"   stop-color="{a1}"><animate attributeName="stop-color" values="{a1};{a2};{a3};{a1}" dur="6s" repeatCount="indefinite"/></stop>
      <stop offset="50%"  stop-color="{a2}"><animate attributeName="stop-color" values="{a2};{a3};{a1};{a2}" dur="6s" repeatCount="indefinite"/></stop>
      <stop offset="100%" stop-color="{a3}"><animate attributeName="stop-color" values="{a3};{a1};{a2};{a3}" dur="6s" repeatCount="indefinite"/></stop>
    </linearGradient>
    <linearGradient id="shimmer" x1="-100%" y1="0%" x2="0%" y2="0%">
      <stop offset="0%"   stop-color="rgba(255,255,255,0)"/>
      <stop offset="50%"  stop-color="rgba(255,255,255,0.3)"/>
      <stop offset="100%" stop-color="rgba(255,255,255,0)"/>
      <animate attributeName="x1" values="-100%;100%" dur="2.8s" repeatCount="indefinite"/>
      <animate attributeName="x2" values="0%;200%"    dur="2.8s" repeatCount="indefinite"/>
    </linearGradient>
    <radialGradient id="blob1" cx="22%" cy="25%" r="45%">
      <stop offset="0%" stop-color="{a1}" stop-opacity="0.16"><animate attributeName="stop-opacity" values="0.16;0.05;0.16" dur="7s" repeatCount="indefinite"/></stop>
      <stop offset="100%" stop-color="{a1}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="blob2" cx="80%" cy="75%" r="45%">
      <stop offset="0%" stop-color="{a2}" stop-opacity="0.11"><animate attributeName="stop-opacity" values="0.11;0.03;0.11" dur="9s" repeatCount="indefinite"/></stop>
      <stop offset="100%" stop-color="{a2}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="photoRing" cx="50%" cy="50%" r="50%">
      <stop offset="70%" stop-color="transparent"/>
      <stop offset="85%" stop-color="{r1}" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="{r2}" stop-opacity="0.3"/>
    </radialGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="strongGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="noise" x="0%" y="0%" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.68" numOctaves="3" stitchTiles="stitch" result="n"><animate attributeName="seed" values="0;20;0" dur="12s" repeatCount="indefinite"/></feTurbulence>
      <feColorMatrix type="saturate" values="0" in="n" result="gn"/>
      <feComponentTransfer in="gn" result="dn"><feFuncA type="linear" slope="{noise_opacity}"/></feComponentTransfer>
      <feBlend in="SourceGraphic" in2="dn" mode="overlay"/>
    </filter>
    <mask id="scanMask">
      <rect width="1180" height="610" fill="black"/>
      <rect width="1180" height="3" fill="white" opacity="{scan_opacity}">
        <animate attributeName="y" values="-5;615" dur="3.5s" repeatCount="indefinite"/>
      </rect>
    </mask>
    <clipPath id="leftClip"><rect x="32" y="32" width="460" height="546" rx="14"/></clipPath>
    <clipPath id="rightClip"><rect x="508" y="32" width="640" height="546" rx="14"/></clipPath>
    <clipPath id="photoCircle"><circle cx="192" cy="170" r="110"/></clipPath>
    <linearGradient id="pill1g" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['pill1']}"/><stop offset="100%" stop-color="{t['pill1']}"/>
    </linearGradient>
    <linearGradient id="pill2g" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['pill2']}"/><stop offset="100%" stop-color="{t['pill2']}"/>
    </linearGradient>
    <linearGradient id="pill3g" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['pill3']}"/><stop offset="100%" stop-color="{t['pill3']}"/>
    </linearGradient>
  </defs>"""


def left_panel(t, b64_photo):
    """Left panel: photo + name + identity + skills."""
    a1, a2, a3 = t['accent1'], t['accent2'], t['accent3']
    p2, p2s = t['pill2'], t['pill2s']
    p1, p1s = t['pill1'], t['pill1s']
    p3, p3s = t['pill3'], t['pill3s']
    return f"""
  <!-- ══ LEFT PANEL ══ -->
  <rect x="32" y="32" width="460" height="546" rx="14" fill="{t['panel2']}" stroke="{t['border']}" stroke-width="1"/>

  <!-- Photo ring glow -->
  <circle cx="192" cy="170" r="124" fill="url(#photoRing)">
    <animate attributeName="r" values="124;128;124" dur="4s" repeatCount="indefinite"/>
  </circle>
  <!-- Animated ring border -->
  <circle cx="192" cy="170" r="115" fill="none" stroke="{a2}" stroke-width="2" stroke-dasharray="6 4" opacity="0.5">
    <animateTransform attributeName="transform" type="rotate" from="0 192 170" to="360 192 170" dur="20s" repeatCount="indefinite"/>
  </circle>
  <circle cx="192" cy="170" r="118" fill="none" stroke="{a1}" stroke-width="1" stroke-dasharray="3 8" opacity="0.3">
    <animateTransform attributeName="transform" type="rotate" from="360 192 170" to="0 192 170" dur="15s" repeatCount="indefinite"/>
  </circle>

  <!-- Photo clipped to circle -->
  <image href="{b64_photo}" x="82" y="60" width="220" height="220" clip-path="url(#photoCircle)" preserveAspectRatio="xMidYMid slice"/>

  <!-- Name -->
  <text x="192" y="315" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
    font-size="20" font-weight="700" fill="{t['text1']}" text-anchor="middle"
    filter="url(#strongGlow)" opacity="0">
    Md Adnan Umar
    <animate attributeName="opacity" values="0;1" dur="0.5s" fill="freeze" begin="0.6s"/>
  </text>

  <!-- Role with typing cursor -->
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.3s" fill="freeze" begin="0.9s"/>
    <text x="192" y="337" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
      font-size="13" fill="url(#accentG)" text-anchor="middle">Software Engineer</text>
    <rect x="283" y="325" width="7" height="12" fill="{a2}" rx="1">
      <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- Info lines -->
  <g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11.5">
    <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.3s" fill="freeze" begin="1.1s"/>
      <text x="90" y="362" fill="{t['muted']}">&#9702; location</text>
      <text x="172" y="362" fill="{t['text2']}">India &#127470;&#127475;</text>
    </g>
    <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.3s" fill="freeze" begin="1.3s"/>
      <text x="90" y="380" fill="{t['muted']}">&#9702; education</text>
      <text x="172" y="380" fill="{t['text2']}">B.Tech CSE · Final Year</text>
    </g>
    <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.3s" fill="freeze" begin="1.5s"/>
      <text x="90" y="398" fill="{t['muted']}">&#9702; focus</text>
      <text x="172" y="398" fill="{t['text2']}">Backend · Cloud · AI Eng.</text>
    </g>
    <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.3s" fill="freeze" begin="1.7s"/>
      <text x="90" y="416" fill="{t['muted']}">&#9702; status</text>
      <circle cx="174" cy="412" r="4" fill="{a3}"><animate attributeName="r" values="4;5;4" dur="1.5s" repeatCount="indefinite"/></circle>
      <text x="182" y="416" fill="{a3}">accepting offers</text>
    </g>
  </g>

  <!-- Divider -->
  <line x1="56" y1="432" x2="460" y2="432" stroke="{t['border']}" stroke-width="1" opacity="0">
    <animate attributeName="opacity" values="0;1" dur="0.4s" fill="freeze" begin="1.9s"/>
  </line>

  <!-- Skill pills row 1 -->
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.4s" fill="freeze" begin="2.1s"/>
    <text x="56" y="452" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="10" fill="{t['muted']}">//  stack</text>
    <!-- Java -->
    <rect x="56"  y="460" width="46"  height="22" rx="11" fill="{p1}"  stroke="{p1s}"  stroke-width="1"><animate attributeName="stroke-opacity" values="0.35;0.7;0.35" dur="2.5s" repeatCount="indefinite"/></rect>
    <text x="79"  y="475" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a2}" text-anchor="middle">Java</text>
    <!-- Spring Boot -->
    <rect x="108" y="460" width="94"  height="22" rx="11" fill="{p2}"  stroke="{p2s}"  stroke-width="1"><animate attributeName="stroke-opacity" values="0.35;0.7;0.35" dur="2.5s" repeatCount="indefinite" begin="0.2s"/></rect>
    <text x="155" y="475" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a1}" text-anchor="middle">Spring Boot</text>
    <!-- Kafka -->
    <rect x="208" y="460" width="50"  height="22" rx="11" fill="{p3}"  stroke="{p3s}"  stroke-width="1"><animate attributeName="stroke-opacity" values="0.35;0.7;0.35" dur="2.5s" repeatCount="indefinite" begin="0.4s"/></rect>
    <text x="233" y="475" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a3}" text-anchor="middle">Kafka</text>
    <!-- Docker -->
    <rect x="264" y="460" width="58"  height="22" rx="11" fill="{p1}"  stroke="{p1s}"  stroke-width="1"><animate attributeName="stroke-opacity" values="0.35;0.7;0.35" dur="2.5s" repeatCount="indefinite" begin="0.6s"/></rect>
    <text x="293" y="475" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a2}" text-anchor="middle">Docker</text>
    <!-- K8s -->
    <rect x="328" y="460" width="76"  height="22" rx="11" fill="{p2}"  stroke="{p2s}"  stroke-width="1"><animate attributeName="stroke-opacity" values="0.35;0.7;0.35" dur="2.5s" repeatCount="indefinite" begin="0.8s"/></rect>
    <text x="366" y="475" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a1}" text-anchor="middle">Kubernetes</text>
    <!-- Redis -->
    <rect x="410" y="460" width="50"  height="22" rx="11" fill="{p3}"  stroke="{p3s}"  stroke-width="1"><animate attributeName="stroke-opacity" values="0.35;0.7;0.35" dur="2.5s" repeatCount="indefinite" begin="1.0s"/></rect>
    <text x="435" y="475" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a3}" text-anchor="middle">Redis</text>
  </g>

  <!-- Skill pills row 2 -->
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.4s" fill="freeze" begin="2.4s"/>
    <rect x="56"  y="490" width="80"  height="22" rx="11" fill="{p1}"  stroke="{p1s}"  stroke-width="1"><animate attributeName="stroke-opacity" values="0.35;0.7;0.35" dur="2.5s" repeatCount="indefinite"/></rect>
    <text x="96"  y="505" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a2}" text-anchor="middle">PostgreSQL</text>
    <rect x="142" y="490" width="56"  height="22" rx="11" fill="{p2}"  stroke="{p2s}"  stroke-width="1"><animate attributeName="stroke-opacity" values="0.35;0.7;0.35" dur="2.5s" repeatCount="indefinite" begin="0.2s"/></rect>
    <text x="170" y="505" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a1}" text-anchor="middle">Python</text>
    <rect x="204" y="490" width="50"  height="22" rx="11" fill="{p3}"  stroke="{p3s}"  stroke-width="1"><animate attributeName="stroke-opacity" values="0.35;0.7;0.35" dur="2.5s" repeatCount="indefinite" begin="0.4s"/></rect>
    <text x="229" y="505" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a3}" text-anchor="middle">React</text>
    <rect x="260" y="490" width="86"  height="22" rx="11" fill="{p1}"  stroke="{p1s}"  stroke-width="1"><animate attributeName="stroke-opacity" values="0.35;0.7;0.35" dur="2.5s" repeatCount="indefinite" begin="0.6s"/></rect>
    <text x="303" y="505" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a2}" text-anchor="middle">Spring AI</text>
    <rect x="352" y="490" width="50"  height="22" rx="11" fill="{p2}"  stroke="{p2s}"  stroke-width="1"><animate attributeName="stroke-opacity" values="0.35;0.7;0.35" dur="2.5s" repeatCount="indefinite" begin="0.8s"/></rect>
    <text x="377" y="505" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a1}" text-anchor="middle">AWS</text>
    <rect x="408" y="490" width="52"  height="22" rx="11" fill="{p3}"  stroke="{p3s}"  stroke-width="1"><animate attributeName="stroke-opacity" values="0.35;0.7;0.35" dur="2.5s" repeatCount="indefinite" begin="1.0s"/></rect>
    <text x="434" y="505" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a3}" text-anchor="middle">CI/CD</text>
  </g>

  <!-- Social pills -->
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.4s" fill="freeze" begin="2.7s"/>
    <rect x="56"  y="523" width="68" height="24" rx="12" fill="{t['panel2']}" stroke="{t['border']}" stroke-width="1"><animate attributeName="stroke-opacity" values="0.07;0.2;0.07" dur="2s" repeatCount="indefinite"/></rect>
    <text x="90"  y="539" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9.5" fill="{t['text2']}" text-anchor="middle">&#127758; Portfolio</text>
    <rect x="132" y="523" width="60" height="24" rx="12" fill="{t['panel2']}" stroke="{t['border']}" stroke-width="1"><animate attributeName="stroke-opacity" values="0.07;0.2;0.07" dur="2s" repeatCount="indefinite" begin="0.3s"/></rect>
    <text x="162" y="539" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9.5" fill="{t['text2']}" text-anchor="middle">&#128188; LinkedIn</text>
    <rect x="200" y="523" width="52" height="24" rx="12" fill="{t['panel2']}" stroke="{t['border']}" stroke-width="1"><animate attributeName="stroke-opacity" values="0.07;0.2;0.07" dur="2s" repeatCount="indefinite" begin="0.6s"/></rect>
    <text x="226" y="539" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9.5" fill="{t['text2']}" text-anchor="middle">&#128231; Email</text>
    <rect x="260" y="523" width="56" height="24" rx="12" fill="{t['panel2']}" stroke="{t['border']}" stroke-width="1"><animate attributeName="stroke-opacity" values="0.07;0.2;0.07" dur="2s" repeatCount="indefinite" begin="0.9s"/></rect>
    <text x="288" y="539" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9.5" fill="{t['text2']}" text-anchor="middle">&#128121; GitHub</text>
  </g>"""


def right_panel(t):
    """Right panel: terminal window with code block + metric cards + what I build."""
    a1, a2, a3 = t['accent1'], t['accent2'], t['accent3']
    kw, ty, st, sy = t['kw'], t['ty'], t['str_'], t['sym']
    ln = t['lnum']
    cb, cbrd = t['code_bg'], t['code_border']
    p2, p2s = t['pill2'], t['pill2s']
    p1, p1s = t['pill1'], t['pill1s']
    p3, p3s = t['pill3'], t['pill3s']
    return f"""
  <!-- ══ RIGHT PANEL ══ -->
  <rect x="508" y="32" width="640" height="546" rx="14" fill="{t['panel']}" stroke="{t['border']}" stroke-width="1"/>

  <!-- Terminal title bar -->
  <rect x="508" y="32" width="640" height="40" rx="12" fill="{t['panel2']}"/>
  <rect x="508" y="60" width="640" height="12" fill="{t['panel2']}" opacity="0.6"/>
  <!-- Traffic lights -->
  <circle cx="533" cy="52" r="6" fill="#FF5F57"><animate attributeName="r" values="6;6.8;6" dur="2.5s" repeatCount="indefinite"/></circle>
  <circle cx="553" cy="52" r="6" fill="#FEBC2E"><animate attributeName="r" values="6;6.8;6" dur="2.5s" repeatCount="indefinite" begin="0.25s"/></circle>
  <circle cx="573" cy="52" r="6" fill="#28C840"><animate attributeName="r" values="6;6.8;6" dur="2.5s" repeatCount="indefinite" begin="0.5s"/></circle>
  <!-- Title -->
  <text x="828" y="56" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
    font-size="11" fill="{t['muted']}" text-anchor="middle">adnan@backend:~$ cat about.java</text>

  <!-- Greeting -->
  <text x="528" y="100" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
    font-size="13" fill="{t['muted']}">&#10095;  Hi there, I build systems that scale.</text>

  <!-- Big name -->
  <text x="528" y="134" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
    font-size="28" font-weight="800" fill="{t['text1']}" filter="url(#strongGlow)"
    opacity="0">
    Md Adnan Umar
    <animate attributeName="opacity" values="0;1" dur="0.5s" fill="freeze" begin="0.5s"/>
  </text>

  <!-- Role line -->
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.3s" fill="freeze" begin="0.8s"/>
    <text x="528" y="160" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
      font-size="14" fill="url(#accentG)">Software Engineer · Java · Spring Boot · Cloud</text>
    <rect x="528" y="164" width="8" height="13" fill="{a2}" rx="1" opacity="0">
      <animate attributeName="opacity" values="0;0;1;1;0" dur="1s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- 4 metric stat cards -->
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.4s" fill="freeze" begin="1.1s"/>
    <rect x="528" y="175" width="136" height="40" rx="8" fill="{p1}" stroke="{p1s}" stroke-width="1"/>
    <text x="596" y="190" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9.5" fill="{t['muted']}" text-anchor="middle">Specialization</text>
    <text x="596" y="207" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11.5" font-weight="700" fill="{a2}" text-anchor="middle">Microservices</text>

    <rect x="672" y="175" width="136" height="40" rx="8" fill="{p2}" stroke="{p2s}" stroke-width="1"/>
    <text x="740" y="190" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9.5" fill="{t['muted']}" text-anchor="middle">Platform</text>
    <text x="740" y="207" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11.5" font-weight="700" fill="{a1}" text-anchor="middle">Kubernetes</text>

    <rect x="816" y="175" width="136" height="40" rx="8" fill="{p3}" stroke="{p3s}" stroke-width="1"/>
    <text x="884" y="190" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9.5" fill="{t['muted']}" text-anchor="middle">AI Layer</text>
    <text x="884" y="207" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11.5" font-weight="700" fill="{a3}" text-anchor="middle">Spring AI</text>

    <rect x="960" y="175" width="168" height="40" rx="8" fill="{p1}" stroke="{p1s}" stroke-width="1"/>
    <text x="1044" y="190" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9.5" fill="{t['muted']}" text-anchor="middle">Architecture</text>
    <text x="1044" y="207" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11.5" font-weight="700" fill="{a2}" text-anchor="middle">System Design</text>
  </g>

  <!-- Divider -->
  <line x1="528" y1="228" x2="1128" y2="228" stroke="{t['border']}" stroke-width="1" opacity="0">
    <animate attributeName="opacity" values="0;1" dur="0.3s" fill="freeze" begin="1.4s"/>
  </line>

  <!-- Code block -->
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.4s" fill="freeze" begin="1.5s"/>
    <rect x="528" y="238" width="600" height="178" rx="10" fill="{cb}" stroke="{cbrd}" stroke-width="1"/>
    <!-- Line 1 -->
    <text x="548" y="260" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11.5">
      <tspan fill="{ln}">1  </tspan><tspan fill="{kw}">public class </tspan><tspan fill="{t['text1']}">AdnanUmar </tspan><tspan fill="{sy}">implements </tspan><tspan fill="{ty}">Engineer </tspan><tspan fill="{sy}">{{</tspan>
    </text>
    <!-- Line 2 -->
    <text x="548" y="278" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11.5">
      <tspan fill="{ln}">2  </tspan><tspan fill="{kw}">  final </tspan><tspan fill="{ty}">String  </tspan><tspan fill="{t['text1']}">focus </tspan><tspan fill="{sy}">= </tspan><tspan fill="{st}">"Backend · Cloud · AI"</tspan><tspan fill="{sy}">;</tspan>
    </text>
    <!-- Line 3 -->
    <text x="548" y="296" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11.5">
      <tspan fill="{ln}">3  </tspan><tspan fill="{kw}">  final </tspan><tspan fill="{ty}">Stack   </tspan><tspan fill="{t['text1']}">primary </tspan><tspan fill="{sy}">= </tspan><tspan fill="{st}">Stack.of(JAVA, SPRING, KAFKA)</tspan><tspan fill="{sy}">;</tspan>
    </text>
    <!-- Line 4 -->
    <text x="548" y="314" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11.5">
      <tspan fill="{ln}">4  </tspan><tspan fill="{kw}">  final </tspan><tspan fill="{ty}">String  </tspan><tspan fill="{t['text1']}">location </tspan><tspan fill="{sy}">= </tspan><tspan fill="{st}">"India"</tspan><tspan fill="{sy}">;</tspan>
    </text>
    <!-- Line 5 -->
    <text x="548" y="332" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11.5">
      <tspan fill="{ln}">5  </tspan><tspan fill="{kw}">  final </tspan><tspan fill="{ty}">String  </tspan><tspan fill="{t['text1']}">status </tspan><tspan fill="{sy}">= </tspan><tspan fill="{a3}">"open_to_work"</tspan><tspan fill="{sy}">;</tspan>
    </text>
    <!-- Line 6 -->
    <text x="548" y="350" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11.5">
      <tspan fill="{ln}">6  </tspan><tspan fill="{kw}">  public </tspan><tspan fill="{ty}">String </tspan><tspan fill="{t['text1']}">build</tspan><tspan fill="{sy}">()</tspan><tspan fill="{ty}"> String </tspan><tspan fill="{sy}">{{</tspan>
    </text>
    <!-- Line 7 -->
    <text x="548" y="368" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11.5">
      <tspan fill="{ln}">7  </tspan><tspan fill="{kw}">    return </tspan><tspan fill="{st}">"Clean systems. Event-driven. Scalable."</tspan><tspan fill="{sy}">;</tspan>
    </text>
    <!-- Line 8 -->
    <text x="548" y="386" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11.5">
      <tspan fill="{ln}">8  </tspan><tspan fill="{sy}">  }} }}</tspan>
    </text>
    <!-- Cursor -->
    <rect x="548" y="390" width="7" height="11" fill="{a2}" rx="1">
      <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- What I build — 3 cards -->
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.4s" fill="freeze" begin="2.0s"/>
    <text x="528" y="438" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
      font-size="10" fill="{t['muted']}">// what I ship</text>

    <rect x="528" y="446" width="186" height="60" rx="8" fill="{p2}" stroke="{p2s}" stroke-width="1"/>
    <text x="539" y="463" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11" font-weight="600" fill="{a1}">Distributed Microservices</text>
    <text x="539" y="479" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9.5" fill="{t['muted']}">Spring Boot · Kafka · Kubernetes</text>
    <text x="539" y="495" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9.5" fill="{t['muted']}">Event-driven · resilient · observable</text>

    <rect x="722" y="446" width="186" height="60" rx="8" fill="{p1}" stroke="{p1s}" stroke-width="1"/>
    <text x="733" y="463" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11" font-weight="600" fill="{a2}">Cloud-Native Backends</text>
    <text x="733" y="479" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9.5" fill="{t['muted']}">Docker · K8s · CI/CD · AWS</text>
    <text x="733" y="495" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9.5" fill="{t['muted']}">Production-grade deployments</text>

    <rect x="916" y="446" width="192" height="60" rx="8" fill="{p3}" stroke="{p3s}" stroke-width="1"/>
    <text x="927" y="463" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11" font-weight="600" fill="{a3}">AI-Integrated Systems</text>
    <text x="927" y="479" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9.5" fill="{t['muted']}">Spring AI · OpenAI APIs</text>
    <text x="927" y="495" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9.5" fill="{t['muted']}">Intelligent context-aware services</text>
  </g>

  <!-- Footer quote -->
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.5s" fill="freeze" begin="2.5s"/>
    <line x1="528" y1="525" x2="1128" y2="525" stroke="{t['border']}" stroke-width="1"/>
    <text x="528" y="543" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
      font-size="11" fill="{t['muted']}" font-style="italic">
      "Clean systems. Event-driven flows. Scalable architecture."
    </text>
  </g>"""


def particles(t):
    a1, a2, a3 = t['accent1'], t['accent2'], t['accent3']
    return f"""
  <!-- Floating particles -->
  <circle cx="200" cy="120" r="1.5" fill="{a1}" opacity="0"><animate attributeName="cy" values="120;108;120" dur="5.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.5;0" dur="5.5s" repeatCount="indefinite"/></circle>
  <circle cx="420" cy="280" r="2"   fill="{a2}" opacity="0"><animate attributeName="cy" values="280;268;280" dur="6.8s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.4;0" dur="6.8s" repeatCount="indefinite"/></circle>
  <circle cx="780" cy="160" r="1.8" fill="{a3}" opacity="0"><animate attributeName="cy" values="160;150;160" dur="7.2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.4;0" dur="7.2s" repeatCount="indefinite"/></circle>
  <circle cx="950" cy="420" r="2"   fill="{a1}" opacity="0"><animate attributeName="cy" values="420;408;420" dur="5.9s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.5;0" dur="5.9s" repeatCount="indefinite"/></circle>
  <circle cx="130" cy="460" r="1.5" fill="{a3}" opacity="0"><animate attributeName="cy" values="460;449;460" dur="6.3s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.4;0" dur="6.3s" repeatCount="indefinite"/></circle>
  <circle cx="680" cy="530" r="1.2" fill="{a2}" opacity="0"><animate attributeName="cy" values="530;519;530" dur="8.1s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.3;0" dur="8.1s" repeatCount="indefinite"/></circle>
  <circle cx="1050" cy="300" r="1.8" fill="{a1}" opacity="0"><animate attributeName="cy" values="300;289;300" dur="7.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.45;0" dur="7.6s" repeatCount="indefinite"/></circle>
  <circle cx="490" cy="560" r="1.2" fill="{a3}" opacity="0"><animate attributeName="cy" values="560;549;560" dur="9.2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.3;0" dur="9.2s" repeatCount="indefinite"/></circle>"""


def build_hero(theme_name, t, b64_photo, noise_op, scan_op):
    W, H = 1180, 610
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
        defs(t, noise_op, scan_op),
        f'  <!-- Background -->',
        f'  <rect width="{W}" height="{H}" fill="{t["bg"]}"/>',
        f'  <rect width="{W}" height="{H}" fill="url(#blob1)"/>',
        f'  <rect width="{W}" height="{H}" fill="url(#blob2)"/>',
        f'  <rect width="{W}" height="{H}" filter="url(#noise)" opacity="0.3"/>',
        f'  <rect width="{W}" height="{H}" mask="url(#scanMask)" opacity="0.4"/>',
        f'  <!-- Outer glass frame -->',
        f'  <rect x="16" y="16" width="1148" height="578" rx="22"',
        f'    fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1">',
        f'    <animate attributeName="stroke-opacity" values="0.07;0.18;0.07" dur="3s" repeatCount="indefinite"/>',
        f'  </rect>',
        f'  <rect x="16" y="16" width="1148" height="578" rx="22"',
        f'    fill="none" stroke="url(#shimmer)" stroke-width="1.5" opacity="0.6"/>',
        left_panel(t, b64_photo),
        right_panel(t),
        particles(t),
        '</svg>',
    ]
    return '\n'.join(lines)


def build_info_card(t, b64_photo):
    a1, a2, a3 = t['accent1'], t['accent2'], t['accent3']
    p1, p1s = t['pill1'], t['pill1s']
    p2, p2s = t['pill2'], t['pill2s']
    p3, p3s = t['pill3'], t['pill3s']
    W, H = 760, 220
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <linearGradient id="accentG" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{a1}"><animate attributeName="stop-color" values="{a1};{a2};{a1}" dur="5s" repeatCount="indefinite"/></stop>
      <stop offset="100%" stop-color="{a2}"><animate attributeName="stop-color" values="{a2};{a1};{a2}" dur="5s" repeatCount="indefinite"/></stop>
    </linearGradient>
    <linearGradient id="shimmer" x1="-100%" y1="0%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="rgba(255,255,255,0)"/>
      <stop offset="50%" stop-color="rgba(255,255,255,0.25)"/>
      <stop offset="100%" stop-color="rgba(255,255,255,0)"/>
      <animate attributeName="x1" values="-100%;100%" dur="3s" repeatCount="indefinite"/>
      <animate attributeName="x2" values="0%;200%" dur="3s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="headerG" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{a1}" stop-opacity="0.3"/>
      <stop offset="50%" stop-color="{a2}" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="{a3}" stop-opacity="0.1"/>
    </linearGradient>
    <clipPath id="avatarCircle"><circle cx="36" cy="25" r="20"/></clipPath>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- Card background -->
  <rect width="{W}" height="{H}" rx="14" fill="{t['panel2']}"/>
  <!-- Ambient blob -->
  <radialGradient id="b1" cx="10%" cy="50%" r="40%">
    <stop offset="0%" stop-color="{a1}" stop-opacity="0.12"/><stop offset="100%" stop-color="{a1}" stop-opacity="0"/>
  </radialGradient>
  <rect width="{W}" height="{H}" rx="14" fill="url(#b1)"/>

  <!-- Gradient header bar -->
  <rect x="0" y="0" width="{W}" height="52" rx="14" fill="url(#headerG)"/>
  <rect x="0" y="42" width="{W}" height="10" fill="url(#headerG)" opacity="0.5"/>
  <!-- Accent underline -->
  <line x1="0" y1="52" x2="{W}" y2="52" stroke="url(#accentG)" stroke-width="1.5" opacity="0.5"/>

  <!-- Traffic lights -->
  <circle cx="22" cy="26" r="5.5" fill="#FF5F57"><animate attributeName="opacity" values="1;0.7;1" dur="2s" repeatCount="indefinite"/></circle>
  <circle cx="38" cy="26" r="5.5" fill="#FEBC2E"><animate attributeName="opacity" values="1;0.7;1" dur="2s" repeatCount="indefinite" begin="0.2s"/></circle>
  <circle cx="54" cy="26" r="5.5" fill="#28C840"><animate attributeName="opacity" values="1;0.7;1" dur="2s" repeatCount="indefinite" begin="0.4s"/></circle>

  <!-- Title -->
  <text x="380" y="32" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
    font-size="11" fill="{t['muted']}" text-anchor="middle">neofetch — adnan@backend</text>

  <!-- Small avatar in header -->
  <image href="{b64_photo}" x="16" y="5" width="42" height="42"
    clip-path="url(#avatarCircle)" preserveAspectRatio="xMidYMid slice"/>
  <circle cx="36" cy="26" r="20" fill="none" stroke="{a2}" stroke-width="1.5" opacity="0.5">
    <animate attributeName="stroke-opacity" values="0.5;0.9;0.5" dur="2s" repeatCount="indefinite"/>
  </circle>

  <!-- LEFT: larger photo section -->
  <image href="{b64_photo}" x="14" y="60" width="100" height="100"
    clip-path="url(#bigCircle)" preserveAspectRatio="xMidYMid slice"/>
  <clipPath id="bigCircle"><circle cx="64" cy="110" r="50"/></clipPath>
  <circle cx="64" cy="110" r="52" fill="none" stroke="{a1}" stroke-width="1.5" opacity="0.4">
    <animate attributeName="r" values="52;55;52" dur="3s" repeatCount="indefinite"/>
    <animate attributeName="stroke-opacity" values="0.4;0.7;0.4" dur="3s" repeatCount="indefinite"/>
  </circle>

  <!-- Open-to-work badge under photo -->
  <rect x="22" y="166" width="84" height="18" rx="9" fill="{p3}" stroke="{p3s}" stroke-width="1"/>
  <circle cx="33" cy="175" r="3.5" fill="{a3}"><animate attributeName="r" values="3.5;4.5;3.5" dur="1.5s" repeatCount="indefinite"/></circle>
  <text x="58" y="179" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
    font-size="8.5" fill="{a3}" text-anchor="middle">accepting offers</text>

  <!-- RIGHT: neofetch info lines -->
  <g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">

    <!-- Username / hostname header -->
    <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.25s" fill="freeze" begin="0.4s"/>
      <text x="128" y="72" font-size="13" font-weight="700" fill="{a2}" filter="url(#glow)">adnan</text>
      <text x="176" y="72" font-size="13" fill="{t['muted']}">@</text>
      <text x="186" y="72" font-size="13" font-weight="700" fill="{a3}" filter="url(#glow)">backend</text>
      <line x1="128" y1="77" x2="520" y2="77" stroke="{t['border']}" stroke-width="1"/>
    </g>

    <!-- Info lines with stagger -->
    <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.2s" fill="freeze" begin="0.6s"/>
      <text x="128" y="95"  font-size="11" fill="{t['muted']}">Name</text><text x="190" y="95"  font-size="11" fill="{t['text1']}">Md Adnan Umar</text>
    </g>
    <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.2s" fill="freeze" begin="0.8s"/>
      <text x="128" y="112" font-size="11" fill="{t['muted']}">Role</text><text x="190" y="112" font-size="11" fill="url(#accentG)">Software Engineer</text>
    </g>
    <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.2s" fill="freeze" begin="1.0s"/>
      <text x="128" y="129" font-size="11" fill="{t['muted']}">OS</text><text x="190" y="129" font-size="11" fill="{t['text2']}">India &#127470;&#127475;</text>
    </g>
    <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.2s" fill="freeze" begin="1.2s"/>
      <text x="128" y="146" font-size="11" fill="{t['muted']}">Education</text><text x="218" y="146" font-size="11" fill="{t['text2']}">B.Tech CSE · Final Year</text>
    </g>
    <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.2s" fill="freeze" begin="1.4s"/>
      <text x="128" y="163" font-size="11" fill="{t['muted']}">Terminal</text><text x="218" y="163" font-size="11" fill="{t['text2']}">Spring Boot 3 · Java 21</text>
    </g>
    <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.2s" fill="freeze" begin="1.6s"/>
      <text x="128" y="180" font-size="11" fill="{t['muted']}">Packages</text><text x="218" y="180" font-size="11" fill="{t['text2']}">Kafka · K8s · Docker · Spring AI</text>
    </g>
    <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.2s" fill="freeze" begin="1.8s"/>
      <text x="128" y="197" font-size="11" fill="{t['muted']}">Uptime</text><text x="218" y="197" font-size="11" fill="{t['text2']}">Building since 2022</text>
    </g>
  </g>

  <!-- Right: skill pills -->
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.3s" fill="freeze" begin="2.0s"/>
    <!-- Row 1 -->
    <rect x="390" y="65"  width="44"  height="18" rx="9"  fill="{p1}" stroke="{p1s}" stroke-width="1"/><text x="412" y="78"  font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a2}" text-anchor="middle">Java</text>
    <rect x="440" y="65"  width="86"  height="18" rx="9"  fill="{p2}" stroke="{p2s}" stroke-width="1"/><text x="483" y="78"  font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a1}" text-anchor="middle">Spring Boot</text>
    <rect x="532" y="65"  width="46"  height="18" rx="9"  fill="{p3}" stroke="{p3s}" stroke-width="1"/><text x="555" y="78"  font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a3}" text-anchor="middle">Kafka</text>
    <rect x="584" y="65"  width="54"  height="18" rx="9"  fill="{p1}" stroke="{p1s}" stroke-width="1"/><text x="611" y="78"  font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a2}" text-anchor="middle">Docker</text>
    <rect x="644" y="65"  width="72"  height="18" rx="9"  fill="{p2}" stroke="{p2s}" stroke-width="1"/><text x="680" y="78"  font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a1}" text-anchor="middle">Kubernetes</text>
    <!-- Row 2 -->
    <rect x="390" y="89"  width="78"  height="18" rx="9"  fill="{p3}" stroke="{p3s}" stroke-width="1"/><text x="429" y="102" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a3}" text-anchor="middle">PostgreSQL</text>
    <rect x="474" y="89"  width="46"  height="18" rx="9"  fill="{p1}" stroke="{p1s}" stroke-width="1"/><text x="497" y="102" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a2}" text-anchor="middle">Redis</text>
    <rect x="526" y="89"  width="54"  height="18" rx="9"  fill="{p2}" stroke="{p2s}" stroke-width="1"/><text x="553" y="102" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a1}" text-anchor="middle">Python</text>
    <rect x="586" y="89"  width="48"  height="18" rx="9"  fill="{p3}" stroke="{p3s}" stroke-width="1"/><text x="610" y="102" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a3}" text-anchor="middle">React</text>
    <rect x="640" y="89"  width="76"  height="18" rx="9"  fill="{p1}" stroke="{p1s}" stroke-width="1"/><text x="678" y="102" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a2}" text-anchor="middle">Spring AI</text>
    <!-- Row 3 -->
    <rect x="390" y="113" width="52"  height="18" rx="9"  fill="{p2}" stroke="{p2s}" stroke-width="1"/><text x="416" y="126" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a1}" text-anchor="middle">CI/CD</text>
    <rect x="448" y="113" width="46"  height="18" rx="9"  fill="{p3}" stroke="{p3s}" stroke-width="1"/><text x="471" y="126" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a3}" text-anchor="middle">AWS</text>
    <rect x="500" y="113" width="68"  height="18" rx="9"  fill="{p1}" stroke="{p1s}" stroke-width="1"/><text x="534" y="126" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a2}" text-anchor="middle">Next.js</text>
    <rect x="574" y="113" width="68"  height="18" rx="9"  fill="{p2}" stroke="{p2s}" stroke-width="1"/><text x="608" y="126" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a1}" text-anchor="middle">FastAPI</text>
    <rect x="648" y="113" width="68"  height="18" rx="9"  fill="{p3}" stroke="{p3s}" stroke-width="1"/><text x="682" y="126" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{a3}" text-anchor="middle">GraphQL</text>
  </g>

  <!-- Color palette swatches -->
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.3s" fill="freeze" begin="2.3s"/>
    <text x="390" y="154" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{t['muted']}">//  palette</text>
    <rect x="390" y="160" width="16" height="16" rx="3" fill="#030712"/>
    <rect x="410" y="160" width="16" height="16" rx="3" fill="{a1}"/>
    <rect x="430" y="160" width="16" height="16" rx="3" fill="{a2}"/>
    <rect x="450" y="160" width="16" height="16" rx="3" fill="{a3}"/>
    <rect x="470" y="160" width="16" height="16" rx="3" fill="#F8FAFC"/>
    <rect x="490" y="160" width="16" height="16" rx="3" fill="#A78BFA"/>
    <rect x="510" y="160" width="16" height="16" rx="3" fill="#34D399"/>
    <rect x="530" y="160" width="16" height="16" rx="3" fill="#94A3B8"/>
  </g>

  <!-- Highlights right column -->
  <g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.3s" fill="freeze" begin="2.5s"/>
    <text x="578" y="154" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{t['muted']}">//  highlights</text>
    <text x="578" y="168" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{t['text2']}">&#9671; Distributed microservices on K8s</text>
    <text x="578" y="181" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{t['text2']}">&#9671; Event-driven Kafka pipelines</text>
    <text x="578" y="194" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{t['text2']}">&#9671; AI-integrated Spring Boot apps</text>
    <text x="578" y="207" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{t['text2']}">&#9671; Clean, scalable backend systems</text>
  </g>

  <!-- Border + shimmer -->
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="13.5"
    fill="none" stroke="{t['border']}" stroke-width="1">
    <animate attributeName="stroke-opacity" values="0.07;0.18;0.07" dur="3s" repeatCount="indefinite"/>
  </rect>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="13.5"
    fill="none" stroke="url(#shimmer)" stroke-width="1" opacity="0.5"/>
</svg>"""


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import pathlib

    root = pathlib.Path(".")

    print("Building dark.svg …")
    dark_svg = build_hero("dark", DARK, B64, "0.32", "0.3")
    (root / "dark.svg").write_text(dark_svg, encoding="utf-8")
    print(f"  → dark.svg  ({len(dark_svg):,} chars)")

    print("Building light.svg …")
    light_svg = build_hero("light", LIGHT, B64, "0.12", "0.15")
    (root / "light.svg").write_text(light_svg, encoding="utf-8")
    print(f"  → light.svg  ({len(light_svg):,} chars)")

    print("Building info-card.svg (dark) …")
    info_dark = build_info_card(DARK, B64)
    (root / "info-card.svg").write_text(info_dark, encoding="utf-8")
    print(f"  → info-card.svg  ({len(info_dark):,} chars)")

    print("\nAll SVGs written.")
