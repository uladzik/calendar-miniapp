<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>CalendarBot</title>
  <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #f0f4f8;
      --bg2: #ffffff;
      --glass: rgba(255,255,255,0.8);
      --text: #1e293b;
      --text2: #64748b;
      --text3: #94a3b8;
      --accent: #6366f1;
      --accent2: #818cf8;
      --accent-soft: rgba(99,102,241,0.12);
      --success: #10b981;
      --warning: #f59e0b;
      --border: rgba(0,0,0,0.06);
      --shadow: 0 4px 24px rgba(0,0,0,0.06);
    }
    [data-theme="dark"] {
      --bg: #0f172a;
      --bg2: #1e293b;
      --glass: rgba(30,41,59,0.9);
      --text: #f1f5f9;
      --text2: #94a3b8;
      --text3: #64748b;
      --border: rgba(255,255,255,0.08);
      --shadow: 0 4px 24px rgba(0,0,0,0.3);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', -apple-system, sans-serif; -webkit-tap-highlight-color: transparent; }
    html, body { overflow-x: hidden; overscroll-behavior: none; }
    body { background: var(--bg); color: var(--text); min-height: 100vh; min-height: 100dvh; transition: background 0.3s, color 0.3s; }
    .app { max-width: 100%; min-height: 100vh; min-height: 100dvh; padding-bottom: 90px; }

    .header { padding: 16px 20px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; background: var(--bg); z-index: 10; }
    .logo { display: flex; align-items: center; gap: 10px; }
    .logo-icon { width: 42px; height: 42px; background: linear-gradient(135deg, var(--accent), var(--accent2)); border-radius: 14px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(99,102,241,0.3); }
    .logo-icon svg { width: 22px; height: 22px; color: #fff; }
    .logo-text { font-size: 20px; font-weight: 700; color: var(--text); }
    .header-btns { display: flex; gap: 8px; }
    .icon-btn { width: 42px; height: 42px; border-radius: 14px; border: none; background: var(--glass); color: var(--text2); cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: var(--shadow); }
    .icon-btn:active { transform: scale(0.95); }
    .icon-btn svg { width: 20px; height: 20px; }

    .stats { display: flex; gap: 10px; padding: 0 16px; margin-bottom: 20px; overflow-x: auto; scrollbar-width: none; }
    .stats::-webkit-scrollbar { display: none; }
    .stat { background: var(--glass); border-radius: 50px; padding: 10px 16px; display: flex; align-items: center; gap: 8px; white-space: nowrap; box-shadow: var(--shadow); flex-shrink: 0; border: 1px solid var(--border); }
    .stat-val { font-size: 16px; font-weight: 700; color: var(--text); }
    .stat-label { font-size: 13px; color: var(--text2); }

    .quick-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 0 16px; margin-bottom: 24px; }
    .quick-card { background: var(--glass); border-radius: 20px; padding: 18px; cursor: pointer; box-shadow: var(--shadow); border: 1px solid var(--border); }
    .quick-card:active { transform: scale(0.98); }
    .quick-icon { width: 48px; height: 48px; border-radius: 14px; display: flex; align-items: center; justify-content: center; margin-bottom: 12px; }
    .quick-icon svg { width: 24px; height: 24px; color: #fff; }
    .quick-icon.purple { background: linear-gradient(135deg, #6366f1, #818cf8); }
    .quick-icon.green { background: linear-gradient(135deg, #10b981, #34d399); }
    .quick-icon.blue { background: linear-gradient(135deg, #3b82f6, #60a5fa); }
    .quick-icon.orange { background: linear-gradient(135deg, #f59e0b, #fbbf24); }
    .quick-title { font-size: 15px; font-weight: 600; color: var(--text); }
    .quick-sub { font-size: 12px; color: var(--text3); margin-top: 2px; }

    .section { padding: 0 20px; margin-bottom: 14px; display: flex; align-items: center; justify-content: space-between; }
    .section-title { font-size: 18px; font-weight: 700; color: var(--text); }
    .section-link { font-size: 14px; font-weight: 600; color: var(--accent); background: none; border: none; cursor: pointer; }

    .event { background: var(--glass); border-radius: 18px; padding: 16px; margin: 0 16px 12px; display: flex; gap: 14px; box-shadow: var(--shadow); border: 1px solid var(--border); position: relative; overflow: hidden; }
    .event::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px; border-radius: 4px 0 0 4px; }
    .event.work::before { background: var(--accent); }
    .event.personal::before { background: var(--success); }
    .event.health::before { background: var(--warning); }
    .event.google::before { background: #4285f4; }
    .event-time { min-width: 54px; padding-right: 14px; border-right: 1px solid var(--border); display: flex; flex-direction: column; align-items: center; justify-content: center; }
    .event-hour { font-size: 16px; font-weight: 700; color: var(--text); }
    .event-ampm { font-size: 11px; color: var(--text3); }
    .event-info { flex: 1; }
    .event-title { font-size: 15px; font-weight: 600; color: var(--text); margin-bottom: 4px; }
    .event-meta { font-size: 12px; color: var(--text2); }
    .event-badge { display: inline-block; font-size: 10px; font-weight: 600; padding: 4px 8px; border-radius: 6px; margin-top: 8px; }
    .event-badge.google { background: rgba(66,133,244,0.12); color: #4285f4; }

    .empty { text-align: center; padding: 50px 30px; }
    .empty-icon { font-size: 56px; margin-bottom: 16px; }
    .empty-title { font-size: 18px; font-weight: 600; color: var(--text); margin-bottom: 6px; }
    .empty-text { font-size: 14px; color: var(--text3); }

    .fab { position: fixed; bottom: 100px; right: 20px; width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, var(--accent), var(--accent2)); border: none; color: #fff; cursor: pointer; box-shadow: 0 6px 20px rgba(99,102,241,0.4); display: flex; align-items: center; justify-content: center; z-index: 40; }
    .fab:active { transform: scale(0.95); }
    .fab svg { width: 28px; height: 28px; }

    .nav { position: fixed; bottom: 0; left: 0; right: 0; background: var(--glass); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-top: 1px solid var(--border); display: flex; justify-content: space-around; padding: 10px 0 28px; z-index: 50; }
    .nav-item { display: flex; flex-direction: column; align-items: center; gap: 4px; background: none; border: none; cursor: pointer; color: var(--text3); padding: 6px 20px; }
    .nav-item.active { color: var(--accent); }
    .nav-wrap { width: 48px; height: 30px; border-radius: 15px; display: flex; align-items: center; justify-content: center; }
    .nav-item.active .nav-wrap { background: var(--accent); }
    .nav-item.active .nav-wrap svg { color: #fff; }
    .nav-wrap svg { width: 22px; height: 22px; }
    .nav-label { font-size: 11px; font-weight: 600; }

    .screen { display: none; }
    .screen.active { display: block; }

    .modal { position: fixed; inset: 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(4px); z-index: 100; display: none; align-items: flex-end; }
    .modal.active { display: flex; }
    .modal-box { background: var(--bg2); border-radius: 28px 28px 0 0; width: 100%; max-height: 92vh; overflow-y: auto; animation: slideUp 0.3s ease; }
    @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
    .modal-handle { width: 40px; height: 5px; background: var(--border); border-radius: 5px; margin: 12px auto; }
    .modal-head { padding: 4px 20px 20px; display: flex; align-items: center; justify-content: space-between; }
    .modal-title { font-size: 20px; font-weight: 700; color: var(--text); }
    .modal-close { width: 36px; height: 36px; border-radius: 50%; background: var(--glass); border: none; font-size: 18px; cursor: pointer; color: var(--text2); }
    .modal-body { padding: 0 20px 36px; }

    .form-group { margin-bottom: 22px; }
    .form-label { font-size: 13px; font-weight: 600; color: var(--text2); margin-bottom: 10px; display: block; }
    .form-input { width: 100%; padding: 16px 18px; border-radius: 14px; border: 2px solid var(--border); background: var(--bg); font-size: 16px; color: var(--text); }
    .form-input:focus { outline: none; border-color: var(--accent); }

    .time-row { display: flex; gap: 12px; align-items: center; }
    .time-row select, .time-row input[type="number"] { flex: 1; padding: 16px; border-radius: 14px; border: 2px solid var(--border); background: var(--bg); font-size: 18px; font-weight: 600; color: var(--text); text-align: center; }
    .time-row select:focus, .time-row input:focus { outline: none; border-color: var(--accent); }
    .time-sep { font-size: 24px; font-weight: 700; color: var(--text); }
    input[type="number"]::-webkit-outer-spin-button, input[type="number"]::-webkit-inner-spin-button { -webkit-appearance: none; }
    input[type="number"] { -moz-appearance: textfield; }

    .chips { display: flex; gap: 10px; flex-wrap: wrap; }
    .chip { padding: 12px 18px; border-radius: 50px; border: 2px solid var(--border); background: var(--bg); font-size: 14px; font-weight: 600; color: var(--text); cursor: pointer; }
    .chip.active { background: var(--accent); border-color: var(--accent); color: #fff; }

    .toggle-row { display: flex; align-items: center; justify-content: space-between; padding: 16px 18px; background: var(--bg); border-radius: 14px; }
    .toggle-label { font-size: 15px; font-weight: 600; color: var(--text); }
    .toggle { width: 52px; height: 30px; border-radius: 30px; background: var(--border); border: none; cursor: pointer; position: relative; }
    .toggle::after { content: ''; position: absolute; top: 3px; left: 3px; width: 24px; height: 24px; border-radius: 50%; background: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: transform 0.2s; }
    .toggle.active { background: var(--accent); }
    .toggle.active::after { transform: translateX(22px); }

    .btn { width: 100%; padding: 18px; border-radius: 16px; border: none; background: linear-gradient(135deg, var(--accent), var(--accent2)); color: #fff; font-size: 16px; font-weight: 700; cursor: pointer; box-shadow: 0 6px 20px rgba(99,102,241,0.3); }
    .btn:active { transform: scale(0.98); }
    .btn:disabled { opacity: 0.6; }

    .cal-card { background: var(--glass); border-radius: 20px; padding: 18px; margin: 0 16px 20px; box-shadow: var(--shadow); border: 1px solid var(--border); }
    .cal-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; }
    .cal-title { font-size: 18px; font-weight: 700; color: var(--text); }
    .cal-nav { display: flex; gap: 8px; }
    .cal-nav button { width: 36px; height: 36px; border-radius: 12px; border: none; background: var(--bg); color: var(--text2); font-size: 16px; cursor: pointer; }
    .cal-week { display: grid; grid-template-columns: repeat(7, 1fr); margin-bottom: 10px; }
    .cal-week span { text-align: center; font-size: 12px; font-weight: 600; color: var(--text3); padding: 8px 0; }
    .cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; }
    .cal-day { aspect-ratio: 1; border-radius: 12px; border: none; background: transparent; font-size: 14px; font-weight: 500; color: var(--text); cursor: pointer; position: relative; }
    .cal-day.other { color: var(--text3); opacity: 0.4; }
    .cal-day.today { background: var(--accent-soft); color: var(--accent); font-weight: 700; }
    .cal-day.selected { background: var(--accent); color: #fff; }
    .cal-day.has::after { content: ''; position: absolute; bottom: 4px; left: 50%; transform: translateX(-50%); width: 5px; height: 5px; border-radius: 50%; background: var(--accent); }
    .cal-day.selected.has::after { background: #fff; }

    .settings-sec { margin: 0 16px 24px; }
    .settings-label { font-size: 12px; font-weight: 600; color: var(--text3); text-transform: uppercase; margin-bottom: 12px; padding-left: 4px; }
    .settings-card { background: var(--glass); border-radius: 18px; overflow: hidden; box-shadow: var(--shadow); border: 1px solid var(--border); }
    .settings-item { display: flex; align-items: center; justify-content: space-between; padding: 16px 18px; border-bottom: 1px solid var(--border); cursor: pointer; }
    .settings-item:last-child { border-bottom: none; }
    .settings-left { display: flex; align-items: center; gap: 14px; }
    .settings-icon { width: 40px; height: 40px; border-radius: 12px; background: var(--accent-soft); display: flex; align-items: center; justify-content: center; }
    .settings-icon svg { width: 20px; height: 20px; color: var(--accent); }
    .settings-name { font-size: 15px; font-weight: 500; color: var(--text); }
    .settings-val { font-size: 14px; color: var(--text3); }

    .toast { position: fixed; top: 70px; left: 50%; transform: translateX(-50%); background: var(--text); color: var(--bg); padding: 14px 24px; border-radius: 14px; font-size: 15px; font-weight: 500; z-index: 200; display: none; }
    .toast.show { display: block; animation: toastIn 0.3s ease; }
    @keyframes toastIn { from { opacity: 0; transform: translateX(-50%) translateY(-10px); } to { opacity: 1; transform: translateX(-50%) translateY(0); } }

    .loading { display: inline-block; width: 20px; height: 20px; border: 3px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: spin 0.8s linear infinite; }
    @keyframes spin { to { transform: rotate(360deg); } }
  </style>
</head>
<body data-theme="light">
<div id="toast" class="toast"></div>
<div class="app">
  <header class="header">
    <div class="logo">
      <div class="logo-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></div>
      <span class="logo-text">CalendarBot</span>
    </div>
    <div class="header-btns">
      <button class="icon-btn" onclick="syncGoogleEvents()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 4v6h-6M1 20v-6h6"/><path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15"/></svg></button>
      <button class="icon-btn" onclick="toggleTheme()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg></button>
    </div>
  </header>

  <section id="screen-home" class="screen active">
    <div class="stats">
      <div class="stat"><span class="stat-val" id="s-today">0</span><span class="stat-label">Today</span></div>
      <div class="stat"><span class="stat-val" id="s-week">0</span><span class="stat-label">This week</span></div>
      <div class="stat"><span class="stat-val" id="s-total">0</span><span class="stat-label">Total</span></div>
    </div>
    <div class="quick-grid">
      <div class="quick-card" onclick="openModal()">
        <div class="quick-icon purple"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></div>
        <div class="quick-title">New Event</div>
        <div class="quick-sub">Create quickly</div>
      </div>
      <div class="quick-card" onclick="goTo('calendar')">
        <div class="quick-icon green"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></div>
        <div class="quick-title">Calendar</div>
        <div class="quick-sub">View all dates</div>
      </div>
      <div class="quick-card" onclick="connectGoogle()">
        <div class="quick-icon blue"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg></div>
        <div class="quick-title">Google</div>
        <div class="quick-sub" id="g-status">Connect</div>
      </div>
      <div class="quick-card" onclick="goTo('settings')">
        <div class="quick-icon orange"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/></svg></div>
        <div class="quick-title">Settings</div>
        <div class="quick-sub">Customize</div>
      </div>
    </div>
    <div class="section"><h2 class="section-title">Upcoming</h2><button class="section-link" onclick="goTo('calendar')">See all →</button></div>
    <div id="events-list"></div>
  </section>

  <section id="screen-calendar" class="screen">
    <div class="cal-card">
      <div class="cal-head"><h2 class="cal-title" id="cal-month">March 2026</h2><div class="cal-nav"><button onclick="prevMonth()">←</button><button onclick="nextMonth()">→</button></div></div>
      <div class="cal-week"><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span></div>
      <div class="cal-grid" id="cal-grid"></div>
    </div>
    <div class="section"><h2 class="section-title" id="sel-date-title">Today</h2></div>
    <div id="cal-events"></div>
  </section>

  <section id="screen-settings" class="screen">
    <div class="settings-sec">
      <div class="settings-label">Appearance</div>
      <div class="settings-card">
        <div class="settings-item" onclick="toggleTheme()">
          <div class="settings-left"><div class="settings-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg></div><span class="settings-name">Dark Mode</span></div>
          <button class="toggle" id="theme-toggle"></button>
        </div>
      </div>
    </div>
    <div class="settings-sec">
      <div class="settings-label">Integrations</div>
      <div class="settings-card">
        <div class="settings-item" onclick="connectGoogle()">
          <div class="settings-left"><div class="settings-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></div><span class="settings-name">Google Calendar</span></div>
          <span class="settings-val" id="g-status2">Connect →</span>
        </div>
      </div>
    </div>
  </section>

  <button class="fab" onclick="openModal()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button>

  <nav class="nav">
    <button class="nav-item active" onclick="goTo('home')" data-s="home"><div class="nav-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></div><span class="nav-label">Home</span></button>
    <button class="nav-item" onclick="goTo('calendar')" data-s="calendar"><div class="nav-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></div><span class="nav-label">Calendar</span></button>
    <button class="nav-item" onclick="goTo('settings')" data-s="settings"><div class="nav-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/></svg></div><span class="nav-label">Settings</span></button>
  </nav>
</div>

<div class="modal" id="modal" onclick="if(event.target===this)closeModal()">
  <div class="modal-box">
    <div class="modal-handle"></div>
    <div class="modal-head"><h2 class="modal-title">New Event</h2><button class="modal-close" onclick="closeModal()">✕</button></div>
    <div class="modal-body">
      <div class="form-group"><label class="form-label">Title</label><input type="text" class="form-input" id="e-title" placeholder="What's happening?"></div>
      <div class="form-group"><label class="form-label">Category</label><div class="chips" id="cats"><button class="chip active" data-c="work">💼 Work</button><button class="chip" data-c="personal">👤 Personal</button><button class="chip" data-c="health">💪 Health</button></div></div>
      <div class="form-group"><label class="form-label">Date</label><input type="date" class="form-input" id="e-date"></div>
      <div class="form-group"><label class="form-label">Time</label><div class="time-row"><select id="e-hour"></select><span class="time-sep">:</span><input type="number" id="e-min" min="0" max="59" value="0" placeholder="00"></div></div>
      <div class="form-group"><label class="form-label">Duration</label><div class="chips" id="durs"><button class="chip" data-d="15">15m</button><button class="chip active" data-d="30">30m</button><button class="chip" data-d="60">1h</button><button class="chip" data-d="120">2h</button></div></div>
      <div class="form-group"><div class="toggle-row"><span class="toggle-label">🔔 Reminder</span><button class="toggle active" id="e-reminder"></button></div></div>
      <button class="btn" id="create-btn" onclick="saveEvent()">Create Event</button>
    </div>
  </div>
</div>

<script>
const API_URL = 'https://calendar-miniapp.onrender.com';
let events = [], googleEvents = [], curMonth = new Date(), selDate = new Date(), selCat = 'work', selDur = 30;
const tg = window.Telegram?.WebApp;
if (tg) { tg.expand(); tg.ready(); if (tg.colorScheme === 'dark') setTheme('dark'); }

document.addEventListener('DOMContentLoaded', () => { loadEvents(); initHours(); initPickers(); renderAll(); checkGoogle(); loadTheme(); });

function setTheme(t) { document.body.setAttribute('data-theme', t); document.getElementById('theme-toggle')?.classList.toggle('active', t === 'dark'); localStorage.setItem('theme', t); }
function toggleTheme() { setTheme(document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'); }
function loadTheme() { const t = localStorage.getItem('theme'); if (t) setTheme(t); }

function toast(m) { const t = document.getElementById('toast'); t.textContent = m; t.classList.add('show'); setTimeout(() => t.classList.remove('show'), 2500); }
function goTo(s) { document.querySelectorAll('.screen').forEach(x => x.classList.remove('active')); document.getElementById('screen-' + s).classList.add('active'); document.querySelectorAll('.nav-item').forEach(n => n.classList.toggle('active', n.dataset.s === s)); if (s === 'calendar') { renderCal(); renderCalEvents(); } }

function loadEvents() { try { events = JSON.parse(localStorage.getItem('events') || '[]'); } catch { events = []; } }
function saveEventsLocal() { localStorage.setItem('events', JSON.stringify(events)); }
function getUserId() { if (tg?.initDataUnsafe?.user) return String(tg.initDataUnsafe.user.id); let id = localStorage.getItem('uid'); if (!id) { id = 'w_' + Date.now(); localStorage.setItem('uid', id); } return id; }

function initHours() { const s = document.getElementById('e-hour'); for (let i = 0; i < 24; i++) { const o = document.createElement('option'); o.value = i; o.textContent = i.toString().padStart(2, '0'); s.appendChild(o); } }
function initPickers() {
  document.getElementById('cats').onclick = e => { const b = e.target.closest('.chip'); if (b) { document.querySelectorAll('#cats .chip').forEach(x => x.classList.remove('active')); b.classList.add('active'); selCat = b.dataset.c; } };
  document.getElementById('durs').onclick = e => { const b = e.target.closest('.chip'); if (b) { document.querySelectorAll('#durs .chip').forEach(x => x.classList.remove('active')); b.classList.add('active'); selDur = +b.dataset.d; } };
  document.querySelectorAll('.toggle').forEach(t => { t.onclick = e => { e.stopPropagation(); t.classList.toggle('active'); }; });
}

function openModal() { document.getElementById('modal').classList.add('active'); const today = new Date(); document.getElementById('e-date').valueAsDate = selDate; document.getElementById('e-date').min = today.toISOString().split('T')[0]; document.getElementById('e-hour').value = today.getHours(); document.getElementById('e-min').value = 0; document.getElementById('e-title').value = ''; }
function closeModal() { document.getElementById('modal').classList.remove('active'); }

async function saveEvent() {
  const title = document.getElementById('e-title').value.trim() || 'Untitled';
  const date = document.getElementById('e-date').value;
  const hour = document.getElementById('e-hour').value;
  const min = document.getElementById('e-min').value || 0;
  const reminder = document.getElementById('e-reminder').classList.contains('active');
  if (!date) { toast('Please select a date'); return; }
  const btn = document.getElementById('create-btn'); btn.disabled = true; btn.innerHTML = '<span class="loading"></span>';
  const dt = `${date}T${hour.toString().padStart(2,'0')}:${min.toString().padStart(2,'0')}:00`;
  const ev = { id: Date.now(), title, datetime: dt, category: selCat, duration: selDur, reminder };
  events.push(ev); saveEventsLocal();
  if (localStorage.getItem('g_con') === 'true') {
    try {
      const res = await fetch(`${API_URL}/create_event`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ user_id: getUserId(), title: ev.title, datetime: ev.datetime, duration: ev.duration }) });
      const data = await res.json();
      if (data.success) toast('✅ Added to Google Calendar!');
      else if (res.status === 401) { localStorage.removeItem('g_con'); checkGoogle(); toast('Please reconnect Google'); }
    } catch (e) { console.error(e); }
  } else { toast('✅ Event created!'); }
  btn.disabled = false; btn.textContent = 'Create Event'; closeModal(); renderAll();
}

function renderAll() { renderEvents(); renderCal(); updateStats(); }
function renderEvents() {
  const c = document.getElementById('events-list'), now = new Date(), all = [...events, ...googleEvents];
  const up = all.filter(e => new Date(e.datetime) >= now).sort((a, b) => new Date(a.datetime) - new Date(b.datetime)).slice(0, 5);
  if (!up.length) { c.innerHTML = '<div class="empty"><div class="empty-icon">📅</div><div class="empty-title">No upcoming events</div><div class="empty-text">Tap + to create one</div></div>'; return; }
  c.innerHTML = up.map(e => evCard(e)).join('');
}
function evCard(e) {
  const d = new Date(e.datetime), h = d.getHours(), m = d.getMinutes().toString().padStart(2, '0'), ap = h >= 12 ? 'PM' : 'AM', h12 = h % 12 || 12;
  const cat = e.category || (e.isGoogle ? 'google' : 'work'), badge = e.isGoogle ? '<span class="event-badge google">📅 Google</span>' : '';
  return `<div class="event ${cat}"><div class="event-time"><span class="event-hour">${h12}:${m}</span><span class="event-ampm">${ap}</span></div><div class="event-info"><div class="event-title">${e.title}</div><div class="event-meta">${e.duration || 30} min · ${d.toLocaleDateString()}</div>${badge}</div></div>`;
}

function renderCal() {
  const y = curMonth.getFullYear(), mo = curMonth.getMonth(), names = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  document.getElementById('cal-month').textContent = `${names[mo]} ${y}`;
  const g = document.getElementById('cal-grid'); g.innerHTML = '';
  const first = new Date(y, mo, 1), last = new Date(y, mo + 1, 0), today = new Date(); today.setHours(0,0,0,0);
  let start = first.getDay() - 1; if (start < 0) start = 6;
  const prevLast = new Date(y, mo, 0).getDate(), allEvents = [...events, ...googleEvents];
  for (let i = start - 1; i >= 0; i--) { const b = document.createElement('button'); b.className = 'cal-day other'; b.textContent = prevLast - i; g.appendChild(b); }
  for (let d = 1; d <= last.getDate(); d++) {
    const b = document.createElement('button'), cell = new Date(y, mo, d); b.className = 'cal-day'; b.textContent = d;
    if (cell.toDateString() === today.toDateString()) b.classList.add('today');
    if (cell.toDateString() === selDate.toDateString()) b.classList.add('selected');
    const ds = cell.toISOString().split('T')[0]; if (allEvents.some(e => e.datetime && e.datetime.startsWith(ds))) b.classList.add('has');
    b.onclick = () => { selDate = cell; renderCal(); renderCalEvents(); document.getElementById('sel-date-title').textContent = cell.toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' }); };
    g.appendChild(b);
  }
  const total = g.children.length; for (let i = 1; total + i <= 42; i++) { const b = document.createElement('button'); b.className = 'cal-day other'; b.textContent = i; g.appendChild(b); }
}
function prevMonth() { curMonth.setMonth(curMonth.getMonth() - 1); renderCal(); }
function nextMonth() { curMonth.setMonth(curMonth.getMonth() + 1); renderCal(); }
function renderCalEvents() {
  const c = document.getElementById('cal-events'), ds = selDate.toISOString().split('T')[0], all = [...events, ...googleEvents];
  const day = all.filter(e => e.datetime && e.datetime.startsWith(ds)).sort((a, b) => new Date(a.datetime) - new Date(b.datetime));
  if (!day.length) { c.innerHTML = '<div class="empty"><div class="empty-icon">📭</div><div class="empty-title">No events</div><div class="empty-text">Nothing scheduled</div></div>'; return; }
  c.innerHTML = day.map(e => evCard(e)).join('');
}

function updateStats() {
  const now = new Date(), td = now.toISOString().split('T')[0], wk = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000), all = [...events, ...googleEvents];
  document.getElementById('s-today').textContent = all.filter(e => e.datetime && e.datetime.startsWith(td)).length;
  document.getElementById('s-week').textContent = all.filter(e => { const d = new Date(e.datetime); return d >= now && d <= wk; }).length;
  document.getElementById('s-total').textContent = all.length;
}

function checkGoogle() { const c = localStorage.getItem('g_con') === 'true'; document.getElementById('g-status').textContent = c ? 'Connected ✓' : 'Connect'; document.getElementById('g-status2').textContent = c ? 'Connected ✓' : 'Connect →'; }
function connectGoogle() { const u = getUserId(), url = `${API_URL}/auth/google?user_id=${u}&chat_id=${u}`; if (tg) tg.openLink(url); else window.open(url, '_blank'); localStorage.setItem('g_con', 'true'); checkGoogle(); toast('Connecting...'); }
async function syncGoogleEvents() {
  if (localStorage.getItem('g_con') !== 'true') { toast('Connect Google first'); return; }
  toast('Syncing...');
  try {
    const res = await fetch(`${API_URL}/get_events?user_id=${getUserId()}`);
    const data = await res.json();
    if (res.status === 401) { localStorage.removeItem('g_con'); checkGoogle(); googleEvents = []; toast('Please reconnect Google'); }
    else if (data.events) { googleEvents = data.events.map(e => ({ id: e.id, title: e.summary || 'No title', datetime: e.start?.dateTime || e.start?.date, duration: calcDur(e.start, e.end), isGoogle: true })); toast(`✅ Synced ${googleEvents.length} events`); }
  } catch (e) { console.error(e); toast('Sync failed'); }
  renderAll();
}
function calcDur(s, e) { if (!s?.dateTime || !e?.dateTime) return 60; return Math.round((new Date(e.dateTime) - new Date(s.dateTime)) / 60000); }
if (localStorage.getItem('g_con') === 'true') setTimeout(syncGoogleEvents, 1500);
</script>
</body>
</html>
