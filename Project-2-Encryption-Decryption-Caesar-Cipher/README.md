# 🔐 Project 2 — Encryption & Decryption using Caesar Cipher

**DecodeLabs Industrial Training Kit | Batch 2026**
**Developed by:** Ajai
**Domain:** Cyber Security
**Framework:** PyQt5 (Python Desktop GUI)

---

## 📌 Project Overview

This project implements a **Caesar Cipher** based encryption and decryption tool
with a professional dark-themed desktop GUI built using PyQt5.

The Caesar Cipher is a classical substitution cipher where each letter in the
plaintext is shifted by a fixed number of positions in the alphabet. This project
demonstrates the core concept of **data confidentiality** — the foundation of
modern cryptography.

---

## 🎯 Objectives

- Implement Caesar Cipher encryption logic using modular arithmetic
- Implement Caesar Cipher decryption as the reverse shift operation
- Build a professional dark-themed GUI using PyQt5
- Handle edge cases: spaces, punctuation, numbers (passed through unchanged)
- Provide real-time status feedback and clipboard copy support

---

## 🧠 Algorithm

### Encryption
```
E(x) = (x + n) mod 26
```

### Decryption
```
D(x) = (x - n) mod 26
```

Where:
- `x` = character position (0–25)
- `n` = shift key (1–25)

### Example (Shift = 3)
```
Plaintext:   H  E  L  L  O
ASCII:       72 69 76 76 79
Shift +3:    75 72 79 79 82
Ciphertext:  K  H  O  O  R
```

---

## 🖥️ Features

| Feature | Description |
|---|---|
| Encrypt | Encrypts plaintext using the chosen shift key |
| Decrypt | Decrypts ciphertext back to plaintext |
| Shift Key | User-selectable shift from 1 to 25 |
| ROT Badge | Live badge updates (ROT-1 to ROT-25) |
| Copy Buttons | Copy encrypted or decrypted output to clipboard |
| Status Bar | Real-time feedback on operation and character count |
| Clear | Resets all input and output fields |

---

## 🗂️ Project Structure

```
Project-2-Encryption-Decryption-Caesar-Cipher/
│
├── main.py               # Main application source code
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation (this file)
│
├── screenshot/           # App screenshots
│   └── app_preview.png
│
└── report/               # Project report
    └── Project2_Report.md
```

---

## ⚙️ Setup & Run

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Install fonts (Windows)
Download and install these fonts from [fonts.google.com](https://fonts.google.com):
- **Orbitron** — titles and labels
- **Share Tech Mono** — input/output text
- **Inter** — status messages

Right-click each `.ttf` file → **Install for all users**

### Step 3 — Run the application
```bash
python main.py
```

---

## 🎨 UI Design

| Element | Value |
|---|---|
| Background | `#0d1117` |
| Surface | `#161b22` |
| Accent Blue | `#58a6ff` |
| Accent Green | `#3fb950` |
| Accent Red | `#f85149` |
| Title Font | Orbitron Bold |
| I/O Font | Share Tech Mono |
| Status Font | Inter |

---

## ⚠️ Limitations

- Caesar Cipher has only **25 possible keys** — vulnerable to brute force
- **Frequency analysis** can break it without knowing the key
- Uppercase and lowercase letters are shifted independently
- Non-alphabetic characters (spaces, numbers, symbols) are **not encrypted**

---

## 🔭 Future Improvements

- Add **Vigenère Cipher** support (keyword-based multi-shift)
- Add **brute force attack demo** (show all 25 decryptions)
- Add **frequency analysis visualiser**
- Export encrypted output to `.txt` file

---

## 📚 Key Concepts Demonstrated

- `ord()` — converts a character to its ASCII integer value
- `chr()` — converts an integer back to a character
- **Modular arithmetic** (`% 26`) — handles alphabet wrap-around
- **Symmetric encryption** — same key is used to both encrypt and decrypt
- **IPO model** — Input → Process → Output architecture

---

## 🏢 About DecodeLabs

**DecodeLabs** | Greater Lucknow, India
📧 decodelabs.tech@gmail.com
🌐 www.decodelabs.tech
📞 +91 89330 06408
