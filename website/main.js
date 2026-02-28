/* ═══════════════════════════════════════════════════════════════
   ESPORTS INTEGRITY COMMAND CENTER — Main JS
   Loads real pipeline data from data.json
   GSAP ScrollTrigger • Lenis Smooth Scroll • Canvas Scatter
   ═══════════════════════════════════════════════════════════════ */

let PLAYERS = [];

// ── LENIS SMOOTH SCROLL ───────────────────────────────────────
const lenis = new Lenis({
    duration: 1.4,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
});
function raf(time) { lenis.raf(time); requestAnimationFrame(raf); }
requestAnimationFrame(raf);

gsap.registerPlugin(ScrollTrigger);
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);

// ── LOAD DATA & INIT ──────────────────────────────────────────
window.addEventListener('load', () => {
    fetch('data.json')
        .then(r => r.json())
        .then(data => {
            PLAYERS = data;
            setTimeout(() => {
                document.getElementById('loader').classList.add('hidden');
                initAll();
            }, 600);
        })
        .catch(() => {
            document.getElementById('loader').classList.add('hidden');
            initAll();
        });
});

function initAll() {
    animateHero();
    populateMetrics();
    populateLiveStats();
    setupScrollAnimations();
    initScatter();
    populateLeaderboard();
    populateSuspects();
    populateRiskGrid();
    setupInteractions();
}

// ── CURSOR GLOW ───────────────────────────────────────────────
const glow = document.getElementById('cursorGlow');
let mx = 0, my = 0, gx = 0, gy = 0;
document.addEventListener('mousemove', (e) => { mx = e.clientX; my = e.clientY; });
(function tickGlow() {
    gx += (mx - gx) * 0.12;
    gy += (my - gy) * 0.12;
    glow.style.left = gx + 'px';
    glow.style.top = gy + 'px';
    requestAnimationFrame(tickGlow);
})();

// ── HERO ──────────────────────────────────────────────────────
function animateHero() {
    const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });
    tl.to('.hero-badge', { opacity: 1, y: 0, duration: 0.8 })
        .to('.hero-title', { opacity: 1, y: 0, duration: 1 }, '-=0.4')
        .to('.hero-sub', { opacity: 1, y: 0, duration: 0.8 }, '-=0.5')
        .to('.hero-cta', { opacity: 1, y: 0, duration: 0.7 }, '-=0.4')
        .to('#scrollHint', { opacity: 1, duration: 0.6 }, '-=0.2');
}

// ── METRICS ───────────────────────────────────────────────────
function populateMetrics() {
    const total = PLAYERS.length;
    const threats = PLAYERS.filter(p => p.suspicious).length;
    const cleanPct = ((total - threats) / total * 100).toFixed(1);
    const avgInt = (PLAYERS.reduce((s, p) => s + p.integrity, 0) / total).toFixed(2);

    animateValue('metTotal', total, 0);
    animateValue('metThreats', threats, 0);
    document.getElementById('metClean').textContent = cleanPct + '%';
    document.getElementById('metIntegrity').textContent = avgInt;
}

function animateValue(id, target, decimals) {
    const el = document.getElementById(id);
    gsap.to({ val: 0 }, {
        val: target, duration: 1.8, ease: 'power2.out',
        onUpdate: function () {
            el.textContent = decimals ? this.targets()[0].val.toFixed(decimals) : Math.round(this.targets()[0].val);
        },
    });
}

// ── LIVE STATS (from real data) ───────────────────────────────
function populateLiveStats() {
    const clean = PLAYERS.filter(p => !p.suspicious);
    const sus = PLAYERS.filter(p => p.suspicious);

    const avg = (arr, key) => arr.reduce((s, p) => s + p[key], 0) / arr.length;

    // KD
    const normKd = avg(clean, 'kd');
    const susKd = avg(sus, 'kd');
    const kdMax = Math.max(normKd, susKd);

    setLive('liveNormKd', normKd, null);
    setLive('liveSusKd', susKd, null);
    setBar('barNormKd', normKd / kdMax * 100);
    setBar('barSusKd', susKd / kdMax * 100);

    // Accuracy
    const normAcc = avg(clean, 'accuracy');
    const susAcc = avg(sus, 'accuracy');

    setLive('liveNormAcc', normAcc, '%');
    setLive('liveSusAcc', susAcc, '%');
    setBar('barNormAcc', normAcc);
    setBar('barSusAcc', susAcc);
}

function setLive(id, val, suffix) {
    const el = document.getElementById(id);
    if (!el) return;
    el.dataset.target = val.toFixed(1);
    if (suffix) el.dataset.suffix = suffix;
}

function setBar(id, width) {
    const el = document.getElementById(id);
    if (!el) return;
    el.dataset.width = Math.round(Math.min(100, width));
}

// ── SCROLL ANIMATIONS ─────────────────────────────────────────
function setupScrollAnimations() {
    // Parallax orbs
    document.querySelectorAll('.parallax-orb').forEach(orb => {
        gsap.to(orb, {
            y: () => window.innerHeight * parseFloat(orb.dataset.speed) * 3,
            ease: 'none',
            scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 1 },
        });
    });

    // Nav
    let lastScroll = 0;
    const nav = document.getElementById('nav');
    lenis.on('scroll', ({ scroll }) => {
        if (scroll > lastScroll && scroll > 150) nav.classList.add('hidden');
        else nav.classList.remove('hidden');
        lastScroll = scroll;
    });

    // Stat cards
    document.querySelectorAll('.stat-card').forEach((card, i) => {
        gsap.from(card, {
            opacity: 0, y: 60, scale: 0.92, duration: 0.8, delay: i * 0.1, ease: 'power3.out',
            scrollTrigger: { trigger: card, start: 'top 85%', toggleActions: 'play none none none' },
        });
    });

    // Stat bars
    document.querySelectorAll('.stat-bar-fill').forEach(bar => {
        ScrollTrigger.create({
            trigger: bar, start: 'top 85%',
            onEnter: () => { bar.style.width = bar.dataset.width + '%'; }, once: true,
        });
    });

    // Counters
    document.querySelectorAll('.counter').forEach(el => {
        const target = parseFloat(el.dataset.target);
        const suffix = el.dataset.suffix || '';
        const isFloat = target % 1 !== 0;
        ScrollTrigger.create({
            trigger: el, start: 'top 88%',
            onEnter: () => {
                gsap.to({ val: 0 }, {
                    val: target, duration: 1.8, ease: 'power2.out',
                    onUpdate: function () {
                        el.textContent = (isFloat ? this.targets()[0].val.toFixed(1) : Math.round(this.targets()[0].val)) + suffix;
                    },
                });
            }, once: true,
        });
    });

    // Risk cards
    document.querySelectorAll('.risk-card').forEach((card, i) => {
        gsap.from(card, {
            opacity: 0, y: 50, scale: 0.9, duration: 0.7, delay: i * 0.12, ease: 'power3.out',
            scrollTrigger: { trigger: card, start: 'top 85%', toggleActions: 'play none none none' },
        });
    });

    // Ring arcs
    document.querySelectorAll('.ring-arc').forEach(arc => {
        const full = parseFloat(arc.getAttribute('stroke-dasharray'));
        const target = parseFloat(arc.dataset.target);
        const offset = full - (target / full) * full;
        ScrollTrigger.create({
            trigger: arc, start: 'top 85%',
            onEnter: () => { gsap.to(arc, { attr: { 'stroke-dashoffset': offset }, duration: 1.5, ease: 'power2.out' }); },
            once: true,
        });
    });

    // CTA
    document.querySelectorAll('.cta-title .line span').forEach((span, i) => {
        gsap.from(span, {
            y: '110%', opacity: 0, duration: 1, delay: i * 0.2, ease: 'power4.out',
            scrollTrigger: { trigger: '.cta-section', start: 'top 70%', toggleActions: 'play none none none' },
        });
    });
    gsap.from('.cta-sub', { opacity: 0, y: 30, duration: 0.8, scrollTrigger: { trigger: '.cta-section', start: 'top 65%' } });
    gsap.from('.cta-btn', { opacity: 0, y: 30, scale: 0.9, duration: 0.7, scrollTrigger: { trigger: '.cta-section', start: 'top 60%' } });

    // Metrics banner cards
    document.querySelectorAll('.mbanner-card').forEach((card, i) => {
        gsap.from(card, {
            opacity: 0, y: 40, scale: 0.9, duration: 0.6, delay: i * 0.1, ease: 'power3.out',
            scrollTrigger: { trigger: card, start: 'top 90%', toggleActions: 'play none none none' },
        });
    });
}

// ═══════════════════════════════════════════════════════════════
// LEADERBOARD
// ═══════════════════════════════════════════════════════════════
function populateLeaderboard() {
    const sorted = [...PLAYERS].sort((a, b) => b.integrity - a.integrity);
    const tbody = document.getElementById('lbBody');
    tbody.innerHTML = '';

    sorted.forEach((p, i) => {
        const iColor = p.integrity > 0.7 ? 'var(--green)' : p.integrity > 0.4 ? 'var(--orange)' : 'var(--red)';
        const pct = Math.round(p.integrity * 100);
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="rank">${i + 1}</td>
            <td class="pid">${p.id}</td>
            <td class="integrity-cell" style="color:${iColor}">
                ${p.integrity.toFixed(4)}
                <span class="ibar-mini"><span class="ibar-mini-fill" style="width:${pct}%;background:${iColor};"></span></span>
            </td>
            <td>${p.anomaly.toFixed(4)}</td>
            <td>${p.kd.toFixed(2)}</td>
            <td>${p.accuracy.toFixed(1)}%</td>
            <td>${p.sessions}</td>
            <td class="${p.suspicious ? 'status-sus' : 'status-clean'}">${p.suspicious ? '🔴 Flagged' : '🟢 Clean'}</td>`;
        tbody.appendChild(tr);
    });

    // Animate table in
    gsap.from('.table-wrap', {
        opacity: 0, y: 40, duration: 0.8, ease: 'power3.out',
        scrollTrigger: { trigger: '.leaderboard-section', start: 'top 75%' },
    });
}

// ═══════════════════════════════════════════════════════════════
// SUSPICIOUS PLAYERS
// ═══════════════════════════════════════════════════════════════
function getRiskLevel(p) {
    if (p.confidence > 0.8) return 'high';
    if (p.confidence > 0.5) return 'mid';
    return 'low';
}

function getRiskBadge(level) {
    if (level === 'high') return '<span class="risk-badge high">🔴 High Risk</span>';
    if (level === 'mid') return '<span class="risk-badge mid">🟠 Medium Risk</span>';
    return '<span class="risk-badge low">🟢 Low Risk</span>';
}

function confRingSVG(val) {
    const sz = 50, sw = 4, r = (sz - sw) / 2;
    const c = 2 * Math.PI * r;
    const off = c * (1 - val);
    const col = val > 0.8 ? 'var(--red)' : val > 0.5 ? 'var(--orange)' : 'var(--green)';
    return `<div class="cring"><svg width="${sz}" height="${sz}">
      <circle cx="${sz / 2}" cy="${sz / 2}" r="${r}" fill="none" stroke="rgba(255,255,255,.07)" stroke-width="${sw}"/>
      <circle cx="${sz / 2}" cy="${sz / 2}" r="${r}" fill="none" stroke="${col}" stroke-width="${sw}"
        stroke-dasharray="${c.toFixed(1)}" stroke-dashoffset="${off.toFixed(1)}" stroke-linecap="round"/>
    </svg><span class="cring-lbl">${Math.round(val * 100)}%</span></div>`;
}

function populateSuspects(filter = 'all') {
    const suspects = PLAYERS.filter(p => p.suspicious);
    let filtered = suspects;
    if (filter === 'high') filtered = suspects.filter(p => getRiskLevel(p) === 'high');
    else if (filter === 'mid') filtered = suspects.filter(p => getRiskLevel(p) === 'mid');
    else if (filter === 'low') filtered = suspects.filter(p => getRiskLevel(p) === 'low');

    filtered.sort((a, b) => b.anomaly - a.anomaly);

    document.getElementById('filterCount').textContent = `${filtered.length} of ${suspects.length} flagged players`;

    const grid = document.getElementById('suspectsGrid');
    grid.innerHTML = '';

    filtered.forEach(p => {
        const level = getRiskLevel(p);
        const card = document.createElement('div');
        card.className = `suspect-card ${level}-risk`;
        card.innerHTML = `
            ${confRingSVG(p.confidence)}
            <div class="suspect-info">
                <div class="suspect-top">
                    <span class="suspect-id">${p.id}</span>
                    ${getRiskBadge(level)}
                </div>
                <div class="suspect-stats">
                    <span>K/D <b>${p.kd.toFixed(2)}</b></span>
                    <span>Acc <b>${p.accuracy.toFixed(1)}%</b></span>
                    <span>Kills <b>${p.kills}</b></span>
                    <span>Deaths <b>${p.deaths}</b></span>
                    <span>Sessions <b>${p.sessions}</b></span>
                </div>
            </div>
            <div class="suspect-anomaly">
                <div class="suspect-anomaly-label">ANOMALY</div>
                <div class="suspect-anomaly-val">${p.anomaly.toFixed(4)}</div>
            </div>`;
        grid.appendChild(card);
    });
}

// ═══════════════════════════════════════════════════════════════
// RISK GRID (dynamic from data)
// ═══════════════════════════════════════════════════════════════
function populateRiskGrid() {
    const tiers = [
        {
            key: 'elite', label: 'Stable', icon: '🔵', cls: 'stable', color: 'var(--blue)',
            desc: 'Integrity ≥ 0.85 — Consistent, normal gameplay.',
            filter: p => p.integrity >= 0.85
        },
        {
            key: 'skilled', label: 'Skilled', icon: '🟣', cls: 'skilled', color: 'var(--purple)',
            desc: 'Integrity 0.60–0.85 — High skill, plausible range.',
            filter: p => p.integrity >= 0.6 && p.integrity < 0.85
        },
        {
            key: 'risky', label: 'Risky', icon: '🟠', cls: 'risky', color: 'var(--orange)',
            desc: 'Integrity 0.35–0.60 — Elevated anomaly markers.',
            filter: p => p.integrity >= 0.35 && p.integrity < 0.6
        },
        {
            key: 'critical', label: 'Critical', icon: '🔴', cls: 'critical', color: 'var(--red)',
            desc: 'Integrity < 0.35 — Strong cheating indicators.',
            filter: p => p.integrity < 0.35
        },
    ];

    const grid = document.getElementById('riskGrid');
    grid.innerHTML = '';

    const total = PLAYERS.length;
    const circ = 2 * Math.PI * 42; // r=42

    tiers.forEach(t => {
        const count = PLAYERS.filter(t.filter).length;
        const pct = count / total;
        const offset = circ * (1 - pct);

        const card = document.createElement('div');
        card.className = `risk-card ${t.cls}`;
        card.setAttribute('data-anim', 'reveal');
        card.innerHTML = `
            <div class="ring-wrap">
                <svg width="90" height="90">
                    <circle cx="45" cy="45" r="38" fill="none" stroke="rgba(255,255,255,.06)" stroke-width="5"/>
                    <circle class="ring-arc" cx="45" cy="45" r="38" fill="none" stroke="${t.color}" stroke-width="5"
                        stroke-dasharray="${(2 * Math.PI * 38).toFixed(1)}" stroke-dashoffset="${(2 * Math.PI * 38).toFixed(1)}"
                        stroke-linecap="round" data-target="${(pct * (2 * Math.PI * 38)).toFixed(1)}"/>
                </svg>
                <span class="ring-value" style="color:${t.color};">${t.icon}</span>
            </div>
            <div class="risk-label" style="color:${t.color};">${t.label}</div>
            <div class="risk-desc">${t.desc}</div>
            <div class="risk-count">${count} players (${(pct * 100).toFixed(1)}%)</div>`;
        grid.appendChild(card);
    });
}

// ═══════════════════════════════════════════════════════════════
// INTERACTIVE CANVAS SCATTER PLOT
// ═══════════════════════════════════════════════════════════════
const canvas = document.getElementById('scatterCanvas');
const ctx = canvas.getContext('2d');
const tooltip = document.getElementById('scatterTooltip');
let cW, cH, dpr;
const PAD = { top: 40, right: 30, bottom: 50, left: 60 };
let scatterAnimProgress = 0;
let hoveredPlayer = null;
let animatedPoints = [];

function resizeCanvas() {
    const rect = canvas.parentElement.getBoundingClientRect();
    dpr = window.devicePixelRatio || 1;
    cW = rect.width - 3; // account for padding
    cH = rect.height || 500;
    canvas.width = cW * dpr;
    canvas.height = cH * dpr;
    canvas.style.width = cW + 'px';
    canvas.style.height = cH + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    buildPoints();
}

function buildPoints() {
    if (!PLAYERS.length) return;
    const xMax = Math.max(...PLAYERS.map(p => p.kd)) * 1.1 || 55;
    const yMin = Math.min(...PLAYERS.map(p => p.accuracy)) * 0.9 || 10;
    const yMax = Math.max(...PLAYERS.map(p => p.accuracy)) * 1.05 || 102;

    animatedPoints = PLAYERS.map(p => {
        const nx = p.kd / xMax;
        const ny = (p.accuracy - yMin) / (yMax - yMin);
        return {
            ...p,
            px: PAD.left + nx * (cW - PAD.left - PAD.right),
            py: cH - PAD.bottom - ny * (cH - PAD.top - PAD.bottom),
            radius: p.suspicious ? 6 : 4,
            currentRadius: 0,
            glowPhase: Math.random() * Math.PI * 2,
        };
    });
}

function initScatter() {
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    ScrollTrigger.create({
        trigger: '#scatter', start: 'top 70%',
        onEnter: () => {
            gsap.to({ val: 0 }, {
                val: 1, duration: 1.8, ease: 'power2.out',
                onUpdate: function () { scatterAnimProgress = this.targets()[0].val; },
            });
        }, once: true,
    });

    drawScatter();
}

function drawScatter() {
    ctx.clearRect(0, 0, cW, cH);

    // Grid
    ctx.strokeStyle = 'rgba(0,245,255,.06)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
        const x = PAD.left + (i / 5) * (cW - PAD.left - PAD.right);
        const y = PAD.top + (i / 5) * (cH - PAD.top - PAD.bottom);
        ctx.beginPath(); ctx.moveTo(x, PAD.top); ctx.lineTo(x, cH - PAD.bottom); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(PAD.left, y); ctx.lineTo(cW - PAD.right, y); ctx.stroke();
    }

    // Axis labels
    ctx.fillStyle = 'rgba(148,163,184,.5)';
    ctx.font = '11px "JetBrains Mono"';
    ctx.textAlign = 'center';
    ctx.fillText('Avg K/D Ratio →', cW / 2, cH - 8);
    ctx.save();
    ctx.translate(14, cH / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('Aim Accuracy (%) →', 0, 0);
    ctx.restore();

    // Points
    const t = scatterAnimProgress;
    animatedPoints.forEach(p => {
        const targetR = p === hoveredPlayer ? p.radius * 2.5 : p.radius;
        p.currentRadius += (targetR * t - p.currentRadius) * 0.15;
        if (p.currentRadius < 0.3) return;
        const r = p.currentRadius;

        if (p.suspicious) {
            p.glowPhase += 0.02;
            const gSize = 8 + Math.sin(p.glowPhase) * 4;
            ctx.beginPath();
            ctx.arc(p.px, p.py, r + gSize, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255,59,59,${0.06 + Math.sin(p.glowPhase) * 0.03})`;
            ctx.fill();
        }

        ctx.beginPath();
        ctx.arc(p.px, p.py, r, 0, Math.PI * 2);
        ctx.fillStyle = p.suspicious ? '#ff3b3b' : '#6366f1';
        ctx.globalAlpha = p === hoveredPlayer ? 1 : 0.8;
        ctx.fill();
        ctx.globalAlpha = 1;
        ctx.strokeStyle = p === hoveredPlayer
            ? (p.suspicious ? 'rgba(255,59,59,.6)' : 'rgba(99,102,241,.6)')
            : 'rgba(255,255,255,.1)';
        ctx.lineWidth = p === hoveredPlayer ? 2 : 0.5;
        ctx.stroke();
    });

    requestAnimationFrame(drawScatter);
}

// Scatter hover
canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    hoveredPlayer = null;
    for (const p of animatedPoints) {
        const dx = p.px - x, dy = p.py - y;
        if (dx * dx + dy * dy < (p.radius + 8) ** 2) { hoveredPlayer = p; break; }
    }

    if (hoveredPlayer) {
        const p = hoveredPlayer;
        document.getElementById('ttId').textContent = p.id;
        document.getElementById('ttKd').textContent = p.kd.toFixed(2);
        document.getElementById('ttAcc').textContent = p.accuracy.toFixed(1) + '%';
        document.getElementById('ttInt').textContent = p.integrity.toFixed(4);
        const st = document.getElementById('ttStatus');
        st.textContent = p.suspicious ? '🔴 Suspicious' : '🟢 Clean';
        st.style.color = p.suspicious ? '#ff3b3b' : '#10b981';

        let tx = e.clientX - rect.left + 16;
        let ty = e.clientY - rect.top - 10;
        if (tx + 200 > cW) tx -= 220;
        if (ty + 120 > cH) ty -= 130;
        tooltip.style.left = tx + 'px';
        tooltip.style.top = ty + 'px';
        tooltip.classList.add('visible');
        canvas.style.cursor = 'pointer';
    } else {
        tooltip.classList.remove('visible');
        canvas.style.cursor = 'crosshair';
    }
});
canvas.addEventListener('mouseleave', () => { hoveredPlayer = null; tooltip.classList.remove('visible'); });

// ═══════════════════════════════════════════════════════════════
// INTERACTIONS
// ═══════════════════════════════════════════════════════════════
function setupInteractions() {
    // Risk filter dropdown
    document.getElementById('riskFilter').addEventListener('change', (e) => {
        populateSuspects(e.target.value);
    });

    // Ripple on buttons
    document.querySelectorAll('.hero-cta, .cta-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            const rect = this.getBoundingClientRect();
            const rip = document.createElement('span');
            rip.className = 'ripple';
            const size = Math.max(rect.width, rect.height);
            rip.style.width = rip.style.height = size + 'px';
            rip.style.left = (e.clientX - rect.left - size / 2) + 'px';
            rip.style.top = (e.clientY - rect.top - size / 2) + 'px';
            this.appendChild(rip);
            rip.addEventListener('animationend', () => rip.remove());
        });
    });

    // Tilt on cards
    document.querySelectorAll('.stat-card, .risk-card, .mbanner-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            card.style.transform = `translateY(-6px) rotateX(${-y * 6}deg) rotateY(${x * 6}deg)`;
        });
        card.addEventListener('mouseleave', () => { card.style.transform = ''; });
    });

    // Smooth anchor scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(anchor.getAttribute('href'));
            if (target) lenis.scrollTo(target);
        });
    });
}
