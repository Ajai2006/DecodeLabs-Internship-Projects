import customtkinter as ctk
import re
import math

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

TITLE_FONT    = ("Orbitron", 24, "bold")
SUBTITLE_FONT = ("Orbitron", 14, "bold")
BODY_FONT     = ("Share Tech", 15)
MONO_FONT     = ("Source Code Pro", 13)
FOOTER_FONT   = ("Share Tech", 12)

COMMON_PASSWORDS = {
    "password", "password123", "123456", "12345678",
    "qwerty", "admin", "welcome", "letmein"
}

BG_DARK    = "#0d1117"
PANEL_BG   = "#111827"
ACCENT     = "#4DA3FF"
GREEN      = "#32D74B"
RED        = "#FF3B30"
YELLOW     = "#FFD60A"
TEXT_MAIN  = "#FFFFFF"
TEXT_MUTED = "#FFFFFF"


def calculate_entropy(password):
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"\d",    password): charset += 10
    if re.search(r"[^A-Za-z0-9]", password): charset += 32
    if charset == 0:
        return 0.0
    return round(len(password) * math.log2(charset), 2)


def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.configure(show="")
        toggle_button.configure(text="  👁  HIDE PASSWORD")
    else:
        password_entry.configure(show="*")
        toggle_button.configure(text="  👁  SHOW PASSWORD")


def analyze_password(event=None):
    password = password_entry.get()

    if not password:
        strength_label.configure(text="STRENGTH: —", text_color=TEXT_MUTED)
        progress_bar.set(0)
        entropy_label.configure(text="Entropy : 0 bits")
        checklist_label.configure(text="Waiting for password...")
        suggestions_text.configure(
        text="Enter a password to begin analysis...",
        text_color="#FFFFFF")
        return

    lower  = bool(re.search(r"[a-z]", password))
    upper  = bool(re.search(r"[A-Z]", password))
    digit  = bool(re.search(r"\d",    password))
    symbol = bool(re.search(r"[^A-Za-z0-9]", password))
    len8   = len(password) >= 8
    len12  = len(password) >= 12

    score = 0
    if password.lower() in COMMON_PASSWORDS:
        score = 5
        strength = "VERY WEAK"
        color = RED
    else:
        if len8:   score += 20
        if len12:  score += 20
        if lower:  score += 15
        if upper:  score += 15
        if digit:  score += 15
        if symbol: score += 15

        if score < 40:
            strength = "WEAK"
            color = RED
        elif score < 80:
            strength = "MEDIUM"
            color = YELLOW
        else:
            strength = "STRONG"
            color = GREEN

    strength_label.configure(text=f"STRENGTH: {strength}", text_color=color)
    progress_bar.set(score / 100)
    progress_bar.configure(progress_color=color)
    entropy_label.configure(text=f"Entropy: {calculate_entropy(password)} bits")

    def yn(flag): return ("✅ YES" if flag else "❌  NO ")

    checklist_text = (
        f"  {yn(len8)}    Length >= 8\n"
        f"  {yn(len12)}    Length >= 12\n"
        f"  {yn(upper)}    Uppercase\n"
        f"  {yn(lower)}    Lowercase\n"
        f"  {yn(digit)}    Number\n"
        f"  {yn(symbol)}    Special Symbol"
    )
    checklist_label.configure(text=checklist_text)

    suggestions = []
    if not len8:   suggestions.append("• Use at least 8 characters")
    if not len12:  suggestions.append("• Use 12+ characters")
    if not upper:  suggestions.append("• Add uppercase letters")
    if not lower:  suggestions.append("• Add lowercase letters")
    if not digit:  suggestions.append("• Add numbers")
    if not symbol: suggestions.append("• Add special characters")

    if password.lower() in COMMON_PASSWORDS:
        suggestions = [
            "• Common password detected",
            "• Choose a unique password"
        ]

    if not suggestions:
        suggestions_text.configure(
            text="✅  Excellent Password!\n\nNo improvements required.",
            text_color=GREEN
        )
    else:
        suggestions_text.configure(
            text="\n".join(suggestions),
            text_color=TEXT_MAIN
        )


# ── App window ───────────────────────────────────────────────────────────────
app = ctk.CTk()
app.title("Password Strength Checker")
app.geometry("1000x750")
app.resizable(False, False)
app.configure(fg_color=BG_DARK)

# Title
title_label = ctk.CTkLabel(
    app, text="🔐  PASSWORD STRENGTH CHECKER",
    font=TITLE_FONT, text_color=ACCENT
)
title_label.pack(pady=(28, 6))

# Password entry
password_entry = ctk.CTkEntry(
    app, width=600, height=55, show="*",
    font=("Share Tech", 15),
    fg_color="#1c2333", border_color="#2d3748",
    text_color=TEXT_MAIN,
    placeholder_text="Enter Your Password",
    placeholder_text_color="#4b5563"
)
password_entry.pack(pady=24)
password_entry.bind("<KeyRelease>", analyze_password)

# Toggle button
toggle_button = ctk.CTkButton(
    app, text="  👁  SHOW PASSWORD",
    width=220, height=45,
    fg_color="#2563eb", hover_color="#1d4ed8",
    font=("Orbitron", 11, "bold"),
    command=toggle_password
)
toggle_button.pack()

# Strength label
strength_label = ctk.CTkLabel(
    app, text="STRENGTH : —",
    font=SUBTITLE_FONT, text_color=TEXT_MUTED
)
strength_label.pack(pady=(20, 10))

# Progress bar
progress_bar = ctk.CTkProgressBar(
    app, width=700, height=18,
    fg_color="#1c2333", progress_color=GREEN,
    corner_radius=9
)
progress_bar.pack(pady=4)
progress_bar.set(0)

# Entropy label
entropy_label = ctk.CTkLabel(
    app, text="Entropy : 0 bits",
    font=BODY_FONT, text_color=TEXT_MAIN
)
entropy_label.pack(pady=14)

# ── Dashboard row ─────────────────────────────────────────────────────────────
dashboard_frame = ctk.CTkFrame(app, fg_color="transparent")
dashboard_frame.pack(pady=10, padx=40, fill="x")

# Left panel – Security Checklist
frame1 = ctk.CTkFrame(
    dashboard_frame, fg_color=PANEL_BG,
    corner_radius=15, border_width=1, border_color="#1f2937"
)
frame1.pack(side="left", padx=(0, 16), fill="both", expand=True)

checklist_title = ctk.CTkLabel(
    frame1, text="🛡  SECURITY CHECKLIST",
    font=SUBTITLE_FONT, text_color=ACCENT
)
checklist_title.pack(pady=(18, 6))

ctk.CTkFrame(frame1, fg_color="#1f2937", height=1).pack(fill="x")

checklist_label = ctk.CTkLabel(
    frame1,
    text="Waiting for password...",
    font=BODY_FONT,
    justify="left",
    text_color="#FFFFFF"
)
checklist_label.pack(anchor="w", padx=24, pady=18)

# Right panel – Security Suggestions
frame2 = ctk.CTkFrame(
    dashboard_frame, fg_color=PANEL_BG,
    corner_radius=15, border_width=1, border_color="#1f2937"
)
frame2.pack(side="right", padx=(16, 0), fill="both", expand=True)

suggestion_title = ctk.CTkLabel(
    frame2, text="💡  SECURITY SUGGESTIONS",
    font=SUBTITLE_FONT, text_color=ACCENT
)
suggestion_title.pack(pady=(18, 6))

ctk.CTkFrame(frame2, fg_color="#1f2937", height=1).pack(fill="x")

suggestions_text = ctk.CTkLabel(
    frame2,
    text="Enter a password to begin analysis...",
    font=BODY_FONT,
    justify="left",
    wraplength=300,
    text_color="#FFFFFF"
)
suggestions_text.pack(anchor="w", padx=24, pady=18)

# Footer
footer = ctk.CTkLabel(
    app,
    text="🔒  STAY SAFE. USE STRONG PASSWORDS.\n\nDeveloped by Ajai",
    font=FOOTER_FONT, text_color=ACCENT
)
footer.pack(side="bottom", pady=20)

app.mainloop()
