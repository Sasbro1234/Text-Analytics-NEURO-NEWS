import sys

with open(r"c:\Users\acer\Desktop\Semester 05\Text Analytics\group project 2\src\streamlit_app.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Replace superb-nav CSS
css_old = "    /* Custom Fixed Anchor Navigation */"
css_start_idx = code.find(css_old)
css_end_idx = code.find("    /* Interactive Dashboard Hover */")
if css_start_idx != -1 and css_end_idx != -1:
    before = code[:css_start_idx]
    after = code[css_end_idx:]
    css_new = """    /* ── NAV BAR STYLING & INTERACTION ── */

    /* Sticky wrapper — collapsed height so it doesn't block content */
    [data-testid="stVerticalBlock"] > div:has(div[data-testid="stRadio"]) {
        position: sticky !important;
        top: 15px !important;
        z-index: 9999 !important;
        height: 0px !important;
        overflow: visible !important;
        display: flex !important;
        justify-content: center !important;
        align-items: flex-start !important;
        pointer-events: none !important;
        margin-bottom: 70px !important;
    }

    /* The pill */
    div[data-testid="stRadio"] {
        pointer-events: auto !important;
        position: relative !important;
        top: 0px !important;
        width: auto !important;
        max-width: fit-content !important;
        min-width: 0 !important;
        display: inline-flex !important;
        align-items: center !important;
        align-self: center !important;
        margin: 0 auto !important;
        background: rgba(4, 20, 40, 0.95) !important;
        border: 2px solid rgba(56, 189, 248, 0.8) !important;
        border-radius: 99px !important;
        padding: 6px 16px !important;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.3), inset 0 0 10px rgba(56, 189, 248, 0.1) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
    }

    /* Hide default radio elements */
    div[data-testid="stRadio"] > label:first-child { display: none !important; }
    div[data-testid="stRadio"] input[type="radio"] { display: none !important; }
    div[data-testid="stRadio"] > div > label > div:first-child { display: none !important; }

    /* Options row */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        display: inline-flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 4px !important;
        align-items: center !important;
        pointer-events: auto !important;
    }

    /* Each tab label */
    div[data-testid="stRadio"] > div > label {
        display: flex !important;
        align-items: center !important;
        padding: 10px 26px !important;
        border-radius: 99px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        color: #7dd3fc !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        white-space: nowrap !important;
        background: transparent !important;
        pointer-events: auto !important;
    }

    div[data-testid="stRadio"] > div > label:hover {
        background: rgba(56, 189, 248, 0.2) !important;
        color: #ffffff !important;
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.4) !important;
        transform: translateY(-1px) !important;
    }

    div[data-testid="stRadio"] > div > label:has(input:checked) {
        background: rgba(56, 189, 248, 0.25) !important;
        color: #ffffff !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.5) !important;
    }

    /* All children clickable */
    div[data-testid="stRadio"] * {
        pointer-events: auto !important;
        cursor: pointer !important;
    }

    /* Column wrappers — non-blocking */
    [data-testid="stHorizontalBlock"] {
        pointer-events: none !important;
    }
    [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        pointer-events: auto !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    .stApp { overflow: visible !important; }

    /* Force Streamlit's main wrapper to allow sticky positioning */
    section[data-testid="stMain"] {
        overflow: visible !important;
    }

    section[data-testid="stMain"] > div {
        overflow: visible !important;
    }

    [data-testid="stAppViewContainer"] {
        overflow: visible !important;
    }
    
    [data-testid="stExpander"] > div:first-child {
        padding: 0px 16px !important;
        min-height: 48px !important;
        display: flex !important;
        align-items: center !important;
    }

"""
    code = before + css_new + after

# 2. remove anchor-offset
code = code.replace("    .anchor-offset {\n        display: block;\n        height: 120px;\n        margin-top: -120px;\n        visibility: hidden;\n    }\n", "")
code = code.replace("st.markdown('<div id=\"landing-station\" class=\"anchor-offset\"></div>', unsafe_allow_html=True)\n", "")
code = code.replace("st.markdown('<div id=\"classification-matrix\" class=\"anchor-offset\"></div>', unsafe_allow_html=True)\n", "")
code = code.replace("st.markdown('<div id=\"intelligent-qa\" class=\"anchor-offset\"></div>', unsafe_allow_html=True)\n", "")
code = code.replace("st.markdown('<div id=\"insights-dashboard\" class=\"anchor-offset\"></div>', unsafe_allow_html=True)\n", "")

# 3. selectbox css
code = code.replace("    /* Expander / Inputs / Charts */", """    .stSelectbox > div > div > div {
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        height: auto !important;
        min-height: 48px !important;
    }

    /* Always show dropdown arrow */
    .stSelectbox [data-baseweb="select"] svg {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        fill: #38bdf8 !important;
    }

    .stSelectbox [data-baseweb="select"] > div {
        overflow: visible !important;
    }

    .stSelectbox [data-baseweb="select"] > div:last-child {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    /* Restore dropdown arrow */
    .stSelectbox > div > div > div > svg {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        color: #38bdf8 !important;
    }

    .stSelectbox [data-baseweb="select"] > div:last-child {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    /* Expander / Inputs / Charts */""")

# 4. Navigation Logic Replacement
nav_old = """# CUSTOM FIXED ANCHOR NAVIGATION
st.markdown(\"\"\"
<div class="superb-nav">
   <a href="#landing-station"><i class="fa-solid fa-cloud-arrow-up"></i> Upload</a>
   <a href="#classification-matrix"><i class="fa-solid fa-table"></i> Matrix</a>
   <a href="#intelligent-qa"><i class="fa-solid fa-sparkles"></i> Q&A</a>
   <a href="#insights-dashboard"><i class="fa-solid fa-chart-pie"></i> Insights</a>
</div>
\"\"\", unsafe_allow_html=True)

# Global Session
if "df" in st.session_state:
    df = st.session_state.df
else:
    df = None"""

nav_new = """# ── Session State Init ────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "upload"

if "df" in st.session_state:
    df = st.session_state.df
else:
    df = None

# ── NAVIGATION BAR ───────────────────────────────────────────────────────────
page_labels = {
    "upload":   "⬆  Upload",
    "export":   "⊞  Export Hub",
    "qa":       "✦  Q&A",
    "insights": "◉  Insights",
}
label_to_key = {v: k for k, v in page_labels.items()}

try:
    current_index = list(page_labels.keys()).index(st.session_state.page)
except (ValueError, KeyError):
    current_index = 0

_nav_l, _nav_c, _nav_r = st.columns([1, 2, 1])

with _nav_c:
    selected_label = st.radio(
    label="nav",
    options=list(page_labels.values()),
    index=current_index,
    horizontal=True,
    label_visibility="collapsed",
)

selected_key = label_to_key[selected_label]
if selected_key != st.session_state.page:
    st.session_state.page = selected_key
    st.rerun()"""
code = code.replace(nav_old, nav_new)

# 5. Fix Section 1 indentation and redirection
s1_start = "# SECTION 1: LANDING STATION"
s2_start = "# SECTION 2: CLASSIFICATION MATRIX"
s3_start = "# SECTION 3: INTELLIGENT Q&A"
s4_start = "# SECTION 4: INSIGHTS DASHBOARD"

block1 = code.split(s1_start)[1].split(s2_start)[0]
block1 = block1.replace('st.markdown("<hr style=\\'border:1px solid rgba(56,189,248,0.1); margin: 60px 0;\\'>", unsafe_allow_html=True)', '')
indented_block1 = "\\n".join(["    " + line if line.strip() else line for line in block1.split("\\n")])
indented_block1 = indented_block1.replace('    st.rerun()', '    st.session_state.page = "export"\\n                st.rerun()')
new_s1 = "\\n# ══════════════════════════════════════════════════════════════════════════════\\n# PAGE 1 — UPLOAD\\n# ══════════════════════════════════════════════════════════════════════════════\\nif st.session_state.page == \"upload\":\\n" + indented_block1

# Fix Section 2
block2 = code.split(s2_start)[1].split(s3_start)[0]
block2 = block2.replace('st.markdown("<hr style=\\'border:1px solid rgba(56,189,248,0.1); margin: 60px 0;\\'>", unsafe_allow_html=True)', '')
indented_block2 = "\\n".join(["    " + line if line.strip() else line for line in block2.split("\\n")])
indented_block2 = indented_block2.replace("st.markdown(\"<div class='instruction-box'><i class='fa-solid fa-lock'></i> Matrix Locked. Awaiting dataset ingestion from Landing Station.</div>\", unsafe_allow_html=True)", "st.markdown(\"<div class='instruction-box'><i class='fa-solid fa-lock'></i> Hub Locked. Please upload and process a dataset from the <b>Upload</b> page first.</div>\", unsafe_allow_html=True)\\n        if st.button(\"Go to Upload1\"):\\n            st.session_state.page = \"upload\"\\n            st.rerun()")
new_s2 = "\\n# ══════════════════════════════════════════════════════════════════════════════\\n# PAGE 2 — DATA EXPORT HUB\\n# ══════════════════════════════════════════════════════════════════════════════\\nelif st.session_state.page == \"export\":\\n" + indented_block2

# Fix Section 3
block3 = code.split(s3_start)[1].split(s4_start)[0]
block3 = block3.replace('st.markdown("<hr style=\\'border:1px solid rgba(56,189,248,0.1); margin: 60px 0;\\'>", unsafe_allow_html=True)', '')
indented_block3 = "\\n".join(["    " + line if line.strip() else line for line in block3.split("\\n")])
indented_block3 = indented_block3.replace('selected_option = st.selectbox("Assign Context Node", options)', 'st.markdown("<style>div[data-testid=\'stSelectbox\'] { width: 100% !important; } div[data-testid=\'stSelectbox\'] > div { width: 100% !important; }</style>", unsafe_allow_html=True)\\n        selected_option = st.selectbox("Assign Context Node", options)')
indented_block3 = indented_block3.replace("st.markdown(\"<div class='instruction-box'><i class='fa-solid fa-lock'></i> Q&A Hub Locked. Awaiting dataset ingestion.</div>\", unsafe_allow_html=True)", "st.markdown(\"<div class='instruction-box'><i class='fa-solid fa-lock'></i> Q&A Hub Locked. Please upload and process a dataset from the <b>Upload</b> page first.</div>\", unsafe_allow_html=True)\\n        if st.button(\"Go to Upload2\"):\\n            st.session_state.page = \"upload\"\\n            st.rerun()")
new_s3 = "\\n# ══════════════════════════════════════════════════════════════════════════════\\n# PAGE 3 — INTELLIGENT Q&A\\n# ══════════════════════════════════════════════════════════════════════════════\\nelif st.session_state.page == \"qa\":\\n" + indented_block3

# Fix Section 4
footer_start = "st.markdown(\"<p style='text-align: center; color: rgba(56,189,248,0.5);"
block4 = code.split(s4_start)[1].split(footer_start)[0]
spinner_split = block4.split('with st.spinner("Compiling Neural Analytics..."):')
b4_top = spinner_split[0]
b4_bottom = spinner_split[1].split('else:')[0]
indented_b4_top = "\\n".join(["    " + line if line.strip() else line for line in b4_top.split("\\n")])
new_s4 = "\\n# ══════════════════════════════════════════════════════════════════════════════\\n# PAGE 4 — INSIGHTS DASHBOARD\\n# ══════════════════════════════════════════════════════════════════════════════\\nelif st.session_state.page == \"insights\":\\n" + indented_b4_top

new_s4 += """        if st.session_state.get("show_insights", False):
"""
for line in b4_bottom.split("\\n"):
    if line.strip():
        new_s4 += "    " + line.rstrip() + "\\n"
    else:
        new_s4 += "\\n"
new_s4 += "                st.session_state.show_insights = False\\n"
new_s4 += """    else:
        st.markdown("<div class='instruction-box'><i class='fa-solid fa-lock'></i> Analytics Locked. Please upload and process a dataset from the <b>Upload</b> page first.</div>", unsafe_allow_html=True)
        if st.button("Go to Upload3"):
            st.session_state.page = "upload"
            st.rerun()
"""

# Reassemble
code = code.split(s1_start)[0] + new_s1 + new_s2 + new_s3 + new_s4 + "\\n# ── FOOTER ────────────────────────────────────────────────────────────────────\\n" + footer_start + code.split(footer_start)[1]

with open(r"c:\Users\acer\Desktop\Semester 05\Text Analytics\group project 2\src\streamlit_app.py", "w", encoding="utf-8") as f:
    f.write(code)
print("Updated successfully")
