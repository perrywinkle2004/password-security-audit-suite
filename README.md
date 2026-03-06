# 🔐 PassSuite — Password Cracking & Credential Attack Suite

> **Educational Simulation Tool** — 100% local, no real system access

A professional, modular cybersecurity lab built with Python and Streamlit demonstrating
dictionary attacks, brute-force simulation, hash analysis, and password strength evaluation.

---

## 📁 Project Structure

```
password_suite/
│
├── app.py                          # Main Streamlit application
├── requirements.txt
├── README.md
│
├── modules/
│   ├── dictionary_generator.py     # Wordlist generation + mutation engine
│   ├── hash_handler.py             # Hashing + dictionary attack simulation
│   ├── brute_force.py              # Brute-force enumeration simulator
│   └── strength_analyzer.py        # Password strength & entropy analysis
│
├── utils/
│   ├── entropy.py                  # Entropy calculation utilities
│   └── logger.py                   # Centralized logging
│
└── data/
    ├── common_passwords.txt        # Built-in wordlist (80+ entries)
    └── generated_wordlist.txt      # Auto-generated (after running generator)
```

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the application

```bash
cd password_suite
streamlit run app.py
```

The app will open at **[PASSSUITE](https://password-security-audit-suite-dxrksrwvca2ryjptednqmr.streamlit.app/)**

---

## 🧩 Modules

### 📋 Dictionary Generator
Generate candidate wordlists from:
- **Name + DOB patterns** — `john15061990`, `JOHN1990`, etc.
- **Common passwords** — 80+ pre-loaded entries
- **Keyboard patterns** — `qwerty`, `1qaz2wsx`, etc.

Mutation rules:
- **Leetspeak** — `a→4/@`, `e→3`, `s→5/$`
- **Case variations** — lower / UPPER / Title / sWaP
- **Suffixes** — appends `123`, `!`, `2024`, `@` etc.

### 🔑 Hash Handler
- Hash any password with MD5, SHA-1, SHA-256, SHA-512
- Run a **simulated dictionary attack** against a hash
- Animated progress with live candidate display

### ⚡ Brute-Force Simulator
- Select character sets (lowercase, uppercase, digits, symbols)
- View total combinations & real-world crack time estimates
- **Live animation** of enumeration against a short demo password

### 🛡️ Strength Analyzer
- Real-time entropy calculation
- Character diversity scoring
- Dictionary match detection
- Pattern detection (sequences, keyboard walks, repeats)
- Score breakdown + improvement suggestions

---

## 🎮 Sample Demo Inputs

### Dictionary Generator
| Field | Sample Value |
|---|---|
| Name | `john smith` |
| DOB | `15061990` |
| Sources | Common Passwords ✅, Keyboard Patterns ✅ |
| Mutations | Leetspeak ✅, Case ✅, Suffixes ✅ |

### Hash Handler
| Field | Sample Value |
|---|---|
| Password | `password123` |
| Algorithm | `SHA-256` |
| Attack | Paste generated hash → Dictionary attack |

### Brute-Force
| Field | Sample Value |
|---|---|
| Charsets | Lowercase + Digits |
| Target Length | 4 |
| Demo Password | `ab12` |

### Strength Analyzer
Try these to see different ratings:
- `abc` → **Weak**
- `hello2024` → **Moderate**
- `MyP@ss#2024` → **Strong**
- `xK#9!mP2@vLq$8nZ` → **Very Strong**

---

## ⚠️ Disclaimer

This tool is **strictly educational**. It:
- Runs entirely locally with no network access
- Does not exploit any real systems
- Does not dump credentials from the OS
- Does not contain real malware or attack code

Use this knowledge responsibly. Unauthorized access to computer systems is illegal.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| UI | Streamlit |
| Hashing | `hashlib` (stdlib) |
| Enumeration | `itertools` (stdlib) |
| Entropy | `math` (stdlib) |
| Pattern matching | `re` (stdlib) |
| Logging | `logging` (stdlib) |

---

## 📜 License

MIT License — for educational and portfolio use only.
