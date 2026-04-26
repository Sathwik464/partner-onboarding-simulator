import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Partner Validator",
    page_icon="◎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif !important;
}
[data-testid="stAppViewContainer"] { background: #f8f7f4; }
[data-testid="stSidebar"] {
    background: #f0efe9 !important;
    border-right: 1px solid #e0ddd4 !important;
}
.stButton > button {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 6px !important;
    background: #1a1a1a !important;
    color: #f8f7f4 !important;
    border: none !important;
}
.stButton > button:hover { background: #333 !important; }
[data-testid="stMetricValue"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 2.4rem !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)


def score_color(score):
    if score >= 80:
        return "#2d6a4f", "#d8f3dc"
    elif score >= 50:
        return "#b5540a", "#fde8d0"
    else:
        return "#9b2226", "#fde8e8"


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Register Partner")
    st.divider()

    company  = st.text_input("Company name", placeholder="Acme Publishers")
    website  = st.text_input("Website", placeholder="https://acme.com")
    platform = st.selectbox("Ad platform", ["GoogleAdManager", "AdSense", "AdMob"])
    endpoint = st.text_input("API endpoint", placeholder="https://api.acme.com/v1")
    auth     = st.selectbox("Auth method", ["OAuth", "APIKey", "JWT"])

    if st.button("Register →", use_container_width=True):
        if company and website and endpoint:
            res = requests.post(f"{BASE_URL}/partners/", json={
                "company_name": company,
                "company_url":  website,
                "ad_platform":  platform,
                "api_endpoint": endpoint,
                "auth_method":  auth
            })
            if res.status_code == 200:
                st.success(f"✓ {company} registered")
                st.rerun()
            else:
                st.error("Registration failed")
        else:
            st.warning("Fill in all fields")


# ── Main ───────────────────────────────────────────────────────────────────────
st.markdown("# Partner Validation Dashboard")
st.caption("Google Ad Integration Health Monitor")
st.divider()

partners_res = requests.get(f"{BASE_URL}/partners")

if partners_res.status_code != 200:
    st.error("Cannot connect to API. Make sure FastAPI is running on port 8000.")
    st.stop()

partners = partners_res.json()

if not partners:
    st.info("No partners registered yet. Add one from the sidebar.")
    st.stop()

# Partner selector
partner_names = {p["company_name"]: p["id"] for p in partners}
col1, col2 = st.columns([4, 1])

with col1:
    selected = st.selectbox("Select partner", list(partner_names.keys()),
                            label_visibility="collapsed")
with col2:
    run = st.button("Run validation →", use_container_width=True)

partner_id = partner_names[selected]
partner    = next(p for p in partners if p["id"] == partner_id)

st.caption(f"`{partner['api_endpoint']}` · **{partner['ad_platform']}** · **{partner['auth_method']}**")
st.divider()

# ── Results ────────────────────────────────────────────────────────────────────
if run:
    with st.spinner("Running validation checks..."):
        val_res = requests.post(f"{BASE_URL}/validate/{partner_id}")

    if val_res.status_code != 200:
        st.error("Validation failed — check API server")
        st.stop()

    data  = val_res.json()
    score = data["health_score"]
    text_color, bg_color = score_color(score)

    # Metric row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Health Score", f"{int(score)} / 100")
    c2.metric("Status", data["status"])
    c3.metric("Passed", f"{data['passed_checks']} / {data['total_checks']}")
    c4.metric("Failed", data["failed_checks"])

    st.divider()

    # ── Critical Issues ────────────────────────────────────────────────────────
    critical = data.get("critical_issues", [])
    warnings = data.get("warnings", [])

    if critical:
        st.error("🚨 Critical Issues Found")
        for issue in critical:
            st.markdown(f"**❌ {issue['check_type']}**")
            st.markdown(f"Issue: {issue['message']}")
            if issue.get("fix"):
                st.markdown(f"💡 Fix: {issue['fix']}")
            st.markdown("")
    else:
        st.success("✅ No critical issues found")

    # ── Warnings ───────────────────────────────────────────────────────────────
    if warnings:
        st.warning("⚠️ Warnings")
        for w in warnings:
            st.markdown(f"**⚠️ {w['check_type']}**")
            st.markdown(f"Issue: {w['message']}")
            if w.get("fix"):
                st.markdown(f"💡 Fix: {w['fix']}")
            st.markdown("")

    # ── All Checks Summary ─────────────────────────────────────────────────────
    st.markdown("#### 📋 All Checks Summary")

    critical_types = {c['check_type']: c for c in critical}
    warning_types  = {w['check_type']: w for w in warnings}

    check_types = [
        "Endpoint Reachability",
        "Response Time",
        "HTTPS Security",
        "Authentication Method"
    ]

    for ct in check_types:
        if ct in critical_types:
            issue  = critical_types[ct]
            passed = False
            msg    = issue['message']
            fix    = issue.get('fix', '')
            icon   = "❌"
        elif ct in warning_types:
            issue  = warning_types[ct]
            passed = False
            msg    = issue['message']
            fix    = issue.get('fix', '')
            icon   = "⚠️"
        else:
            passed = True
            msg    = "Passed"
            fix    = ""
            icon   = "✅"

        with st.container():
            col_a, col_b = st.columns([8, 1])
            with col_a:
                st.markdown(f"{icon} **{ct}**")
                st.caption(msg)
                if fix:
                    st.caption(f"💡 Fix: {fix}")
            with col_b:
                if passed:
                    st.success("pass")
                else:
                    st.error("fail")
            st.markdown("---")