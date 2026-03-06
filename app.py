"""
app.py - Password Cracking & Credential Attack Suite
      Educational Simulation Tool

Run with: streamlit run app.py
"""

import sys
import os
import time

# Ensure local modules resolve correctly
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

# ─── Page Config (MUST be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="PassSuite — Credential Attack Lab",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Imports ──────────────────────────────────────────────────────────────────
from modules.dictionary_generator import DictionaryGenerator
from modules.hash_handler import HashHandler, SUPPORTED_ALGORITHMS
from modules.brute_force import BruteForceEngine, CHARSETS as BF_CHARSETS
from modules.strength_analyzer import StrengthAnalyzer

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Exo 2', sans-serif;
    background-color: #070b12;
    color: #c8d8e8;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1520 0%, #070b12 100%);
    border-right: 1px solid #1e3050;
}

section[data-testid="stSidebar"] .stRadio label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    color: #7aaddd;
    letter-spacing: 0.05em;
}

/* ── Headers ── */
h1 { font-family: 'Share Tech Mono', monospace; color: #00e5ff !important; letter-spacing: 0.05em; }
h2 { font-family: 'Share Tech Mono', monospace; color: #7aaddd !important; letter-spacing: 0.03em; }
h3 { color: #a8c8e8 !important; }

/* ── Cards ── */
.card {
    background: linear-gradient(135deg, #0d1a2a 0%, #0a1520 100%);
    border: 1px solid #1e3a5a;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 0.75rem 0;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00e5ff, #0066ff, #00e5ff);
}

/* ── Result Cards ── */
.result-success {
    background: linear-gradient(135deg, #062010 0%, #041510 100%);
    border: 1px solid #00aa44;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin: 0.5rem 0;
}
.result-fail {
    background: linear-gradient(135deg, #1a0808 0%, #120505 100%);
    border: 1px solid #aa2222;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin: 0.5rem 0;
}
.result-info {
    background: linear-gradient(135deg, #081525 0%, #051020 100%);
    border: 1px solid #1155aa;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin: 0.5rem 0;
}

/* ── Hash display ── */
.hash-display {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    color: #00e5ff;
    background: #020810;
    border: 1px solid #1e3050;
    border-radius: 6px;
    padding: 0.6rem 1rem;
    word-break: break-all;
    letter-spacing: 0.05em;
}

/* ── Stat pill ── */
.stat-pill {
    display: inline-block;
    background: #0d1a2a;
    border: 1px solid #1e3a5a;
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.8rem;
    font-family: 'Share Tech Mono', monospace;
    color: #7aaddd;
    margin: 0.2rem;
}

/* ── Strength bar ── */
.strength-bar-container {
    background: #0a1520;
    border-radius: 999px;
    height: 14px;
    width: 100%;
    margin: 0.5rem 0;
    overflow: hidden;
    border: 1px solid #1e3050;
}

/* ── Disclaimer banner ── */
.disclaimer {
    background: linear-gradient(90deg, #1a0e00, #1a0500);
    border: 1px solid #ff8800;
    border-left: 4px solid #ff8800;
    border-radius: 6px;
    padding: 0.6rem 1rem;
    font-size: 0.82rem;
    color: #ffaa44;
    margin-bottom: 1rem;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0044aa, #0066cc) !important;
    color: #ffffff !important;
    border: 1px solid #0088ff !important;
    border-radius: 8px !important;
    font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 0.05em !important;
    transition: all 0.2s ease !important;
    padding: 0.5rem 1.5rem !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0055cc, #0077ee) !important;
    border-color: #00aaff !important;
    box-shadow: 0 0 12px rgba(0, 150, 255, 0.3) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background-color: #0a1520 !important;
    border: 1px solid #1e3a5a !important;
    color: #c8d8e8 !important;
    border-radius: 8px !important;
}

/* ── Progress bar ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #0066ff, #00e5ff) !important;
}

/* ── Metric ── */
[data-testid="metric-container"] {
    background: #0d1a2a;
    border: 1px solid #1e3a5a;
    border-radius: 10px;
    padding: 0.8rem;
}
[data-testid="metric-container"] label {
    color: #7aaddd !important;
    font-size: 0.75rem !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #0d1a2a !important;
    color: #7aaddd !important;
    border-radius: 8px !important;
    border: 1px solid #1e3a5a !important;
}

/* ── Divider ── */
hr { border-color: #1e3050 !important; }

/* ── Code ── */
code {
    background: #020810 !important;
    color: #00e5ff !important;
    border: 1px solid #1e3050 !important;
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def header(icon: str, title: str, subtitle: str = "") -> None:
    st.markdown(f"# {icon} {title}")
    if subtitle:
        st.markdown(f"<p style='color:#4a7aaa;font-size:0.9rem;margin-top:-0.5rem;'>{subtitle}</p>",
                    unsafe_allow_html=True)
    st.divider()


def card(content_fn):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    content_fn()
    st.markdown("</div>", unsafe_allow_html=True)


def disclaimer():
    st.markdown("""
    <div class="disclaimer">
    ⚠️ <strong>EDUCATIONAL USE ONLY</strong> — This tool is a local simulation for learning purposes.
    It does not interact with any real systems, networks, or credentials.
    Always use cybersecurity knowledge responsibly and legally.
    </div>""", unsafe_allow_html=True)


def strength_bar(score: int, color: str) -> None:
    pct = max(0, min(100, score))
    st.markdown(f"""
    <div class="strength-bar-container">
      <div style="width:{pct}%;height:100%;
                  background:linear-gradient(90deg,{color}88,{color});
                  border-radius:999px;transition:width 0.5s ease;">
      </div>
    </div>""", unsafe_allow_html=True)


def hash_display(h: str) -> None:
    st.markdown(f'<div class="hash-display">{h}</div>', unsafe_allow_html=True)


def result_box(msg: str, kind: str = "info") -> None:
    css = f"result-{kind}"
    st.markdown(f'<div class="{css}">{msg}</div>', unsafe_allow_html=True)


# ─── Pages ────────────────────────────────────────────────────────────────────

def page_home():
    st.markdown("""
    <div style='text-align:center;padding:2rem 0 1rem;'>
      <div style='font-family:"Share Tech Mono",monospace;font-size:2.8rem;
                  color:#00e5ff;letter-spacing:0.08em;text-shadow:0 0 20px #00e5ff55;'>
        🔐 PASSSUITE
      </div>
      <div style='color:#4a7aaa;font-size:1rem;margin-top:0.5rem;letter-spacing:0.2em;'>
        PASSWORD CRACKING &amp; CREDENTIAL ATTACK SUITE
      </div>
      <div style='display:inline-block;background:#0d1a2a;border:1px solid #ff8800;
                  border-radius:20px;padding:0.3rem 1.2rem;margin-top:0.8rem;
                  color:#ff8800;font-size:0.78rem;font-family:"Share Tech Mono",monospace;'>
        ⚠ EDUCATIONAL SIMULATION — LOCAL ONLY
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    modules = [
        ("📋", "Dictionary\nGenerator", "Generate mutated wordlists from names, patterns & common passwords"),
        ("🔑", "Hash Handler\n& Attack", "Hash passwords and run simulated dictionary attacks"),
        ("⚡", "Brute-Force\nSimulator", "Animate character-set enumeration with time estimates"),
        ("🛡️", "Strength\nAnalyzer", "Entropy scoring, pattern detection & improvement tips"),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3, c4], modules):
        with col:
            st.markdown(f"""
            <div class="card" style="text-align:center;min-height:160px;">
              <div style="font-size:2rem;margin-bottom:0.5rem;">{icon}</div>
              <div style="font-family:'Share Tech Mono',monospace;color:#00e5ff;
                          font-size:0.85rem;white-space:pre-line;margin-bottom:0.5rem;">{title}</div>
              <div style="font-size:0.78rem;color:#4a7aaa;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 Select a module from the sidebar to get started.", icon="ℹ️")


def page_dictionary():
    header("📋", "Dictionary Generator",
           "Build customized wordlists from name patterns, common passwords & keyboard walks")
    disclaimer()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### ⚙️ Configuration")
        name = st.text_input("Target Name (optional)", placeholder="e.g. john smith")
        dob = st.text_input("Date of Birth (optional)", placeholder="e.g. 15061990")

        st.markdown("**Word Sources**")
        use_common = st.checkbox("Common Passwords List", value=True)
        use_keyboard = st.checkbox("Keyboard Patterns", value=True)

        st.markdown("**Mutation Rules**")
        mc1, mc2, mc3 = st.columns(3)
        apply_leet = mc1.checkbox("Leetspeak", value=True)
        apply_case = mc2.checkbox("Case Vars", value=True)
        apply_suffix = mc3.checkbox("Suffixes", value=True)

    with col2:
        st.markdown("#### ℹ️ About Mutations")
        st.markdown("""
        <div class="result-info" style="font-size:0.82rem;">
        <strong style="color:#00e5ff;">Leetspeak</strong> — replaces letters with look-alikes:<br>
        &nbsp;&nbsp;<code>a→4/@</code> &nbsp;<code>e→3</code> &nbsp;<code>s→5/$</code> &nbsp;<code>o→0</code><br><br>
        <strong style="color:#00e5ff;">Case Variations</strong> — generates lowercase, UPPERCASE, Title, sWaPcAsE<br><br>
        <strong style="color:#00e5ff;">Suffixes</strong> — appends <code>1</code>, <code>123</code>, <code>!</code>, <code>2024</code>, etc.
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Generate Wordlist", use_container_width=True):
        with st.spinner("Generating wordlist..."):
            gen = DictionaryGenerator()
            wordlist = gen.build(
                name=name, dob=dob,
                use_common=use_common, use_keyboard=use_keyboard,
                leet=apply_leet, case=apply_case, suffixes=apply_suffix,
            )

        st.success(f"✅ Generated **{len(wordlist):,}** unique candidates")

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Words", f"{len(wordlist):,}")
        c2.metric("Sources Active", sum([bool(name and dob), use_common, use_keyboard]))
        c3.metric("Mutations On", sum([apply_leet, apply_case, apply_suffix]))

        st.markdown("#### 👁️ Preview (first 50 entries)")
        preview = wordlist[:50]
        st.code("\n".join(preview), language="text")

        # Save button
        if st.button("💾 Save Wordlist to File"):
            try:
                path = gen.save("data/generated_wordlist.txt")
                st.success(f"Saved to `{path}`")
            except Exception as e:
                st.error(f"Save failed: {e}")

        st.session_state["wordlist"] = wordlist


def page_hash():
    header("🔑", "Hash Handler & Dictionary Attack",
           "Generate hashes and simulate dictionary-based credential attacks")
    disclaimer()

    tab1, tab2 = st.tabs(["🔒 Hash Generator", "⚔️ Dictionary Attack"])

    # ── Tab 1: Hash Generator ──────────────────────────────────────────────────
    with tab1:
        st.markdown("#### Generate a Password Hash")
        col1, col2 = st.columns([2, 1])
        with col1:
            password_input = st.text_input("Password", type="password",
                                           placeholder="Enter password to hash")
            algo = st.selectbox("Algorithm", list(SUPPORTED_ALGORITHMS.keys()))

        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if password_input:
                hint_len = {32: "MD5", 40: "SHA-1", 64: "SHA-256", 128: "SHA-512"}
                st.markdown(f"""
                <div class="stat-pill">Length: {len(password_input)} chars</div>
                """, unsafe_allow_html=True)

        if st.button("Generate Hash", use_container_width=True):
            if not password_input:
                st.warning("Please enter a password.")
            else:
                try:
                    handler = HashHandler(algo)
                    h = handler.hash_password(password_input)
                    st.markdown("#### Result")
                    st.markdown(f"**Algorithm:** `{algo}` &nbsp;|&nbsp; **Hash length:** `{len(h)} chars`")
                    hash_display(h)
                    st.session_state["last_hash"] = h
                    st.session_state["last_algo"] = algo
                    st.info("💡 Hash saved to session — switch to Dictionary Attack tab to crack it.")
                except Exception as e:
                    st.error(f"Error: {e}")

    # ── Tab 2: Dictionary Attack ───────────────────────────────────────────────
    with tab2:
        st.markdown("#### Simulated Dictionary Attack")

        col1, col2 = st.columns([2, 1])
        with col1:
            target_hash = st.text_input(
                "Target Hash",
                value=st.session_state.get("last_hash", ""),
                placeholder="Paste MD5/SHA-256/SHA-512 hash here"
            )
            attack_algo = st.selectbox(
                "Hash Algorithm",
                list(SUPPORTED_ALGORITHMS.keys()),
                index=list(SUPPORTED_ALGORITHMS.keys()).index(
                    st.session_state.get("last_algo", "SHA-256")
                )
            )

        with col2:
            if target_hash:
                handler_hint = HashHandler(attack_algo)
                st.markdown(f"""
                <div class="result-info" style="font-size:0.82rem;">
                <strong>Auto-detect:</strong><br>
                {handler_hint.identify_algorithm_hint(target_hash)}
                </div>""", unsafe_allow_html=True)

        # Wordlist source
        wl_source = st.radio("Wordlist Source", ["Common Passwords (built-in)", "Session Wordlist (from Generator)"],
                             horizontal=True)

        speed_limit = st.slider("Max candidates to check", 100, 5000, 1000, step=100)

        if st.button("⚔️ Launch Dictionary Attack", use_container_width=True):
            if not target_hash:
                st.warning("Please provide a target hash.")
                return

            # Load wordlist
            if wl_source == "Session Wordlist (from Generator)":
                wordlist = st.session_state.get("wordlist", [])
                if not wordlist:
                    st.warning("No session wordlist found. Run the Dictionary Generator first.")
                    return
            else:
                gen = DictionaryGenerator()
                wordlist = gen.from_common_passwords()

            wordlist = wordlist[:speed_limit]

            handler = HashHandler(attack_algo)
            progress_bar = st.progress(0, text="Initializing attack...")
            status = st.empty()
            result_placeholder = st.empty()

            # Run attack with generator
            gen_obj = handler.dictionary_attack(target_hash, wordlist, max_attempts=speed_limit)
            crack_result = None
            last_progress = {}

            try:
                while True:
                    p = next(gen_obj)
                    last_progress = p
                    pct = p["progress_pct"]
                    progress_bar.progress(pct, text=f"Trying: `{p['current_word']}` — Attempt {p['attempts']:,}/{p['total']:,}")
                    time.sleep(0.001)  # slight delay for animation

                    if p.get("found"):
                        crack_result = {"found": True, "password": p["password"],
                                        "attempts": p["attempts"]}
                        break
            except StopIteration as e:
                crack_result = {"found": False, "attempts": last_progress.get("attempts", 0)}

            progress_bar.progress(1.0, text="Attack complete.")

            if crack_result and crack_result["found"]:
                result_placeholder.markdown(f"""
                <div class="result-success">
                <span style="font-size:1.5rem;">✅</span>
                <strong style="color:#00ff66;font-size:1.1rem;"> PASSWORD FOUND</strong><br><br>
                🔓 <strong>Plaintext:</strong> <code style="font-size:1rem;color:#00ff88;">{crack_result['password']}</code><br>
                📊 <strong>Attempts:</strong> {crack_result['attempts']:,}
                </div>""", unsafe_allow_html=True)
            else:
                result_placeholder.markdown(f"""
                <div class="result-fail">
                <span style="font-size:1.5rem;">❌</span>
                <strong style="color:#ff4444;"> NOT FOUND</strong><br><br>
                Checked {crack_result.get('attempts', 0):,} candidates without a match.<br>
                <small style="color:#aa4444;">Try a larger wordlist or different algorithm.</small>
                </div>""", unsafe_allow_html=True)


def page_brute_force():
    header("⚡", "Brute-Force Simulator",
           "Visualize character enumeration attacks with real-world time estimates")
    disclaimer()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### ⚙️ Character Set Selection")
        charset_options = list(BF_CHARSETS.keys())
        selected_charsets = st.multiselect(
            "Include character sets:",
            charset_options,
            default=["Lowercase (a-z)", "Digits (0-9)"]
        )

        target_length = st.slider("Target password length (for stats)", 1, 12, 4)

        st.markdown("#### 🎯 Live Simulation")
        sim_password = st.text_input("Demo password to find (max 5 chars)",
                                     placeholder="e.g. abc1 or dog",
                                     max_chars=5)
        max_attempts = st.slider("Max simulation attempts", 1000, 100_000, 20_000, step=1000)

    with col2:
        st.markdown("#### 📊 Estimated Attack Stats")
        if selected_charsets:
            engine = BruteForceEngine(selected_charsets, max_length=target_length)
            stats = engine.estimate_only(target_length)

            st.markdown(f"""
            <div class="card">
              <div style="font-family:'Share Tech Mono',monospace;font-size:0.8rem;color:#7aaddd;">
                CHARSET SIZE
              </div>
              <div style="font-size:2rem;color:#00e5ff;font-weight:800;">{stats['charset_size']}</div>
              <div style="font-size:0.75rem;color:#4a7aaa;">unique characters</div>
              <hr style="border-color:#1e3050;margin:0.8rem 0;">
              <div style="font-family:'Share Tech Mono',monospace;font-size:0.8rem;color:#7aaddd;">
                TOTAL COMBINATIONS (len 1–{target_length})
              </div>
              <div style="font-size:1.4rem;color:#ffcc00;font-weight:700;">{stats['total_combinations']:,}</div>
              <hr style="border-color:#1e3050;margin:0.8rem 0;">
              <div style="font-family:'Share Tech Mono',monospace;font-size:0.8rem;color:#7aaddd;">
                REAL-WORLD CRACK TIME (10B guesses/sec GPU)
              </div>
              <div style="font-size:1.3rem;color:#ff6644;font-weight:700;">{stats['real_world_estimate']}</div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("View charset"):
                st.code(stats["charset"], language="text")
        else:
            st.info("Select at least one character set.")

    st.divider()

    if st.button("⚡ Run Live Simulation", use_container_width=True):
        if not selected_charsets:
            st.warning("Select at least one character set.")
            return
        if not sim_password:
            st.warning("Enter a demo password to search for.")
            return
        if len(sim_password) > 5:
            st.warning("Keep demo password ≤ 5 characters for real-time simulation.")
            return

        # Check if password chars are in charset
        engine = BruteForceEngine(selected_charsets, max_length=len(sim_password))
        charset = engine.charset
        bad_chars = [c for c in sim_password if c not in charset]
        if bad_chars:
            st.warning(f"Characters `{''.join(bad_chars)}` not in selected charset. Add the right charset.")
            return

        progress_bar = st.progress(0, text="Starting brute-force simulation...")
        status_col1, status_col2, status_col3 = st.columns(3)
        attempts_display = status_col1.empty()
        speed_display = status_col2.empty()
        candidate_display = status_col3.empty()
        result_placeholder = st.empty()

        found = False
        last_p = {}
        gen = engine.simulate(sim_password, max_attempts=max_attempts)

        for p in gen:
            pct = min(p["attempts"] / max_attempts, 1.0)
            progress_bar.progress(pct)
            attempts_display.metric("Attempts", f"{p['attempts']:,}")
            speed_display.metric("Speed", f"{p['speed']:,.0f}/s")
            candidate_display.metric("Testing", f"`{p['candidate']}`")
            last_p = p
            time.sleep(0.0001)

            if p["found"]:
                found = True
                break

        if found:
            result_placeholder.markdown(f"""
            <div class="result-success">
            ✅ <strong style="color:#00ff66;font-size:1.1rem;">CRACKED!</strong><br><br>
            🔓 Password: <code style="color:#00ff88;font-size:1.1rem;">{sim_password}</code><br>
            📊 Attempts: <strong>{last_p['attempts']:,}</strong> &nbsp;|&nbsp;
            ⏱ Time: <strong>{last_p['elapsed']:.3f}s</strong> &nbsp;|&nbsp;
            🚀 Speed: <strong>{last_p['speed']:,.0f} guesses/sec</strong>
            </div>""", unsafe_allow_html=True)
            progress_bar.progress(1.0, text="✅ Password found!")
        else:
            result_placeholder.markdown(f"""
            <div class="result-fail">
            ❌ <strong style="color:#ff4444;">Not found</strong> within {max_attempts:,} attempts.<br>
            <small>Increase attempts or simplify the demo password.</small>
            </div>""", unsafe_allow_html=True)


def page_strength():
    header("🛡️", "Password Strength Analyzer",
           "Real-time entropy scoring, pattern detection & security recommendations")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### 🔍 Analyze a Password")
        password = st.text_input("Password", type="password",
                                 placeholder="Type any password to analyze...")
        show_plain = st.checkbox("Reveal password (for demo)")
        if show_plain and password:
            st.markdown(f"<code style='color:#00e5ff;'>{password}</code>", unsafe_allow_html=True)

    analyzer = StrengthAnalyzer()

    if password:
        report = analyzer.analyze(password)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### Strength Meter")
            st.markdown(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.3rem;">
              <span style="font-size:1.1rem;font-weight:700;color:{report.label_color};">{report.label}</span>
              <span style="font-family:'Share Tech Mono',monospace;color:{report.label_color};font-size:1.3rem;">
                {report.score}/100
              </span>
            </div>
            """, unsafe_allow_html=True)
            strength_bar(report.score, report.label_color)

        with col2:
            st.markdown("#### 📊 Metrics")

            mc1, mc2 = st.columns(2)
            mc1.metric("🔑 Entropy", f"{report.entropy_bits:.1f} bits")
            mc2.metric("🎲 Charset Size", f"{report.charset_size} chars")

            mc3, mc4 = st.columns(2)
            mc3.metric("📏 Length", f"{len(password)} chars")
            mc4.metric("⏱ Est. Crack Time", report.crack_time)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 🔬 Character Analysis")

            detail = report.details
            checks = [
                ("a–z lowercase", detail.get("has_lower")),
                ("A–Z uppercase", detail.get("has_upper")),
                ("0–9 digits", detail.get("has_digit")),
                ("!@# symbols", detail.get("has_symbol")),
            ]
            check_html = "".join([
                f'<span class="stat-pill">{"✅" if v else "❌"} {k}</span>'
                for k, v in checks
            ])
            st.markdown(check_html, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            flags = []
            if report.common_match:
                flags.append('<span class="stat-pill" style="border-color:#ff4444;color:#ff4444;">⚠️ Common Password</span>')
            if report.pattern_found:
                flags.append('<span class="stat-pill" style="border-color:#ff8800;color:#ff8800;">⚠️ Predictable Pattern</span>')
            if flags:
                st.markdown("".join(flags), unsafe_allow_html=True)

        # Score breakdown
        st.divider()
        st.markdown("#### 📈 Score Breakdown")
        sc1, sc2, sc3 = st.columns(3)
        sc1.metric("Length Score", f"{report.length_score}/100")
        sc2.metric("Diversity Score", f"{report.diversity_score}/100")
        sc3.metric("Entropy Score", f"{report.entropy_score}/100")

        # Suggestions
        st.markdown("#### 💡 Recommendations")
        for tip in report.suggestions:
            if "✅" in tip:
                st.success(tip)
            elif "⚠️" in tip:
                st.error(tip)
            else:
                st.info(tip)

    else:
        with col2:
            st.markdown("""
            <div class="result-info" style="margin-top:1.5rem;">
            <strong style="color:#00e5ff;">How scoring works:</strong><br><br>
            📏 <strong>Length (30%)</strong> — Longer is better. 16+ chars scores max.<br><br>
            🔀 <strong>Diversity (25%)</strong> — Points for each character class used.<br><br>
            🔢 <strong>Entropy (25%)</strong> — Bits of randomness. More = harder to crack.<br><br>
            📖 <strong>Dictionary check (10%)</strong> — Penalizes common passwords.<br><br>
            🔠 <strong>Patterns (10%)</strong> — Penalizes keyboard walks & sequences.
            </div>""", unsafe_allow_html=True)


# ─── Sidebar Navigation ───────────────────────────────────────────────────────

def sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:1rem 0 0.5rem;">
          <div style="font-family:'Share Tech Mono',monospace;color:#00e5ff;font-size:1.1rem;
                      letter-spacing:0.1em;">🔐 PASSSUITE</div>
          <div style="color:#2a4a6a;font-size:0.7rem;letter-spacing:0.2em;">v1.0.0 · EDUCATIONAL</div>
        </div>""", unsafe_allow_html=True)
        st.divider()

        st.markdown("<div style='color:#2a4a6a;font-size:0.7rem;letter-spacing:0.2em;padding:0 0.5rem 0.3rem;'>MODULES</div>",
                    unsafe_allow_html=True)

        page = st.radio(
            "Navigate",
            ["🏠 Home", "📋 Dictionary Generator", "🔑 Hash Handler", "⚡ Brute-Force", "🛡️ Strength Analyzer"],
            label_visibility="collapsed"
        )

        st.divider()
        st.markdown("""
        <div style="font-size:0.72rem;color:#2a4a6a;padding:0 0.5rem;line-height:1.6;">
          <strong style="color:#1e3a5a;">Stack:</strong><br>
          Python · Streamlit · hashlib<br>
          itertools · re · math<br><br>
          <strong style="color:#1e3a5a;">Author:</strong><br>
          Educational Demo Project<br><br>
          <strong style="color:#1e3a5a;">License:</strong><br>
          MIT — Learning use only
        </div>""", unsafe_allow_html=True)

    return page


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    page = sidebar()

    if page == "🏠 Home":
        page_home()
    elif page == "📋 Dictionary Generator":
        page_dictionary()
    elif page == "🔑 Hash Handler":
        page_hash()
    elif page == "⚡ Brute-Force":
        page_brute_force()
    elif page == "🛡️ Strength Analyzer":
        page_strength()


if __name__ == "__main__":
    main()
