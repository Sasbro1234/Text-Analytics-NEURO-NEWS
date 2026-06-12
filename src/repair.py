file_path = r"c:\Users\acer\Desktop\Semester 05\Text Analytics\group project 2\src\streamlit_app.py"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")

out_lines = []
in_superb = False
in_anchor = False

for line in lines:
    # Remove superb-nav
    if "/* Custom Fixed Anchor Navigation */" in line:
        in_superb = True
        
        # Insert new css
        out_lines.append("""    /* ── NAV BAR STYLING & INTERACTION ── */

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

    div[data-testid="stRadio"] > label:first-child { display: none !important; }
    div[data-testid="stRadio"] input[type="radio"] { display: none !important; }
    div[data-testid="stRadio"] > div > label > div:first-child { display: none !important; }

    div[data-testid="stRadio"] > div[role="radiogroup"] {
        display: inline-flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 4px !important;
        align-items: center !important;
        pointer-events: auto !important;
    }

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

    div[data-testid="stRadio"] * {
        pointer-events: auto !important;
        cursor: pointer !important;
    }

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

    section[data-testid="stMain"] { overflow: visible !important; }
    section[data-testid="stMain"] > div { overflow: visible !important; }
    [data-testid="stAppViewContainer"] { overflow: visible !important; }
    [data-testid="stExpander"] > div:first-child { padding: 0px 16px !important; min-height: 48px !important; display: flex !important; align-items: center !important; }
""")
        continue
    
    if in_superb and "/* Interactive Dashboard Hover */" in line:
        in_superb = False
        out_lines.append(line)
        continue
    if in_superb:
        continue
        
    # Remove anchor-offset css
    if ".anchor-offset {" in line:
        in_anchor = True
        continue
    if in_anchor and "visibility: hidden;" in line:
        continue
    if in_anchor and "}" in line:
        in_anchor = False
        continue
    if in_anchor:
        continue

    # Add Selectbox CSS
    if "/* Expander / Inputs / Charts */" in line:
        out_lines.append("""    .stSelectbox > div > div > div { white-space: nowrap !important; overflow: hidden !important; text-overflow: ellipsis !important; height: auto !important; min-height: 48px !important; }
    .stSelectbox [data-baseweb="select"] svg { display: block !important; visibility: visible !important; opacity: 1 !important; fill: #38bdf8 !important; }
    .stSelectbox [data-baseweb="select"] > div { overflow: visible !important; }
    .stSelectbox [data-baseweb="select"] > div:last-child { display: flex !important; visibility: visible !important; opacity: 1 !important; }
    .stSelectbox > div > div > div > svg { display: block !important; visibility: visible !important; opacity: 1 !important; color: #38bdf8 !important; }""")
        out_lines.append(line)
        continue

    out_lines.append(line)

content = "\n".join(out_lines)

# Nav logic replace
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

content = content.replace(nav_old, nav_new)

# Remove anchor divs
content = content.replace("st.markdown('<div id=\"landing-station\" class=\"anchor-offset\"></div>', unsafe_allow_html=True)\n", "")
content = content.replace("st.markdown('<div id=\"classification-matrix\" class=\"anchor-offset\"></div>', unsafe_allow_html=True)\n", "")
content = content.replace("st.markdown('<div id=\"intelligent-qa\" class=\"anchor-offset\"></div>', unsafe_allow_html=True)\n", "")
content = content.replace("st.markdown('<div id=\"insights-dashboard\" class=\"anchor-offset\"></div>', unsafe_allow_html=True)\n", "")

# Remove HRs
content = content.replace('st.markdown("<hr style=\'border:1px solid rgba(56,189,248,0.1); margin: 60px 0;\'>", unsafe_allow_html=True)\n', '')


# Fix Section logic
s1 = content.split("# SECTION 1: LANDING STATION")[1].split("# SECTION 2: CLASSIFICATION MATRIX")[0]
s1_new = "\\n# ══════════════════════════════════════════════════════════════════════════════\\n# PAGE 1 — UPLOAD\\n# ══════════════════════════════════════════════════════════════════════════════\\nif st.session_state.page == \\"upload\\":\\n"
for l in s1.split("\\n"):
    if l.strip():
        # Export handling
        if l.strip() == "st.rerun()":
            s1_new += "                st.session_state.page = \"export\"\\n"
            s1_new += "                st.rerun()\\n"
        else:
            s1_new += "    " + l + "\\n"
    else:
        s1_new += "\\n"

s2 = content.split("# SECTION 2: CLASSIFICATION MATRIX")[1].split("# SECTION 3: INTELLIGENT Q&A")[0]
s2_new = "# ══════════════════════════════════════════════════════════════════════════════\\n# PAGE 2 — DATA EXPORT HUB\\n# ══════════════════════════════════════════════════════════════════════════════\\nelif st.session_state.page == \\"export\\":\\n"
for l in s2.split("\\n"):
    if l.strip():
        if "Matrix Locked" in l:
            s2_new += "        st.markdown(\"<div class='instruction-box'><i class='fa-solid fa-lock'></i> Hub Locked. Please upload and process a dataset from the <b>Upload</b> page first.</div>\", unsafe_allow_html=True)\\n"
            s2_new += "        if st.button(\"Go to Upload1\"):\\n"
            s2_new += "            st.session_state.page = \"upload\"\\n"
            s2_new += "            st.session_state.pop(\"nav_radio\", None)\\n"
            s2_new += "            st.rerun()\\n"
        else:
            s2_new += "    " + l + "\\n"
    elif l:
        s2_new += "\\n"

s3 = content.split("# SECTION 3: INTELLIGENT Q&A")[1].split("# SECTION 4: INSIGHTS DASHBOARD")[0]
s3_new = "# ══════════════════════════════════════════════════════════════════════════════\\n# PAGE 3 — INTELLIGENT Q&A\\n# ══════════════════════════════════════════════════════════════════════════════\\nelif st.session_state.page == \\"qa\\":\\n"
for l in s3.split("\\n"):
    if l.strip():
        if "Q&A Hub Locked" in l:
            s3_new += "        st.markdown(\"<div class='instruction-box'><i class='fa-solid fa-lock'></i> Q&A Hub Locked. Please upload and process a dataset from the <b>Upload</b> page first.</div>\", unsafe_allow_html=True)\\n"
            s3_new += "        if st.button(\"Go to Upload2\"):\\n"
            s3_new += "            st.session_state.page = \"upload\"\\n"
            s3_new += "            st.session_state.pop(\"nav_radio\", None)\\n"
            s3_new += "            st.rerun()\\n"
        elif "selected_option = st.selectbox" in l:
            s3_new += "        st.markdown(\"<style>div[data-testid='stSelectbox'] { width: 100% !important; } div[data-testid='stSelectbox'] > div { width: 100% !important; }</style>\", unsafe_allow_html=True)\\n"
            s3_new += "        selected_option = st.selectbox(\"Assign Context Node\", options)\\n"
        else:
            s3_new += "    " + l + "\\n"
    elif l:
        s3_new += "\\n"

foot_line = "st.markdown(\"<p style='text-align: center;"
s4 = content.split("# SECTION 4: INSIGHTS DASHBOARD")[1].split(foot_line)[0]
s4_new = "# ══════════════════════════════════════════════════════════════════════════════\\n# PAGE 4 — INSIGHTS DASHBOARD\\n# ══════════════════════════════════════════════════════════════════════════════\\nelif st.session_state.page == \\"insights\\":\\n"

b4_top = s4.split('with st.spinner("Compiling Neural Analytics..."):')[0]
for l in b4_top.split("\\n"):
    if l.strip():
        s4_new += "    " + l + "\\n"
    elif l:
        s4_new += "\\n"

s4_new += "        if st.session_state.get(\"show_insights\", False):\\n"
b4_bot = s4.split('with st.spinner("Compiling Neural Analytics..."):')[1].split("else:")[0]

for l in b4_bot.split("\\n"):
    if l.strip():
        s4_new += "    " + l + "\\n"
    elif l:
        s4_new += "\\n"
s4_new += "                st.session_state.show_insights = False\\n"
s4_new += "    else:\\n"
s4_new += "        st.markdown(\"<div class='instruction-box'><i class='fa-solid fa-lock'></i> Analytics Locked. Please upload and process a dataset from the <b>Upload</b> page first.</div>\", unsafe_allow_html=True)\\n"
s4_new += "        if st.button(\"Go to Upload3\"):\\n"
s4_new += "            st.session_state.page = \"upload\"\\n"
s4_new += "            st.session_state.pop(\"nav_radio\", None)\\n"
s4_new += "            st.rerun()\\n"

final_file = content.split("# SECTION 1: LANDING STATION")[0] + s1_new + s2_new + s3_new + s4_new + "\\n# ── FOOTER ────────────────────────────────────────────────────────────────────\\n" + foot_line + content.split(foot_line)[1]


# Clean up double blank lines that were stripped
final_file = final_file.replace("    \\n", "\\n").replace("\\n\\n\\n", "\\n\\n")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(final_file)
