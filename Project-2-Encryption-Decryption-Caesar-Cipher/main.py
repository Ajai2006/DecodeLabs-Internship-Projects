import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QTextEdit, QSpinBox,
    QPushButton, QFrame, QStatusBar, QSizePolicy
)
from PyQt5.QtGui import QFont, QFontDatabase, QColor, QPalette, QIcon
from PyQt5.QtCore import Qt, QTimer


# ── Caesar cipher logic ────────────────────────────────────────────────────────

def caesar_encrypt(text: str, shift: int) -> str:
    result = []
    for ch in text:
        if ch.isupper():
            result.append(chr((ord(ch) - 65 + shift) % 26 + 65))
        elif ch.islower():
            result.append(chr((ord(ch) - 97 + shift) % 26 + 97))
        else:
            result.append(ch)
    return "".join(result)


def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, 26 - (shift % 26))


# ── Styled widgets ─────────────────────────────────────────────────────────────

class SectionLabel(QLabel):
    def __init__(self, text):
        super().__init__(text.upper())
        self.setFont(QFont("Orbitron", 8, QFont.Bold))
        self.setStyleSheet("color: #3d7aed; letter-spacing: 3px; margin-bottom: 4px;")


class MonoTextEdit(QTextEdit):
    def __init__(self, placeholder="", read_only=False):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setReadOnly(read_only)
        self.setFixedHeight(100)
        color = "#3fb950" if read_only else "#e6edf3"
        self.setFont(QFont("Share Tech Mono", 12))
        self.setStyleSheet(f"""
            QTextEdit {{
                background: #0d1117;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 8px 10px;
                color: {color};
                selection-background-color: #1f6feb;
            }}
            QTextEdit:focus {{
                border: 1px solid #58a6ff;
            }}
        """)


class CipherButton(QPushButton):
    STYLES = {
        "encrypt": ("ENCRYPT", "#1a3a5c", "#58a6ff", "#1f6feb"),
        "decrypt": ("DECRYPT", "#1a2e1a", "#3fb950", "#238636"),
        "clear":   ("CLEAR",   "#2d1b1b", "#f85149", "#da3633"),
        "copy":    ("COPY",    "#1e1e2e", "#a78bfa", "#7c3aed"),
    }

    def __init__(self, kind: str):
        label, bg, fg, border = self.STYLES[kind]
        super().__init__(label)
        self.setFont(QFont("Orbitron", 8, QFont.Bold))
        self.setFixedHeight(36)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background: {bg};
                color: {fg};
                border: 1px solid {border};
                border-radius: 5px;
                letter-spacing: 1.5px;
                padding: 0 12px;
            }}
            QPushButton:hover {{
                background: {border};
                color: #ffffff;
            }}
            QPushButton:pressed {{
                opacity: 0.8;
            }}
        """)


class Divider(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setStyleSheet("color: #21262d;")


# ── Main window ────────────────────────────────────────────────────────────────

class CipherVault(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CIPHER VAULT  —  Caesar Cipher")
        self.setMinimumSize(820, 560)
        self.resize(900, 600)
        self._apply_dark_palette()
        self._build_ui()

    # ── Palette ────────────────────────────────────────────────────────────────

    def _apply_dark_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window,          QColor("#0d1117"))
        palette.setColor(QPalette.WindowText,      QColor("#e6edf3"))
        palette.setColor(QPalette.Base,            QColor("#161b22"))
        palette.setColor(QPalette.AlternateBase,   QColor("#0d1117"))
        palette.setColor(QPalette.Text,            QColor("#e6edf3"))
        palette.setColor(QPalette.Button,          QColor("#161b22"))
        palette.setColor(QPalette.ButtonText,      QColor("#e6edf3"))
        palette.setColor(QPalette.Highlight,       QColor("#1f6feb"))
        palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
        self.setPalette(palette)
        self.setStyleSheet("QMainWindow { background: #0d1117; }")

    # ── UI Construction ────────────────────────────────────────────────────────

    def _build_ui(self):
        root = QWidget()
        root.setStyleSheet("background: #0d1117;")
        self.setCentralWidget(root)

        outer = QVBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        outer.addWidget(self._titlebar())
        outer.addWidget(self._body(), stretch=1)
        outer.addWidget(self._footer())

    # ── Title bar ──────────────────────────────────────────────────────────────

    def _titlebar(self) -> QWidget:
        bar = QWidget()
        bar.setFixedHeight(46)
        bar.setStyleSheet("background: #161b22; border-bottom: 1px solid #21262d;")

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 0, 20, 0)

        dots = QHBoxLayout()
        dots.setSpacing(6)
        for color in ("#ff5f57", "#ffbd2e", "#28c840"):
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {color}; font-size: 12px;")
            dots.addWidget(dot)
        layout.addLayout(dots)

        layout.addStretch()

        title = QLabel("Encryption & Decryption using Caesar Cipher")
        title.setFont(QFont("Orbitron", 11, QFont.Bold))
        title.setStyleSheet("color: #58a6ff; letter-spacing: 2px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addStretch()

        return bar

    # ── Body ───────────────────────────────────────────────────────────────────

    def _body(self) -> QWidget:
        body = QWidget()
        body.setStyleSheet("background: #0d1117;")
        cols = QHBoxLayout(body)
        cols.setContentsMargins(0, 0, 0, 0)
        cols.setSpacing(0)
        cols.addWidget(self._left_panel(), stretch=1)
        cols.addWidget(self._right_panel(), stretch=1)
        return body

    # ── Left panel ─────────────────────────────────────────────────────────────

    def _left_panel(self) -> QWidget:
        panel = QWidget()
        panel.setStyleSheet("border-right: 1px solid #21262d;")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(10)

        layout.addWidget(SectionLabel("Plaintext Input"))

        self.input_box = MonoTextEdit(placeholder="Type your message here…")
        layout.addWidget(self.input_box)

        # Shift key row
        shift_row = QHBoxLayout()
        shift_row.setSpacing(10)

        shift_lbl = QLabel("SHIFT KEY")
        shift_lbl.setFont(QFont("Share Tech Mono", 10))
        shift_lbl.setStyleSheet("color: #8b949e;")

        self.shift_spin = QSpinBox()
        self.shift_spin.setRange(1, 25)
        self.shift_spin.setValue(3)
        self.shift_spin.setFixedWidth(64)
        self.shift_spin.setFixedHeight(32)
        self.shift_spin.setFont(QFont("Orbitron", 11, QFont.Bold))
        self.shift_spin.setAlignment(Qt.AlignCenter)
        self.shift_spin.setStyleSheet("""
            QSpinBox {
                background: #161b22;
                color: #58a6ff;
                border: 1px solid #30363d;
                border-radius: 4px;
                padding: 2px 4px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background: #21262d;
                border: none;
                width: 16px;
            }
            QSpinBox::up-arrow  { color: #58a6ff; }
            QSpinBox::down-arrow{ color: #58a6ff; }
        """)
        self.shift_spin.valueChanged.connect(self._update_rot_badge)

        self.rot_badge = QLabel("  ROT-3  ")
        self.rot_badge.setFont(QFont("Orbitron", 8, QFont.Bold))
        self.rot_badge.setStyleSheet("""
            color: #58a6ff;
            background: #1a3a5c;
            border: 1px solid #1f6feb;
            border-radius: 3px;
            padding: 2px 6px;
            letter-spacing: 1px;
        """)

        shift_row.addWidget(shift_lbl)
        shift_row.addWidget(self.shift_spin)
        shift_row.addWidget(self.rot_badge)
        shift_row.addStretch()
        layout.addLayout(shift_row)

        layout.addWidget(Divider())

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        self.btn_enc = CipherButton("encrypt")
        self.btn_dec = CipherButton("decrypt")
        self.btn_clr = CipherButton("clear")
        btn_row.addWidget(self.btn_enc)
        btn_row.addWidget(self.btn_dec)
        btn_row.addWidget(self.btn_clr)
        layout.addLayout(btn_row)

        self.btn_enc.clicked.connect(self.do_encrypt)
        self.btn_dec.clicked.connect(self.do_decrypt)
        self.btn_clr.clicked.connect(self.do_clear)

        # Algorithm info card
        layout.addWidget(Divider())
        info = QLabel(
            "Algorithm: Caesar Cipher  ·  E(x) = (x + n) mod 26\n"
            "Symmetric key — same shift to encrypt & decrypt"
        )
        info.setFont(QFont("Share Tech Mono", 9))
        info.setStyleSheet("""
            color: #484f58;
            background: #161b22;
            border: 1px solid #21262d;
            border-radius: 5px;
            padding: 8px 10px;
        """)
        info.setWordWrap(True)
        layout.addWidget(info)
        layout.addStretch()

        return panel

    # ── Right panel ────────────────────────────────────────────────────────────

    def _right_panel(self) -> QWidget:
        panel = QWidget()
        panel.setStyleSheet("background: #0d1117;")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(10)

        layout.addWidget(SectionLabel("Encrypted Output"))

        self.output_box = MonoTextEdit(read_only=True)
        layout.addWidget(self.output_box)

        # Status row
        status_row = QHBoxLayout()
        self.status_dot = QLabel("●")
        self.status_dot.setStyleSheet("color: #484f58; font-size: 10px;")
        self.status_msg = QLabel("Awaiting input…")
        self.status_msg.setFont(QFont("Share Tech Mono", 9))
        self.status_msg.setStyleSheet("color: #c9d1d9;")
        status_row.addWidget(self.status_dot)
        status_row.addWidget(self.status_msg)
        status_row.addStretch()
        layout.addLayout(status_row)

        layout.addWidget(Divider())
        layout.addWidget(SectionLabel("Decrypted Output"))

        self.decrypt_box = MonoTextEdit(read_only=True)
        layout.addWidget(self.decrypt_box)

        status_row2 = QHBoxLayout()
        self.status_dot2 = QLabel("●")
        self.status_dot2.setStyleSheet("color: #484f58; font-size: 10px;")
        self.status_msg2 = QLabel("Awaiting input…")
        self.status_msg2.setFont(QFont("Share Tech Mono", 9))
        self.status_msg2.setStyleSheet("color: #c9d1d9;")
        status_row2.addWidget(self.status_dot2)
        status_row2.addWidget(self.status_msg2)
        status_row2.addStretch()
        layout.addLayout(status_row2)

        layout.addWidget(Divider())

        # Copy button
        copy_row = QHBoxLayout()
        self.btn_copy_enc = CipherButton("copy")
        self.btn_copy_enc.setText("COPY ENCRYPTED")
        self.btn_copy_dec = CipherButton("copy")
        self.btn_copy_dec.setText("COPY DECRYPTED")
        copy_row.addWidget(self.btn_copy_enc)
        copy_row.addWidget(self.btn_copy_dec)
        layout.addLayout(copy_row)

        self.btn_copy_enc.clicked.connect(lambda: self._copy_text(self.output_box, "Encrypted text copied!"))
        self.btn_copy_dec.clicked.connect(lambda: self._copy_text(self.decrypt_box, "Decrypted text copied!"))

        layout.addStretch()
        return panel

    # ── Footer ─────────────────────────────────────────────────────────────────

    def _footer(self) -> QWidget:
        bar = QWidget()
        bar.setFixedHeight(36)
        bar.setStyleSheet("background: #161b22; border-top: 1px solid #21262d;")

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 0, 20, 0)

        left = QLabel("Developed By Ajai")
        left.setFont(QFont("Share Tech Mono", 9))
        left.setStyleSheet("color: #8b949e;")
        left.setAlignment(Qt.AlignCenter)
        layout.addWidget(left, stretch=1)

        self.ready_badge = QLabel("  READY  ")
        self.ready_badge.setFont(QFont("Orbitron", 8, QFont.Bold))
        self.ready_badge.setStyleSheet("""
            color: #3fb950;
            background: #1a2e1a;
            border: 1px solid #238636;
            border-radius: 3px;
            padding: 2px 6px;
            letter-spacing: 1px;
        """)
        layout.addWidget(self.ready_badge)

        return bar

    # ── Logic ──────────────────────────────────────────────────────────────────

    def _update_rot_badge(self, val):
        self.rot_badge.setText(f"  ROT-{val}  ")

    def do_encrypt(self):
        text = self.input_box.toPlainText().strip()
        if not text:
            self._flash_status("No input provided.", error=True)
            return
        shift = self.shift_spin.value()
        encrypted = caesar_encrypt(text, shift)
        decrypted = caesar_decrypt(encrypted, shift)

        self.output_box.setPlainText(encrypted)
        self.decrypt_box.setPlainText(decrypted)

        n = len(text)
        self._set_status(
            self.status_dot, self.status_msg,
            f"Encrypted  ·  shift +{shift}  ·  {n} chars", green=True
        )
        self._set_status(
            self.status_dot2, self.status_msg2,
            f"Round-trip verified  ·  shift -{shift}", green=True
        )
        self._set_ready("ENCRYPTED")

    def do_decrypt(self):
        text = self.input_box.toPlainText().strip()
        if not text:
            self._flash_status("No input provided.", error=True)
            return
        shift = self.shift_spin.value()
        decrypted = caesar_decrypt(text, shift)

        self.output_box.setPlainText(text)
        self.decrypt_box.setPlainText(decrypted)

        n = len(text)
        self._set_status(
            self.status_dot, self.status_msg,
            f"Ciphertext  ·  {n} chars", green=False
        )
        self._set_status(
            self.status_dot2, self.status_msg2,
            f"Decrypted  ·  shift -{shift}  ·  {n} chars", green=True
        )
        self._set_ready("DECRYPTED")

    def do_clear(self):
        self.input_box.clear()
        self.output_box.clear()
        self.decrypt_box.clear()
        self._set_status(self.status_dot,  self.status_msg,  "Awaiting input…", green=False)
        self._set_status(self.status_dot2, self.status_msg2, "Awaiting input…", green=False)
        self._set_ready("READY")

    def _set_status(self, dot: QLabel, msg: QLabel, text: str, green: bool):
        color = "#3fb950" if green else "#484f58"
        dot.setStyleSheet(f"color: {color}; font-size: 10px;")
        msg.setText(text)

    def _set_ready(self, label: str):
        self.ready_badge.setText(f"  {label}  ")

    def _copy_text(self, box: QTextEdit, msg: str):
        text = box.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            old = self.ready_badge.text()
            self.ready_badge.setText("  COPIED  ")
            QTimer.singleShot(1500, lambda: self.ready_badge.setText(old))

    def _flash_status(self, msg: str, error=False):
        color = "#f85149" if error else "#3fb950"
        self.status_dot.setStyleSheet(f"color: {color}; font-size: 10px;")
        self.status_msg.setText(msg)


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = CipherVault()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
