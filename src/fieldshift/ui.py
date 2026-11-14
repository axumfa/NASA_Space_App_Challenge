"""Field Shift design system: CSS tokens + small HTML components used by app.py.

Everything visual lives here (colours, type, spacing, cards, KPI tiles, comparison table). No text is hard-coded: callers pass
already-translated strings. All strings are HTML-escaped here unless a parameter is documented as markup.
"""
from __future__ import annotations

from html import escape as esc

import streamlit as st

LOGO_SVG = ('<svg viewBox="0 0 32 32" width="30" height="30" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            '<rect width="32" height="32" rx="8" fill="#2F6B45"/>'
            '<path d="M6 12.5 L26 7.5" stroke="#CFE0C8" stroke-width="3" stroke-linecap="round"/>'
            '<path d="M6 19 L26 14" stroke="#EAF1E4" stroke-width="3" stroke-linecap="round"/>'
            '<path d="M6 25.5 L26 20.5" stroke="#B9C48A" stroke-width="3" stroke-linecap="round"/></svg>')

# faint contour lines for the hero panel (decorative)
_CONTOUR = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='420' height='200' viewBox='0 0 420 200' fill='none' "
            "stroke='%232F6B45' stroke-opacity='0.13' stroke-width='1.2'><path d='M0 150C80 120 130 170 210 140S350 90 420 120'/>"
            "<path d='M0 120C80 90 130 140 210 110S350 60 420 90'/><path d='M0 90C80 60 130 110 210 80S350 30 420 60'/>"
            "<path d='M0 60C80 30 130 80 210 50S350 0 420 30'/><path d='M0 180C80 150 130 200 210 170S350 120 420 150'/></svg>")

CSS = """
<style>
:root{
  --fs-forest:#2F6B45; --fs-forest-d:#234E35; --fs-sage:#8FA68A; --fs-sage-l:#E8EEE2; --fs-olive:#6B7248;
  --fs-bg:#FAF8F3; --fs-surface:#FFFFFF; --fs-ink:#232623; --fs-muted:#6B6F66; --fs-border:#E3DFD3; --fs-amber:#B9731F;
  --fs-font: Inter, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;

  /* Kinetics Spring-Physics Linear Easing Curves */
  --spring-snappy: linear(
    0, 0.009, 0.035 2.1%, 0.141, 0.281 6.7%, 0.723 12.9%, 0.938 16.7%, 
    1.017, 1.049 21.6%, 1.054 23.9%, 1.038, 1.018 30.5%, 0.999 35.8%, 
    0.995 40%, 1 50%
  );
  --spring-bouncy: linear(
    0, 0.006, 0.025 2.8%, 0.101 6.1%, 0.539 18.9%, 0.721 25.3%, 0.849 31.6%, 
    1.042 42.5%, 1.069 47.2%, 1.066 52.8%, 0.989 68.3%, 0.985 75.5%, 1 90%
  );
  --spring-gentle: linear(
    0, 0.004, 0.016, 0.035, 0.063, 0.098, 0.141 6.8%, 0.441 16.2%, 
    0.72 25.6%, 0.904 36.1%, 0.968 44.5%, 0.993 54.4%, 1 65%
  );
  --spring-elastic: linear(
    0, 0.009, 0.037 2.3%, 0.148 5.7%, 0.738 15.6%, 0.978 20.7%, 
    1.062 25.3%, 1.077 28.2%, 1.067 31.3%, 1.012 40.5%, 0.994 48.9%, 1 65%
  );
}
html, body, .stApp, [class*="css"]{font-family:var(--fs-font); color:var(--fs-ink);}
.stApp{background:var(--fs-bg);}
#MainMenu, footer, [data-testid="stDecoration"], [data-testid="stStatusWidget"], [data-testid="stToolbarActions"]{visibility:hidden; height:0; display:none !important;}
[data-testid="stToolbar"]{background:transparent !important; height:2.5rem !important;}
[data-testid="stExpandSidebarButton"]{visibility:visible !important; display:inline-flex !important; pointer-events:auto !important; z-index:1000001 !important; cursor:pointer !important;}
header[data-testid="stHeader"]{background:transparent; pointer-events:none;}
header[data-testid="stHeader"] button, header[data-testid="stHeader"] a{pointer-events:auto;}
.block-container{max-width:min(1640px, 96vw); padding:1.1rem 2rem 3.5rem;}
h1,h2,h3,h4{color:var(--fs-ink); letter-spacing:-0.01em; font-weight:650;}
[data-testid="stMarkdownContainer"] h2, h2{font-size:1.2rem !important; margin:2.1rem 0 .15rem !important; padding:0 !important; font-weight:650 !important;}
h3{font-size:1.05rem;} [data-testid="stMarkdownContainer"] h4{font-size:1rem !important;}
p, li, label, .stMarkdown{font-size:15px;}
[data-testid="stCaptionContainer"]{color:var(--fs-muted);}
section[data-testid="stSidebar"]{background:#F3F1E8; border-right:1px solid var(--fs-border);}
section[data-testid="stSidebar"] .block-container{padding-top:1.2rem;}
section[data-testid="stSidebar"][aria-expanded="true"], section[data-testid="stSidebar"][data-collapsed="false"]{min-width:340px; max-width:340px;}
.fs-rotprev{display:flex; flex-wrap:wrap; align-items:center; gap:.3rem; margin:.1rem 0 .7rem;}
.fs-rotprev span.c{
  background:var(--fs-sage-l); border:1px solid #D3DDC9; color:var(--fs-forest-d); border-radius:6px;
  padding:.12rem .55rem; font-size:.82rem; font-weight:600; display:inline-block;
  transition:transform 350ms var(--spring-bouncy), background-color 200ms ease, box-shadow 350ms var(--spring-bouncy);
  will-change:transform; cursor:default;
}
.fs-rotprev span.c:hover{transform:translateY(-1.5px) scale(1.04); background:#DDE8D4; box-shadow:0 3px 8px rgba(47,107,69,.16);}
.fs-rotprev span.c:active{transform:scale(0.96); transition-duration:100ms;}
.fs-rotprev span.a{color:var(--fs-muted); display:inline-block; transition:transform 350ms var(--spring-snappy);}
.fs-rotprev:hover span.a{transform:translateX(1.5px);}
.fs-grp{font-size:.74rem; font-weight:650; color:var(--fs-olive); margin:.5rem 0 .1rem; text-transform:uppercase; letter-spacing:.06em;}
.st-key-sidecrops{
  background:#fff; border:1px solid var(--fs-border) !important; border-radius:10px; padding:.6rem .7rem .6rem;
  transition:transform 450ms var(--spring-gentle), box-shadow 450ms var(--spring-gentle);
}
.st-key-sidecrops:hover{box-shadow:0 4px 14px rgba(0,0,0,.05);}
.fs-side-h{font-size:.72rem; text-transform:uppercase; letter-spacing:.08em; color:var(--fs-muted); font-weight:650; margin:1.1rem 0 .35rem;}

/* ---------- header & brand ---------- */
.fs-brand{display:flex; align-items:center; gap:.65rem; padding:.2rem 0; cursor:default;}
.fs-brand svg{transition:transform 500ms var(--spring-bouncy); will-change:transform;}
.fs-brand:hover svg{transform:rotate(-5deg) scale(1.08);}
.fs-brand b{font-size:1.15rem; letter-spacing:-0.02em; font-weight:700; display:block; line-height:1.1;}
.fs-brand span{font-size:.74rem; color:var(--fs-muted); display:block; line-height:1.2;}
.st-key-nav [role="radiogroup"], .st-key-langbox [role="radiogroup"]{gap:.2rem; flex-wrap:wrap;}
.st-key-nav label[data-testid="stRadioOption"], .st-key-langbox label[data-testid="stRadioOption"]{
  margin:0; padding:.38rem .85rem; border-radius:8px; cursor:pointer; border:1px solid transparent; background:transparent;
  transition:transform 380ms var(--spring-snappy), background-color 200ms ease, border-color 200ms ease, box-shadow 380ms var(--spring-snappy), color 180ms ease;
  will-change:transform;
}
.st-key-nav label[data-testid="stRadioOption"] > div > div:first-child, .st-key-langbox label[data-testid="stRadioOption"] > div > div:first-child{display:none;}
.st-key-nav label[data-testid="stRadioOption"] p, .st-key-langbox label[data-testid="stRadioOption"] p{font-size:.9rem; font-weight:550; color:var(--fs-muted); transition:color 180ms ease;}
.st-key-nav label[data-testid="stRadioOption"]:hover, .st-key-langbox label[data-testid="stRadioOption"]:hover{background:#EFECE2; transform:translateY(-1.5px);}
.st-key-nav label[data-testid="stRadioOption"]:active, .st-key-langbox label[data-testid="stRadioOption"]:active{transform:scale(0.96); transition-duration:120ms;}
.st-key-nav label[data-testid="stRadioOption"][data-selected="true"]{background:var(--fs-sage-l); border-color:#D3DDC9; box-shadow:0 2px 8px rgba(47,107,69,.12); transform:translateY(-1px);}
.st-key-nav label[data-testid="stRadioOption"][data-selected="true"]:hover{transform:translateY(-1.5px);}
.st-key-nav label[data-testid="stRadioOption"][data-selected="true"] p{color:var(--fs-forest-d);}
.st-key-langbox [role="radiogroup"]{background:#EFECE2; border-radius:9px; padding:3px; display:inline-flex; gap:2px; float:right;}
.st-key-langbox label[data-testid="stRadioOption"]{padding:.25rem .7rem; transition:transform 350ms var(--spring-snappy), background-color 180ms ease, box-shadow 350ms var(--spring-snappy), color 180ms ease;}
.st-key-langbox label[data-testid="stRadioOption"]:hover{transform:translateY(-1px);}
.st-key-langbox label[data-testid="stRadioOption"]:active{transform:scale(0.94); transition-duration:120ms;}
.st-key-langbox label[data-testid="stRadioOption"][data-selected="true"]{background:#fff; border-color:var(--fs-border); box-shadow:0 2px 6px rgba(0,0,0,.06); transform:scale(1.02);}
.st-key-langbox label[data-testid="stRadioOption"][data-selected="true"] p{color:var(--fs-ink);}
.st-key-langbox [data-testid="stWidgetLabel"]{display:none;}
.fs-lyrs{display:flex; flex-wrap:wrap; gap:.25rem .9rem; font-size:.78rem; color:var(--fs-muted); margin:.15rem 0 0;}
.fs-lyrs .h{text-transform:uppercase; letter-spacing:.06em; font-weight:650; font-size:.7rem;}
.fs-lyr b{color:var(--fs-ink); font-weight:600;} .fs-lyr.off{color:#8A5313;}
.fs-rule{height:1px; background:var(--fs-border); margin:.5rem 0 .9rem;}
.fs-notice{font-size:.82rem; color:var(--fs-muted); display:flex; gap:.5rem; align-items:center; margin:.1rem 0 .6rem;}
.fs-notice i{
  width:7px; height:7px; border-radius:50%; background:var(--fs-amber); display:inline-block; flex:none;
  animation:kinetics-breathe 2.4s var(--spring-gentle) infinite alternate; will-change:transform, opacity;
}

/* ---------- panels (bordered containers whose key starts with panel) ---------- */
[class*="st-key-panel"]{
  background:var(--fs-surface); border:1px solid var(--fs-border) !important; border-radius:10px; padding:.5rem .75rem;
  height:auto !important; min-height:fit-content; box-sizing:border-box;
  transition:transform 450ms var(--spring-gentle), box-shadow 450ms var(--spring-gentle), border-color 250ms ease;
}
.st-key-panel_map{padding:.5rem .75rem 1.1rem !important;}
.st-key-panel_map [data-testid="stMarkdownContainer"]{margin-bottom:0 !important;}
[class*="st-key-panel_card"], .st-key-panel_cardtop{will-change:transform, box-shadow; cursor:default;}
[class*="st-key-panel_card"]:hover, .st-key-panel_cardtop:hover{
  transform:translateY(-3px); box-shadow:0 10px 24px rgba(47,107,69,.08);
}
.st-key-panel_summary{border-left:4px solid var(--fs-forest) !important; transition:transform 450ms var(--spring-gentle), box-shadow 450ms var(--spring-gentle);}
.st-key-panel_summary:hover{transform:translateY(-2px); box-shadow:0 6px 20px rgba(0,0,0,.05);}
.st-key-panel_next{padding:.8rem 1.2rem !important;}
.st-key-panel_next [data-testid="stMarkdownContainer"]{margin-bottom:0 !important;}
.st-key-panel_next [data-testid="stColumn"]{min-width:0 !important;}
.st-key-panel_next .stButton > button{width:100% !important; max-width:100% !important; white-space:normal !important; word-break:break-word !important;}
[class*="st-key-bar"]{
  background:var(--fs-surface); border:1px solid var(--fs-border) !important; border-radius:10px; padding:.6rem 1rem;
  height:auto !important; min-height:fit-content; box-sizing:border-box;
  transition:box-shadow 400ms var(--spring-gentle), border-color 250ms ease;
}
.st-key-bar_field [data-testid="stColumn"]{min-width:0 !important;}
.st-key-bar_field [data-testid="stNumberInputContainer"]{min-width:0 !important;}
[class*="st-key-bar"]:focus-within{border-color:#D3DDC9 !important; box-shadow:0 4px 16px rgba(0,0,0,.04);}

/* ---------- hero (selected field) ---------- */
.st-key-hero{
  background:var(--fs-sage-l) url("%CONTOUR%") right bottom/auto 70% no-repeat; border:1px solid #D3DDC9 !important;
  border-radius:12px; padding:1.1rem 1.4rem 1rem; margin:.3rem 0 .4rem;
  transition:transform 450ms var(--spring-gentle), box-shadow 450ms var(--spring-gentle);
}
.st-key-hero:hover{box-shadow:0 8px 24px rgba(47,107,69,.08);}
.fs-eyebrow{font-size:.72rem; text-transform:uppercase; letter-spacing:.09em; color:var(--fs-forest); font-weight:700;}
.fs-hero h1{font-size:1.75rem; margin:.1rem 0 .45rem; line-height:1.15;}
.fs-meta{display:flex; flex-wrap:wrap; gap:.4rem .5rem; align-items:center; margin-bottom:.55rem;}
.fs-coord{
  display:inline-flex; align-items:center; gap:.35rem; background:#fff; border:1px solid #D3DDC9; border-radius:7px;
  padding:.14rem .6rem; font-size:.84rem; font-weight:600; font-variant-numeric:tabular-nums;
  transition:transform 350ms var(--spring-snappy), box-shadow 350ms var(--spring-snappy), border-color 200ms ease;
  will-change:transform;
}
.fs-coord:hover{transform:translateY(-1.5px); box-shadow:0 3px 10px rgba(0,0,0,.06); border-color:var(--fs-forest);}
.fs-coord svg{width:12px; height:12px; flex:none; transition:transform 400ms var(--spring-bouncy);}
.fs-coord:hover svg{transform:rotate(-8deg) scale(1.15);}
.fs-meta .lbl{font-size:.78rem; color:var(--fs-muted); margin-left:.3rem;}
.fs-hero p.lead{max-width:600px; font-size:.97rem; color:#3B3F39; margin:.2rem 0 .3rem;}

/* ---------- data availability ---------- */
.fs-data{background:rgba(255,255,255,.72); border:1px solid #D3DDC9; border-radius:10px; padding:.7rem .9rem .6rem; backdrop-filter:blur(2px); transition:box-shadow 400ms var(--spring-gentle);}
.fs-data:hover{box-shadow:0 4px 14px rgba(0,0,0,.04);}
.fs-data h4{padding:0 !important; line-height:1.2 !important; font-size:.72rem !important; text-transform:uppercase; letter-spacing:.08em; color:var(--fs-muted); margin:0 0 .35rem !important; font-weight:650;}
.fs-dr{
  display:flex; align-items:center; gap:.55rem; padding:.28rem .35rem; border-top:1px solid #E8E5DA; font-size:.85rem;
  transition:transform 320ms var(--spring-snappy), background-color 200ms ease; will-change:transform; border-radius:6px;
}
.fs-dr:first-of-type{border-top:none;}
.fs-dr:hover{transform:translateX(4px); background-color:rgba(239,236,226,.45);}
.fs-dr .dot{width:9px; height:9px; border-radius:50%; flex:none; transition:transform 400ms var(--spring-bouncy); will-change:transform;}
.fs-dr:hover .dot{transform:scale(1.35);}
.fs-dr.ok .dot{background:var(--fs-forest);}
.fs-dr.miss .dot{background:transparent; border:2px solid var(--fs-amber);}
.fs-dr.na .dot{background:transparent; border:2px solid #BDB8A6; width:9px; height:2px; border-radius:2px; border-width:0; background:#BDB8A6; height:3px;}
.fs-dr .nm{flex:1; color:var(--fs-ink);}
.fs-dr .st{font-size:.76rem; font-weight:600;}
.fs-dr.ok .st{color:var(--fs-forest-d);} .fs-dr.miss .st{color:#8A5313;} .fs-dr.na .st{color:var(--fs-muted);}
.fs-dnote{font-size:.76rem; color:var(--fs-muted); margin-top:.4rem; line-height:1.4;}

/* ---------- KPI tiles ---------- */
.fs-kpis{display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:10px;}
.fs-kpis.c3{grid-template-columns:repeat(3,minmax(0,1fr)); grid-auto-rows:minmax(212px,1fr);}
.fs-kpi{
  background:var(--fs-surface); border:1px solid var(--fs-border); border-radius:10px; padding:.8rem .95rem .75rem;
  transition:transform 400ms var(--spring-gentle), box-shadow 400ms var(--spring-gentle), border-color 250ms ease;
  will-change:transform, box-shadow; cursor:default;
}
.fs-kpi:hover{transform:translateY(-2.5px); box-shadow:0 6px 18px rgba(47,107,69,.06); border-color:#D3DDC9;}
.fs-kpi:active{transform:scale(0.985); transition-duration:120ms;}
.fs-kpi .n{font-size:.74rem; text-transform:uppercase; letter-spacing:.06em; color:var(--fs-muted); font-weight:650;}
.fs-kpi .v{font-size:1.75rem; font-weight:680; letter-spacing:-0.02em; line-height:1.15; margin:.15rem 0 .05rem; transition:transform 300ms var(--spring-snappy); display:inline-block;}
.fs-kpi:hover .v{transform:scale(1.02);}
.fs-kpi .v small{font-size:.8rem; color:var(--fs-muted); font-weight:550; letter-spacing:0; margin-left:.25rem;}
.fs-kpi .d{font-size:.8rem; color:var(--fs-muted); line-height:1.35;}
.fs-kpi .c{font-size:.78rem; color:var(--fs-forest-d); border-top:1px dashed var(--fs-border); margin-top:.45rem; padding-top:.35rem; line-height:1.35;}
.fs-kpi .c.warn{color:#8A5313;}

/* ---------- comparison table ---------- */
.fs-tablewrap{overflow-x:auto; background:var(--fs-surface); border:1px solid var(--fs-border); border-radius:10px; transition:box-shadow 400ms var(--spring-gentle);}
.fs-tablewrap:hover{box-shadow:0 4px 16px rgba(0,0,0,.04);}
table.fs-table{border-collapse:collapse; width:100%; min-width:560px; font-size:.88rem;}
.fs-table tbody tr{transition:background-color 200ms ease;}
.fs-table tbody tr:not(.grp):hover{background-color:rgba(239,236,226,.4);}
.fs-table th{background:#F6F4EC; text-align:left; font-weight:650; padding:.6rem .8rem; border-bottom:1px solid var(--fs-border); vertical-align:bottom; transition:background-color 200ms ease;}
.fs-table th small{display:block; color:var(--fs-muted); font-weight:500; font-size:.72rem;}
.fs-table td{padding:.55rem .8rem; border-bottom:1px solid #F0EDE2; vertical-align:top;}
.fs-table tr:last-child td{border-bottom:none;}
.fs-table td.m{color:var(--fs-muted); width:28%;}
.fs-table tr.grp td{background:#F6F4EC; font-size:.72rem; text-transform:uppercase; letter-spacing:.07em; font-weight:700; color:var(--fs-olive); padding:.4rem .8rem;}
.fs-table th.top{background:#EEF4E8; border-top:3px solid var(--fs-forest);}
.fs-table .tag2{
  display:inline-block; background:var(--fs-forest); color:#fff; font-size:.64rem; letter-spacing:.05em; text-transform:uppercase;
  padding:.05rem .4rem; border-radius:4px; margin-bottom:.25rem; animation:kinetics-bloom 600ms var(--spring-bouncy) both;
  transition:transform 350ms var(--spring-bouncy); will-change:transform;
}
.fs-table .tag2:hover{transform:scale(1.08);}
.fs-table td.best{font-weight:680; color:var(--fs-forest-d); background:#F1F6EC; transition:transform 300ms var(--spring-bouncy), background-color 200ms ease; will-change:transform;}
table.fs-table tbody tr:hover td.best{background:#E5EFDD; transform:scale(1.02);}
.fs-table td.cur, .fs-table th.cur{border-left:3px solid #CFC8B4;}
.fs-table .num{font-variant-numeric:tabular-nums;}

/* ---------- option cards ---------- */
.fs-opt-h{font-size:1.02rem; font-weight:680; line-height:1.3; margin-bottom:.25rem;}
.fs-tag{
  display:inline-block; font-size:.7rem; font-weight:650; letter-spacing:.04em; text-transform:uppercase; padding:.12rem .5rem; border-radius:5px;
  background:#ECE8DC; color:#5C584A; transition:transform 350ms var(--spring-bouncy), box-shadow 350ms var(--spring-bouncy); will-change:transform;
}
.fs-tag:hover{transform:scale(1.06); box-shadow:0 2px 6px rgba(0,0,0,.08);}
.fs-tag.top{background:var(--fs-forest); color:#fff; animation:kinetics-bloom 600ms var(--spring-bouncy) both;}
.fs-tag.new{background:var(--fs-sage-l); color:var(--fs-forest-d);}
.fs-score{display:flex; align-items:baseline; gap:.4rem; margin:.5rem 0 .2rem;}
.fs-score b{font-size:2.3rem; font-weight:700; letter-spacing:-0.03em; color:var(--fs-forest-d); line-height:1; transition:transform 400ms var(--spring-bouncy); display:inline-block; will-change:transform;}
[class*="st-key-panel_card"]:hover .fs-score b, .st-key-panel_cardtop:hover .fs-score b{transform:scale(1.04);}
.fs-score span{font-size:.8rem; color:var(--fs-muted);}
.fs-bar{height:6px; background:#ECE8DC; border-radius:4px; overflow:hidden; margin:.1rem 0 .35rem; position:relative;}
.fs-bar i{display:block; height:100%; background:var(--fs-forest); border-radius:4px; transition:width 900ms var(--spring-elastic); will-change:width;}
.fs-line{font-size:.85rem; margin:.18rem 0; color:var(--fs-ink);}
.st-key-panel_cardtop{border:2px solid var(--fs-forest) !important; box-shadow:0 3px 12px rgba(47,107,69,.08);}
.st-key-panel_cardtop:hover{border-color:var(--fs-forest-d) !important; box-shadow:0 10px 28px rgba(47,107,69,.14);}
.fs-next{display:flex; gap:1rem; align-items:center; justify-content:space-between;}
.fs-next b{font-size:1.05rem;} .fs-next span{color:var(--fs-muted); font-size:.9rem;}
.fs-summary{border-left:4px solid var(--fs-forest); padding:.2rem 0 .2rem 1rem;}

/* ---------- widgets & inputs (Kinetics Tactile Depress & Focus Springs) ---------- */
.stButton > button, .stFormSubmitButton > button{
  border-radius:8px; border:1px solid var(--fs-border);
  transition:transform 400ms var(--spring-snappy), box-shadow 400ms var(--spring-snappy), background-color 200ms ease, border-color 200ms ease, color 200ms ease;
  will-change:transform; cursor:pointer;
}
.stButton > button:hover, .stFormSubmitButton > button:hover{
  transform:translateY(-2px) scale(1.01); box-shadow:0 4px 12px rgba(0,0,0,.08); border-color:#D3DDC9;
}
.stButton > button:active, .stFormSubmitButton > button:active{
  transform:translateY(0) scale(0.96); transition-duration:120ms; box-shadow:0 1px 3px rgba(0,0,0,.06);
}
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"]{
  background:var(--fs-forest); border:1px solid var(--fs-forest-d); border-radius:8px; font-weight:600; color:#FFFFFF;
  box-shadow:0 2px 6px rgba(47,107,69,.2);
}
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover{
  background:var(--fs-forest-d); transform:translateY(-2px) scale(1.01); box-shadow:0 6px 18px rgba(35,78,53,.28);
}
.stButton > button[kind="primary"]:active, .stFormSubmitButton > button[kind="primary"]:active{
  transform:translateY(0) scale(0.96); transition-duration:120ms; box-shadow:0 2px 5px rgba(35,78,53,.2);
}
[data-testid="stExpander"]{
  border:1px solid var(--fs-border); border-radius:9px; background:var(--fs-surface);
  transition:border-color 250ms ease, box-shadow 380ms var(--spring-gentle), transform 380ms var(--spring-gentle);
}
[data-testid="stExpander"]:hover{box-shadow:0 4px 14px rgba(0,0,0,.04);}
[data-testid="stExpander"] summary{
  font-weight:600; transition:color 200ms ease, background-color 200ms ease, transform 250ms var(--spring-snappy);
}
[data-testid="stExpander"] summary:active{transform:scale(0.995); transition-duration:100ms;}
[data-baseweb="select"] > div{
  border-radius:8px; background:#fff;
  transition:border-color 250ms ease, box-shadow 350ms var(--spring-snappy), transform 350ms var(--spring-snappy);
}
[data-baseweb="select"] > div:focus-within{
  border-color:var(--fs-forest) !important; box-shadow:0 0 0 3px rgba(47,107,69,.18) !important; transform:scale(1.003);
}
[data-testid="stNumberInput"] input{
  border-radius:8px; background:#fff; transition:border-color 250ms ease, box-shadow 350ms var(--spring-snappy);
}
[data-testid="stNumberInput"] input:focus{
  border-color:var(--fs-forest) !important; box-shadow:0 0 0 3px rgba(47,107,69,.18) !important;
}
[data-testid="stSlider"] div[role="slider"]{
  transition:transform 300ms var(--spring-bouncy), box-shadow 300ms var(--spring-snappy); will-change:transform;
}
[data-testid="stSlider"] div[role="slider"]:hover, [data-testid="stSlider"] div[role="slider"]:active{
  transform:scale(1.25); box-shadow:0 2px 8px rgba(47,107,69,.28);
}
[data-testid="stDataFrame"]{
  border:1px solid var(--fs-border); border-radius:10px; transition:box-shadow 400ms var(--spring-gentle);
}
[data-testid="stDataFrame"]:hover{box-shadow:0 4px 14px rgba(0,0,0,.04);}
[data-testid="stAlert"]{
  border-radius:9px; animation:kinetics-surface-enter 450ms var(--spring-gentle) both;
  transition:transform 350ms var(--spring-gentle), box-shadow 350ms var(--spring-gentle);
}
[data-testid="stAlert"]:hover{transform:translateY(-1.5px); box-shadow:0 4px 12px rgba(0,0,0,.05);}

/* ---------- kinetics keyframe animations ---------- */
@keyframes kinetics-bloom{
  0%{transform:scale(0.7); opacity:0.7;}
  50%{transform:scale(1.12);}
  100%{transform:scale(1); opacity:1;}
}
@keyframes kinetics-surface-enter{
  0%{opacity:0; transform:scale(0.96) translateY(6px);}
  100%{opacity:1; transform:scale(1) translateY(0);}
}
@keyframes kinetics-breathe{
  0%{transform:scale(1); opacity:0.85;}
  100%{transform:scale(1.35); opacity:1;}
}
@keyframes kinetics-shake{
  0%, 100%{transform:translateX(0);}
  20%{transform:translateX(-5px);}
  40%{transform:translateX(4px);}
  60%{transform:translateX(-3px);}
  80%{transform:translateX(2px);}
}

/* ---------- kinetics accessibility (prefers-reduced-motion) ---------- */
@media (prefers-reduced-motion: reduce){
  *, *::before, *::after{
    animation-duration:0.01ms !important;
    animation-iteration-count:1 !important;
    transition-duration:0.01ms !important;
    scroll-behavior:auto !important;
  }
}

@media (max-width: 760px){
  .block-container{padding:.8rem .8rem 2.5rem; max-width:100vw;}
  .st-key-hero{padding:1rem; background-image:none;}
  .fs-hero h1{font-size:1.4rem;}
  .st-key-langbox [role="radiogroup"]{float:none;}
  .fs-kpis, .fs-kpis.c3{grid-template-columns:repeat(2,minmax(0,1fr));}
  .fs-kpi .v{font-size:1.4rem;}
}
</style>
""".replace("%CONTOUR%", _CONTOUR.replace('"', "'"))


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def brand(tagline: str) -> str:
    return f'<div class="fs-brand">{LOGO_SVG}<div><b>Field Shift</b><span>{esc(tagline)}</span></div></div>'


def side_heading(text: str) -> None:
    st.markdown(f'<div class="fs-side-h">{esc(text)}</div>', unsafe_allow_html=True)


def notice(text: str) -> None:
    st.markdown(f'<div class="fs-notice"><i></i><span>{esc(text)}</span></div>', unsafe_allow_html=True)


def chip(text: str, on: bool = True) -> str:
    return f'<span class="fs-chip{"" if on else " off"}"><i></i>{esc(text)}</span>'


PIN = '<svg viewBox="0 0 16 16" fill="none" stroke="#2F6B45" stroke-width="1.6"><path d="M8 14.5s5-4.4 5-8.2A5 5 0 0 0 3 6.3c0 3.8 5 8.2 5 8.2z"/><circle cx="8" cy="6.3" r="1.7"/></svg>'


def hero_left(eyebrow: str, title: str, coords: str, extra: list[str], grows_label: str, crops: list[str], lead: str) -> str:
    """Selected-field card text: name, scannable coordinate chips, rotation chips, one-line purpose."""
    chips = f'<span class="fs-coord">{PIN}{esc(coords)}</span>' + "".join(f'<span class="fs-coord" style="font-weight:550">{esc(x)}</span>' for x in extra)
    rot = '<span class="lbl">' + esc(grows_label) + '</span><span class="fs-rotprev" style="margin:0">' + '<span class="a">→</span>'.join(
        f'<span class="c">{esc(c)}</span>' for c in crops) + "</span>"
    return (f'<div class="fs-hero"><div class="fs-eyebrow">{esc(eyebrow)}</div><h1>{esc(title)}</h1>'
            f'<div class="fs-meta">{chips}</div><div class="fs-meta">{rot}</div><p class="lead">{esc(lead)}</p></div>')


def data_status(title: str, rows: list[tuple[str, str, str, str]], note: str = "") -> str:
    """rows: (name, state in {ok, miss, na}, status text, tooltip). Three visually distinct states."""
    body = "".join(f'<div class="fs-dr {stt}" title="{esc(tip)}"><span class="dot"></span><span class="nm">{esc(nm)}</span>'
                   f'<span class="st">{esc(txt)}</span></div>' for nm, stt, txt, tip in rows)
    return f'<div class="fs-data"><h4>{esc(title)}</h4>{body}' + (f'<div class="fs-dnote">{esc(note)}</div>' if note else "") + "</div>"


def rotation_preview(crops: list[str]) -> None:
    st.markdown('<div class="fs-rotprev">' + '<span class="a">→</span>'.join(f'<span class="c">{esc(c)}</span>' for c in crops) + "</div>",
                unsafe_allow_html=True)


def layer_line(title: str, items: list[tuple[str, str, str, bool]]) -> str:
    """One quiet line under the map: each NASA layer with its observation date, or 'unavailable' in amber."""
    parts = "".join(f'<span class="fs-lyr{"" if ok else " off"}" title="{esc(tip)}"><b>{esc(n)}</b> {esc(txt)}</span>' for n, txt, tip, ok in items)
    return f'<div class="fs-lyrs"><span class="h">{esc(title)}</span>{parts}</div>'


def group_label(text: str) -> None:
    st.markdown(f'<div class="fs-grp">{esc(text)}</div>', unsafe_allow_html=True)


def kpi(name: str, value: str, unit: str, desc: str, ctx: str = "", warn: bool = False) -> str:
    unit_html = f"<small>{esc(unit)}</small>" if unit else ""
    ctx_html = f'<div class="c{" warn" if warn else ""}">{esc(ctx)}</div>' if ctx else ""
    return (f'<div class="fs-kpi"><div class="n">{esc(name)}</div><div class="v">{esc(value)}{unit_html}</div>'
            f'<div class="d">{esc(desc)}</div>{ctx_html}</div>')


def kpi_grid(items: list[str], cols: int | None = None) -> None:
    cls = f"fs-kpis c{cols}" if cols else "fs-kpis"
    st.markdown(f'<div class="{cls}">{"".join(items)}</div>', unsafe_allow_html=True)


def section(title: str, sub: str = "") -> None:
    st.markdown(f"## {title}")
    if sub:
        st.caption(sub)


def compare_table(head: list[tuple[str, str, bool]], rows: list, metric_label: str, top: int | None = None, top_tag: str = "") -> None:
    """head: (name, small tag, is_current) per option. rows: (measure, cell texts, best indexes) or ("__group__", label).
    `top` = index of the highlighted (best-fit) option. All texts are escaped."""
    def th_cell(i, n, tag, cur):
        mark = f'<span class="tag2">{esc(top_tag)}</span><br>' if top == i and top_tag else ""
        return f'<th class="{"cur" if cur else ""}{" top" if top == i else ""}">{mark}{esc(n)}<small>{esc(tag)}</small></th>'
    th = "".join(th_cell(i, n, tag, cur) for i, (n, tag, cur) in enumerate(head))
    body = ""
    for row in rows:
        if row[0] == "__group__":
            body += f'<tr class="grp"><td colspan="{len(head) + 1}">{esc(row[1])}</td></tr>'
            continue
        label, cells, best = row
        tds = "".join(f'<td class="num{" best" if i in best else ""}{" cur" if head[i][2] else ""}">{esc(c)}</td>' for i, c in enumerate(cells))
        body += f'<tr><td class="m">{esc(label)}</td>{tds}</tr>'
    st.markdown(f'<div class="fs-tablewrap"><table class="fs-table"><thead><tr><th>{esc(metric_label)}</th>{th}</tr></thead>'
                f'<tbody>{body}</tbody></table></div>', unsafe_allow_html=True)


def score_block(fit: float, caption: str) -> str:
    pct = max(0.0, min(100.0, fit))
    return (f'<div class="fs-score"><b>{fit:.0f}</b><span>/ 100</span></div><div class="fs-bar"><i style="width:{pct:.0f}%"></i></div>'
            f'<div class="fs-line" style="color:var(--fs-muted);font-size:.78rem">{esc(caption)}</div>')
