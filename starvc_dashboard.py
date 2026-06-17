#!/usr/bin/env python3
"""StarVC Health Dashboard — live monitor on localhost:3000"""

import json
import urllib.request
from flask import Flask, Response

API_URL = "https://starvc.ir/api/health"
app = Flask(__name__)


def fetch_health():
    try:
        req = urllib.request.Request(API_URL, headers={"User-Agent": "StarVC-Dashboard/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}


@app.route("/api/health")
def api_health():
    data = fetch_health()
    return Response(json.dumps(data), mimetype="application/json")


HTML = r"""<!DOCTYPE html>
<html lang="en" dir="ltr" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>StarVC Health Dashboard</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@600;700;800;900&display=swap');

:root{
  --g:#018182;--g2:#02b5b6;--g3:#e6f5f5;--g4:#b2dcdc;
  --ink:#0d2e2e;--ink2:#3a6060;--bg:#f5fafa;--white:#fff;
  --yellow:#ffd166;--coral:#ff6b6b;--green:#22c55e;
  --border:3px solid var(--ink);
  --shadow:5px 5px 0 var(--ink);--shadow-sm:3px 3px 0 var(--ink);--shadow-lg:8px 8px 0 var(--ink);
  --rad:16px;--rad-sm:12px;
}
[data-theme="dark"]{
  --g:#02b5b6;--g2:#01cfcf;--g3:#0d2e2e;--g4:#1a4a4a;
  --ink:#e0f5f5;--ink2:#7ec8c8;--bg:#0a1a1a;--white:#111f1f;
  --yellow:#ffd166;--coral:#ff6b6b;--green:#22c55e;
  --border:3px solid rgba(255,255,255,0.15);
  --shadow:5px 5px 0 rgba(0,0,0,0.4);--shadow-sm:3px 3px 0 rgba(0,0,0,0.4);--shadow-lg:8px 8px 0 rgba(0,0,0,0.5);
}
[data-theme="dark"] .nav-tag{background:var(--g3);color:var(--ink);}
[data-theme="dark"] .srv-card{background:#1a2e2e;border-color:rgba(255,255,255,0.10);box-shadow:5px 5px 0 rgba(0,0,0,0.4);color:var(--ink);}
[data-theme="dark"] .srv-card:hover{box-shadow:9px 9px 0 rgba(0,0,0,0.5);}
[data-theme="dark"] .srv-desc{color:var(--ink2);}
[data-theme="dark"] .srv-icon{background:#0d2020;border-color:rgba(255,255,255,0.10);}
[data-theme="dark"] .stat-card{background:#1a2e2e;border-color:rgba(255,255,255,0.10);box-shadow:5px 5px 0 rgba(0,0,0,0.4);}
[data-theme="dark"] .stat-card:hover{box-shadow:9px 9px 0 rgba(0,0,0,0.5);}
[data-theme="dark"] .users-badge{background:#0d2020;}
[data-theme="dark"] footer{background:var(--white);border-top-color:rgba(255,255,255,0.08);color:var(--ink2);}

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth}
body{
  font-family:'Inter','Vazirmatn',Tahoma,sans-serif;
  background:var(--bg);color:var(--ink);
  min-height:100vh;display:flex;flex-direction:column;
  position:relative;overflow-x:hidden;
}
body::before{
  content:'';position:fixed;inset:0;
  background-image:radial-gradient(circle,var(--g4) 1.5px,transparent 1.5px);
  background-size:28px 28px;opacity:.35;pointer-events:none;z-index:0;
}

/* theme toggle */
.theme-toggle{
  position:relative;width:64px;height:32px;flex-shrink:0;cursor:pointer;
}
.theme-toggle input{opacity:0;width:0;height:0;position:absolute;}
.theme-track{
  position:absolute;inset:0;
  background:linear-gradient(135deg,#87ceeb,#ffd166);
  border:var(--border);border-radius:99px;
  transition:background .4s;overflow:hidden;
}
[data-theme="dark"] .theme-track{background:linear-gradient(135deg,#1a1a3e,#0d2040);}
.theme-stars{
  position:absolute;top:4px;left:6px;
  display:flex;gap:3px;opacity:0;transition:opacity .4s;pointer-events:none;
}
[data-theme="dark"] .theme-stars{opacity:1;}
.theme-stars span{width:3px;height:3px;border-radius:50%;background:#fff;display:block;}
.theme-stars span:nth-child(2){margin-top:5px;opacity:.7;}
.theme-stars span:nth-child(3){margin-top:2px;opacity:.5;}
.theme-thumb{
  position:absolute;top:3px;right:3px;
  width:22px;height:22px;border-radius:50%;
  background:#fff;border:2px solid var(--ink);
  display:flex;align-items:center;justify-content:center;
  transition:transform .35s cubic-bezier(.34,1.56,.64,1),background .4s,border-color .4s;
  box-shadow:0 2px 6px rgba(0,0,0,.25);
}
[data-theme="dark"] .theme-thumb{transform:translateX(-32px);background:#1a1a3e;border-color:rgba(255,255,255,0.3);}
.theme-thumb svg{width:13px;height:13px;}
.theme-thumb .icon-sun{display:block;}
.theme-thumb .icon-moon{display:none;}
[data-theme="dark"] .theme-thumb .icon-sun{display:none;}
[data-theme="dark"] .theme-thumb .icon-moon{display:block;}

/* nav */
nav{
  position:relative;z-index:100;
  display:flex;align-items:center;justify-content:space-between;
  padding:14px 32px;background:var(--white);
  border-bottom:var(--border);
}
.nav-logo{display:flex;align-items:center;gap:10px;font-size:20px;font-weight:900;color:var(--ink);text-decoration:none;}
.nav-icon{width:34px;height:34px;background:var(--g);border:var(--border);border-radius:10px;display:flex;align-items:center;justify-content:center;}
.nav-icon svg{width:22px;height:22px;fill:#fff;}
.nav-center{display:flex;align-items:center;gap:6px;}
.nav-tag{padding:5px 12px;border:var(--border);border-radius:99px;font-size:11px;font-weight:700;background:var(--g3);color:var(--ink);box-shadow:var(--shadow-sm);}
.nav-tag.live{background:var(--green);color:#fff;display:flex;align-items:center;gap:6px;}
.nav-tag .pdot{width:6px;height:6px;border-radius:50%;background:#fff;animation:pulse-dot 1.5s infinite;}
@keyframes pulse-dot{0%,100%{opacity:1}50%{opacity:.2}}
.nav-actions{display:flex;align-items:center;gap:10px;}

/* hero */
.hero{position:relative;z-index:1;padding:48px 32px 32px;max-width:1100px;margin:0 auto;width:100%;flex:1;}
.hero-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:32px;flex-wrap:wrap;gap:16px;}
.status-badge{display:inline-flex;align-items:center;gap:10px;background:var(--green);border:var(--border);border-radius:99px;padding:8px 22px;font-size:14px;font-weight:900;color:#fff;box-shadow:var(--shadow-sm);}
.status-badge .pdot{width:10px;height:10px;border-radius:50%;background:#fff;animation:pulse-dot 1.5s infinite;}
.hero-meta{display:flex;align-items:center;gap:16px;flex-wrap:wrap;font-size:13px;color:var(--ink2);font-weight:600;}
.hero-meta .sep{width:4px;height:4px;border-radius:50%;background:var(--g4);}
.refresh-indicator{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--ink2);font-weight:600;}
.refresh-indicator svg{animation:spin 2s linear infinite;width:14px;height:14px;stroke:var(--g2);}
@keyframes spin{to{transform:rotate(360deg)}}

/* stat cards row */
.stats-row{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px;}
.stat-card{background:var(--white);border:var(--border);border-radius:var(--rad);padding:22px 20px;box-shadow:var(--shadow);transition:transform .2s,box-shadow .2s;}
.stat-card:hover{transform:translate(-3px,-3px);box-shadow:8px 8px 0 var(--ink);}
.stat-card.highlight{background:var(--g);color:#fff;}
.stat-card.highlight .stat-label{color:rgba(255,255,255,.8);}
.stat-card.highlight .stat-icon{background:rgba(255,255,255,.2);border-color:rgba(255,255,255,.3);}
.stat-card.highlight .stat-value{color:#fff;}
.stat-icon{width:40px;height:40px;background:var(--g3);border:var(--border);border-radius:var(--rad-sm);display:flex;align-items:center;justify-content:center;margin-bottom:12px;}
.stat-icon svg{width:20px;height:20px;fill:var(--ink);}
.stat-card.highlight .stat-icon svg{fill:#fff;}
.stat-label{font-size:12px;font-weight:700;color:var(--ink2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px;}
.stat-value{font-size:28px;font-weight:900;color:var(--ink);line-height:1.1;font-variant-numeric:tabular-nums;}
.stat-sub{font-size:12px;color:var(--ink2);margin-top:4px;font-weight:600;}

/* services grid */
.sec-title{font-size:18px;font-weight:900;margin-bottom:16px;display:flex;align-items:center;gap:8px;}
.sec-pill{display:inline-block;background:var(--g);color:#fff;border:var(--border);border-radius:99px;padding:3px 16px;font-size:12px;transform:rotate(-1deg);}
.srv-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin-bottom:24px;}
.srv-card{background:var(--white);border:var(--border);border-radius:var(--rad);padding:22px 20px;box-shadow:var(--shadow);transition:transform .2s,box-shadow .2s;position:relative;}
.srv-card:hover{transform:translate(-3px,-3px);box-shadow:8px 8px 0 var(--ink);}
.srv-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;}
.srv-name{display:flex;align-items:center;gap:10px;font-size:15px;font-weight:900;}
.srv-icon{width:34px;height:34px;background:var(--g3);border:var(--border);border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.srv-icon svg{width:18px;height:18px;fill:var(--ink);}
.srv-status{display:flex;align-items:center;gap:6px;font-size:12px;font-weight:700;text-transform:uppercase;}
.sdot{width:10px;height:10px;border-radius:50%;flex-shrink:0;}
.sdot.on{background:var(--green);animation:pulse-dot 2s infinite;}
.sdot.off{background:var(--coral);}
.srv-bar-wrap{margin-bottom:8px;}
.srv-bar-label{display:flex;justify-content:space-between;font-size:12px;font-weight:600;color:var(--ink2);margin-bottom:4px;}
.srv-bar{height:14px;background:var(--g3);border:var(--border);border-radius:99px;overflow:hidden;}
.srv-bar-fill{height:100%;background:var(--g);border-radius:99px;transition:width .6s cubic-bezier(.16,1,.3,1);}
.srv-bar-fill.green{background:var(--green);}
.srv-bar-fill.yellow{background:var(--yellow);}
.srv-bar-fill.red{background:var(--coral);}
.srv-desc{font-size:12px;color:var(--ink2);font-weight:600;margin-top:4px;}
.srv-users{display:flex;align-items:center;gap:8px;margin-top:10px;padding-top:10px;border-top:2px solid var(--g3);}
.srv-users .users-count{font-size:22px;font-weight:900;color:var(--ink);font-variant-numeric:tabular-nums;}
.srv-users .users-label{font-size:12px;color:var(--ink2);font-weight:600;}
.online-dot{width:8px;height:8px;border-radius:50%;background:var(--green);animation:pulse-dot 1.5s infinite;}

/* memory */
.mem-card{background:var(--white);border:var(--border);border-radius:var(--rad);padding:22px 24px;box-shadow:var(--shadow);transition:box-shadow .2s;margin-bottom:24px;}
.mem-card:hover{box-shadow:8px 8px 0 var(--ink);}
.mem-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;}
.mem-title{display:flex;align-items:center;gap:10px;font-size:16px;font-weight:900;}
.mem-nums{font-size:14px;font-weight:700;color:var(--ink2);font-variant-numeric:tabular-nums;}
.mem-bar{height:22px;background:var(--g3);border:var(--border);border-radius:99px;overflow:hidden;}
.mem-bar-fill{height:100%;background:linear-gradient(90deg,var(--g),var(--g2));border-radius:99px;transition:width .6s cubic-bezier(.16,1,.3,1);}

/* uptime card */
.uptime-row{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px;}
.uptime-card{background:var(--white);border:var(--border);border-radius:var(--rad);padding:20px 24px;box-shadow:var(--shadow);display:flex;align-items:center;gap:16px;transition:transform .2s,box-shadow .2s;}
.uptime-card:hover{transform:translate(-3px,-3px);box-shadow:8px 8px 0 var(--ink);}
.uptime-card .stat-icon{width:48px;height:48px;margin-bottom:0;}
.uptime-info{}
.uptime-label{font-size:12px;font-weight:700;color:var(--ink2);text-transform:uppercase;letter-spacing:.5px;}
.uptime-value{font-size:22px;font-weight:900;color:var(--ink);}

/* footer */
footer{
  position:relative;z-index:1;
  border-top:var(--border);padding:18px 32px;
  display:flex;align-items:center;justify-content:space-between;
  background:var(--white);font-size:12px;color:var(--ink2);font-weight:600;
  margin-top:auto;flex-wrap:wrap;gap:12px;
}
.footer-logo{font-weight:900;color:var(--ink);font-size:14px;}

/* fade up animation */
.fu{opacity:0;transform:translateY(24px);animation:fu .55s cubic-bezier(.16,1,.3,1) forwards;}
@keyframes fu{to{opacity:1;transform:translateY(0)}}

/* highlight flash on update */
@keyframes flash{0%{background:rgba(1,129,130,.15)}100%{background:transparent}}
.flash{animation:flash .6s ease-out;}

/* responsive */
@media(max-width:800px){
  .stats-row{grid-template-columns:repeat(2,1fr);}
  .srv-grid{grid-template-columns:1fr;}
  .uptime-row{grid-template-columns:1fr;}
  nav{padding:10px 16px;}
  .hero{padding:24px 16px;}
  footer{padding:14px 16px;flex-direction:column;text-align:center;}
  .nav-tag.live .label{display:none;}
}
@media(max-width:480px){
  .stats-row{grid-template-columns:1fr;}
}
</style>
</head>
<body>

<nav>
  <a href="/" class="nav-logo">
    <div class="nav-icon">
      <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
    </div>
    StarVC Health
  </a>
  <div class="nav-center">
    <span class="nav-tag">v1.0</span>
    <span class="nav-tag live"><span class="pdot"></span><span class="label">LIVE</span></span>
  </div>
  <div class="nav-actions">
    <label class="theme-toggle" title="Toggle theme">
      <input type="checkbox" id="themeToggle" onchange="toggleTheme(this)">
      <div class="theme-track">
        <div class="theme-stars"><span></span><span></span><span></span></div>
        <div class="theme-thumb">
          <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round">
            <circle cx="12" cy="12" r="4"/>
            <line x1="12" y1="2" x2="12" y2="5"/><line x1="12" y1="19" x2="12" y2="22"/>
            <line x1="4.22" y1="4.22" x2="6.34" y2="6.34"/><line x1="17.66" y1="17.66" x2="19.78" y2="19.78"/>
            <line x1="2" y1="12" x2="5" y2="12"/><line x1="19" y1="12" x2="22" y2="12"/>
            <line x1="4.22" y1="19.78" x2="6.34" y2="17.66"/><line x1="17.66" y1="6.34" x2="19.78" y2="4.22"/>
          </svg>
          <svg class="icon-moon" viewBox="0 0 24 24" fill="#c7d2fe" stroke="#818cf8" stroke-width="2" stroke-linecap="round">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
          </svg>
        </div>
      </div>
    </label>
  </div>
</nav>

<main class="hero">
  <div class="hero-top fu">
    <div class="status-badge">
      <span class="pdot"></span>
      <span id="overallStatus">All Systems Operational</span>
    </div>
    <div class="hero-meta">
      <span id="lastChecked">checking...</span>
      <span class="sep"></span>
      <span>refreshes every 10s</span>
      <span class="refresh-indicator">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>
      </span>
    </div>
  </div>

  <div class="stats-row fu">
    <div class="stat-card highlight" style="animation-delay:.05s">
      <div class="stat-icon">
        <svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/></svg>
      </div>
      <div class="stat-label">Overall</div>
      <div class="stat-value" id="overallValue">OK</div>
      <div class="stat-sub" id="overallSub">healthy</div>
    </div>
    <div class="stat-card" style="animation-delay:.1s">
      <div class="stat-icon">
        <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
      </div>
      <div class="stat-label">Uptime</div>
      <div class="stat-value" id="uptimeValue">--</div>
      <div class="stat-sub" id="uptimeSub">since last restart</div>
    </div>
    <div class="stat-card" style="animation-delay:.15s">
      <div class="stat-icon">
        <svg viewBox="0 0 24 24"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
      </div>
      <div class="stat-label">Users Online</div>
      <div class="stat-value" id="usersOnline">0</div>
      <div class="stat-sub" style="display:flex;align-items:center;gap:6px;">
        <span class="online-dot"></span>
        <span>currently connected</span>
      </div>
    </div>
    <div class="stat-card" style="animation-delay:.2s">
      <div class="stat-icon">
        <svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="2"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="12" y1="2" x2="12" y2="22"/></svg>
      </div>
      <div class="stat-label">Memory</div>
      <div class="stat-value" id="memValue">--</div>
      <div class="stat-sub" id="memSub">used / total</div>
    </div>
  </div>

  <div class="sec-title fu"><span class="sec-pill">Services</span> Health Status</div>

  <div class="srv-grid fu">
    <div class="srv-card" id="card-api">
      <div class="srv-head">
        <div class="srv-name">
          <div class="srv-icon"><svg viewBox="0 0 24 24"><path d="M13 9h-2v2h2V9zm0 4h-2v6h2v-6zm-1-9C6.48 4 2 8.48 2 14s4.48 10 10 10 10-4.48 10-10S17.52 4 12 4zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/></svg></div>
          API
        </div>
        <div class="srv-status"><span class="sdot" id="dot-api"></span><span id="label-api">checking</span></div>
      </div>
      <div class="srv-bar-wrap">
        <div class="srv-bar-label"><span>Uptime</span><span id="pct-api">--</span></div>
        <div class="srv-bar"><div class="srv-bar-fill" id="bar-api" style="width:0%"></div></div>
      </div>
    </div>

    <div class="srv-card" id="card-database">
      <div class="srv-head">
        <div class="srv-name">
          <div class="srv-icon"><svg viewBox="0 0 24 24"><path d="M12 3C7.58 3 4 4.79 4 7v10c0 2.21 3.58 4 8 4s8-1.79 8-4V7c0-2.21-3.58-4-8-4zm0 2c3.87 0 6 1.5 6 2s-2.13 2-6 2-6-1.5-6-2 2.13-2 6-2zm0 14c-3.87 0-6-1.5-6-2v-3.23c1.63.79 3.72 1.23 6 1.23s4.37-.44 6-1.23V17c0 .5-2.13 2-6 2zm0-7c-3.87 0-6-1.5-6-2V6.77C7.63 7.56 9.72 8 12 8s4.37-.44 6-1.23V10c0 .5-2.13 2-6 2z"/></svg></div>
          Database
        </div>
        <div class="srv-status"><span class="sdot" id="dot-database"></span><span id="label-database">checking</span></div>
      </div>
      <div class="srv-bar-wrap">
        <div class="srv-bar-label"><span>Uptime</span><span id="pct-database">--</span></div>
        <div class="srv-bar"><div class="srv-bar-fill" id="bar-database" style="width:0%"></div></div>
      </div>
    </div>

    <div class="srv-card" id="card-socket">
      <div class="srv-head">
        <div class="srv-name">
          <div class="srv-icon"><svg viewBox="0 0 24 24"><path d="M15.05 3.91c.29.22.56.49.78.78l-1.42 1.42c-.56-.46-1.22-.8-1.95-1V3.36c.79.08 1.54.28 2.22.55zM12 20c-4.41 0-8-3.59-8-8s3.59-8 8-8c.73 0 1.43.1 2.1.28L13.7 4.7c-.56-.23-1.15-.37-1.76-.37-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6c.01-.62-.14-1.22-.37-1.77l1.42-1.42c.28.69.47 1.43.56 2.19H20c-.09-1.06-.38-2.06-.84-2.96l1.42-1.42c.73 1.18 1.14 2.54 1.14 4.01 0 2.9-1.18 5.52-3.07 7.43l1.42 1.42c.2-.2.51-.51.51-.51l3.54 3.54-1.41 1.41-3.54-3.54c-.47.47-1.01.89-1.6 1.2l-1.44-1.44c.50-.23.96-.54 1.37-.93l-1.42-1.42c-.84.84-2 1.37-3.31 1.37zm0-4c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0-1c1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3 1.34 3 3 3z"/></svg></div>
          Socket
        </div>
        <div class="srv-status"><span class="sdot" id="dot-socket"></span><span id="label-socket">checking</span></div>
      </div>
      <div class="srv-bar-wrap">
        <div class="srv-bar-label"><span>Uptime</span><span id="pct-socket">--</span></div>
        <div class="srv-bar"><div class="srv-bar-fill" id="bar-socket" style="width:0%"></div></div>
      </div>
      <div class="srv-users">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="var(--ink2)"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
        <span class="users-count" id="socketUsers">0</span>
        <span class="users-label">users online</span>
        <span class="online-dot"></span>
      </div>
    </div>

    <div class="srv-card" id="card-voice">
      <div class="srv-head">
        <div class="srv-name">
          <div class="srv-icon"><svg viewBox="0 0 24 24"><path d="M12 14c1.66 0 2.99-1.34 2.99-3L15 5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm-1 7v-3.08c-2.84-.48-5-2.94-5-5.92h2c0 2.21 1.79 4 4 4s4-1.79 4-4h2c0 2.98-2.16 5.44-5 5.92V21h-2z"/></svg></div>
          Voice
        </div>
        <div class="srv-status"><span class="sdot" id="dot-voice"></span><span id="label-voice">checking</span></div>
      </div>
      <div class="srv-bar-wrap">
        <div class="srv-bar-label"><span>Uptime</span><span id="pct-voice">--</span></div>
        <div class="srv-bar"><div class="srv-bar-fill" id="bar-voice" style="width:0%"></div></div>
      </div>
    </div>
  </div>

  <div class="mem-card fu">
    <div class="mem-head">
      <div class="mem-title">
        <div class="stat-icon" style="width:36px;height:36px;margin-bottom:0;">
          <svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="2"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="12" y1="2" x2="12" y2="22"/></svg>
        </div>
        Memory
      </div>
      <div class="mem-nums" id="memNums">-- / -- MB</div>
    </div>
    <div class="mem-bar"><div class="mem-bar-fill" id="memBar" style="width:0%"></div></div>
  </div>
</main>

<footer>
  <div class="footer-logo">StarVC Health Dashboard</div>
  <div>Data from <a href="https://starvc.ir/api/health" target="_blank" style="color:var(--g);font-weight:700;text-decoration:none;">starvc.ir/api/health</a></div>
  <div>Built with the StarClient design language</div>
</footer>

<script>
var prevData = null;

function fmtUptime(ms) {
  var sec = Math.floor(ms / 1000);
  var d = Math.floor(sec / 86400), h = Math.floor((sec % 86400) / 3600);
  var m = Math.floor((sec % 3600) / 60), s = sec % 60;
  var parts = [];
  if (d) parts.push(d + 'd');
  if (h) parts.push(h + 'h');
  if (m) parts.push(m + 'm');
  if (s) parts.push(s + 's');
  return parts.join(' ') || '0s';
}

function getBarColor(pct) {
  if (pct >= 99) return 'green';
  if (pct >= 80) return 'yellow';
  return 'red';
}

function updateUI(data) {
  var now = new Date();
  document.getElementById('lastChecked').textContent = 'updated ' + now.toLocaleTimeString();

  var status = data.status || 'unknown';
  var statusEl = document.getElementById('overallStatus');
  statusEl.textContent = status === 'ok' ? 'All Systems Operational' : status.toUpperCase();

  document.getElementById('overallValue').textContent = status === 'ok' ? 'OK' : 'ERR';
  document.getElementById('overallSub').textContent = status === 'ok' ? 'healthy' : 'issues detected';

  var uptimeMs = data.uptime_ms || 0;
  document.getElementById('uptimeValue').textContent = fmtUptime(uptimeMs);

  var services = data.services || {};
  var svcMap = {api: 'api', database: 'database', socket: 'socket', voice: 'voice'};

  var totalConns = 0;

  Object.keys(svcMap).forEach(function(key) {
    var svc = services[key];
    var dot = document.getElementById('dot-' + key);
    var label = document.getElementById('label-' + key);
    var pctEl = document.getElementById('pct-' + key);
    var bar = document.getElementById('bar-' + key);
    var card = document.getElementById('card-' + key);

    if (!svc) {
      dot.className = 'sdot off';
      label.textContent = 'unavailable';
      pctEl.textContent = '--';
      bar.style.width = '0%';
      return;
    }

    var st = svc.status || 'offline';
    var pct = svc.uptime_pct || 0;
    dot.className = 'sdot ' + (st === 'online' ? 'on' : 'off');
    label.textContent = st;
    pctEl.textContent = pct.toFixed(1) + '%';
    bar.style.width = pct + '%';
    bar.className = 'srv-bar-fill ' + getBarColor(pct);

    if (key === 'socket' && svc.active_connections != null) {
      var conns = svc.active_connections;
      totalConns += conns;
      document.getElementById('socketUsers').textContent = conns;
    }
  });

  document.getElementById('usersOnline').textContent = totalConns;

  var mem = data.memory || {};
  var used = mem.used_mb || 0;
  var total = mem.total_mb || 0;
  var pct = total ? Math.round(used / total * 100) : 0;
  document.getElementById('memValue').textContent = used + '/' + total + 'MB';
  document.getElementById('memSub').textContent = used + 'MB used of ' + total + 'MB total';
  document.getElementById('memNums').textContent = used + ' / ' + total + ' MB';
  document.getElementById('memBar').style.width = pct + '%';

  // flash changed values
  if (prevData) {
    var flashEls = document.querySelectorAll('.stat-value, .mem-nums, .users-count');
    flashEls.forEach(function(el) {
      el.classList.remove('flash');
      void el.offsetWidth;
      el.classList.add('flash');
    });
  }
  prevData = data;
}

function fetchHealth() {
  fetch('/api/health')
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data.error) {
        document.getElementById('overallStatus').textContent = 'Error: ' + data.error;
        return;
      }
      updateUI(data);
    })
    .catch(function(err) {
      document.getElementById('overallStatus').textContent = 'Failed to connect';
    });
}

fetchHealth();
setInterval(fetchHealth, 10000);

function toggleTheme(cb) {
  var isDark = cb.checked;
  document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
  localStorage.setItem('starTheme', isDark ? 'dark' : 'light');
}

(function() {
  var saved = localStorage.getItem('starTheme') || 'light';
  if (saved === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
    var cb = document.getElementById('themeToggle');
    if (cb) cb.checked = true;
  }
})();
</script>
</body>
</html>"""


@app.route("/")
def index():
    return HTML, 200, {"Content-Type": "text/html; charset=utf-8"}


if __name__ == "__main__":
    print("StarVC Health Dashboard running at http://localhost:3000")
    app.run(host="0.0.0.0", port=3000, debug=False)