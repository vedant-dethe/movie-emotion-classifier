# movie_emotion_classifier.py — Tkinter UI only, calls backend.py

import tkinter as tk
from tkinter import font as tkfont
from backend import predict, EMOTIONS

EXAMPLES = [
    "This movie was absolutely wonderful, loved every minute!",
    "I cried through the entire film, so heartbreaking.",
    "Worst movie ever made, complete waste of money.",
    "The film was shot in New Zealand and runs for 148 minutes.",
    "The performances were outstanding, truly a masterpiece!",
    "So boring, I wanted to walk out after 20 minutes.",
]

BG, PANEL, CARD = "#0B0F1A", "#131929", "#1A2035"
ORANGE, WHITE, MUTED, LIGHT, BORDER = "#FF5C00", "#FFFFFF", "#8A9BB5", "#E2E8F0", "#2A3350"

class EmotionApp:
    def __init__(self, root):
        self.root = root
        root.title("Movie Review Emotion Classifier")
        root.geometry("780x620")
        root.minsize(700, 560)
        root.configure(bg=BG)

        F = lambda s, b=False: tkfont.Font(family="Arial", size=s, weight="bold" if b else "normal")
        self.fb, self.fs, self.fl = F(11, True), F(9), F(11)
        self.fr, self.feg = F(26, True), F(9)
        self._build()

    def _build(self):
        hdr = tk.Frame(self.root, bg=PANEL, height=64)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🎬", bg=PANEL, fg=WHITE, font=tkfont.Font(size=22)).place(x=18, y=12)
        tk.Label(hdr, text="Movie Review  ", bg=PANEL, fg=WHITE, font=tkfont.Font(family="Arial", size=16, weight="bold")).place(x=58, y=8)
        tk.Label(hdr, text="Emotion Classifier", bg=PANEL, fg=ORANGE, font=tkfont.Font(family="Arial", size=16, weight="bold")).place(x=220, y=8)
        tk.Label(hdr, text="TF-IDF  •  SVM  •  NLP", bg=PANEL, fg=MUTED, font=self.fs).place(x=60, y=38)
        tk.Frame(self.root, bg=ORANGE, height=2).pack(fill="x")

        content = tk.Frame(self.root, bg=BG)
        content.pack(fill="both", expand=True, padx=20, pady=14)

        left = tk.Frame(content, bg=BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left, text="Enter a Movie Review", bg=BG, fg=LIGHT, font=self.fb).pack(anchor="w")
        tk.Label(left, text="Type or paste any movie review below", bg=BG, fg=MUTED, font=self.fs).pack(anchor="w", pady=(0, 6))

        inp = tk.Frame(left, bg=BORDER)
        inp.pack(fill="x")
        self.text_input = tk.Text(inp, height=7, wrap="word", bg=CARD, fg=WHITE,
            insertbackground=ORANGE, font=self.fl, relief="flat", bd=8,
            selectbackground=ORANGE, selectforeground=WHITE)
        self.text_input.pack(fill="x", padx=1, pady=1)
        self.text_input.bind("<Control-Return>", lambda e: self._predict())

        btn_row = tk.Frame(left, bg=BG)
        btn_row.pack(fill="x", pady=10)
        tk.Button(btn_row, text="Detect Emotion", command=self._predict, bg=ORANGE, fg=WHITE,
            font=self.fb, relief="flat", bd=0, padx=18, pady=8,
            activebackground="#CC4A00", activeforeground=WHITE, cursor="hand2").pack(side="left", padx=(0, 8))
        tk.Button(btn_row, text="Clear", command=self._clear, bg=CARD, fg=MUTED,
            font=self.fb, relief="flat", bd=0, padx=18, pady=8,
            activebackground=BORDER, activeforeground=WHITE, cursor="hand2").pack(side="left")
        tk.Label(btn_row, text="Ctrl+Enter to submit", bg=BG, fg=MUTED, font=self.fs).pack(side="right", padx=4)

        tk.Label(left, text="Examples", bg=BG, fg=MUTED, font=self.fb).pack(anchor="w", pady=(4, 4))
        eg = tk.Frame(left, bg=BG)
        eg.pack(fill="x")
        for i, ex in enumerate(EXAMPLES):
            short = ex[:38] + "..." if len(ex) > 38 else ex
            tk.Button(eg, text=short, bg=CARD, fg=MUTED, font=self.feg, relief="flat", bd=0,
                padx=6, pady=5, wraplength=170, justify="left",
                activebackground=BORDER, activeforeground=LIGHT, cursor="hand2",
                command=lambda e=ex: self._load(e)).grid(row=i//2, column=i%2, sticky="ew", padx=3, pady=2)
        eg.columnconfigure(0, weight=1)
        eg.columnconfigure(1, weight=1)

        right = tk.Frame(content, bg=CARD, width=240)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)
        tk.Frame(right, bg=ORANGE, height=4).pack(fill="x")
        tk.Label(right, text="Detected Emotion", bg=CARD, fg=MUTED, font=self.fs).pack(pady=(12, 0))

        self.emoji_var = tk.StringVar(value="🎬")
        tk.Label(right, textvariable=self.emoji_var, bg=CARD, fg=WHITE, font=tkfont.Font(family="Arial", size=52)).pack(pady=(10, 0))

        self.result_var = tk.StringVar(value="—")
        self.result_lbl = tk.Label(right, textvariable=self.result_var, bg=CARD, fg=ORANGE, font=self.fr)
        self.result_lbl.pack(pady=(4, 0))
        tk.Frame(right, bg=BORDER, height=1).pack(fill="x", padx=20, pady=10)

        self.desc_var = tk.StringVar(value="Enter a review and\nclick Detect Emotion")
        tk.Label(right, textvariable=self.desc_var, bg=CARD, fg=LIGHT, font=self.fs, wraplength=190, justify="center").pack(padx=16)

        self.status_var = tk.StringVar(value="Ready")
        bar = tk.Frame(self.root, bg=PANEL, height=24)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        tk.Label(bar, textvariable=self.status_var, bg=PANEL, fg=MUTED, font=self.fs).pack(side="left", padx=12, pady=4)

    def _predict(self):
        review = self.text_input.get("1.0", "end").strip()
        if not review:
            self.status_var.set("Please enter a review first.")
            return
        self.status_var.set("Analyzing...")
        self.root.update()
        emoji, label, color, desc = predict(review)
        self.emoji_var.set(emoji)
        self.result_var.set(label)
        self.result_lbl.config(fg=color)
        self.desc_var.set(desc)
        self.status_var.set(f"Predicted: {label}")

    def _clear(self):
        self.text_input.delete("1.0", "end")
        self.emoji_var.set("🎬")
        self.result_var.set("—")
        self.result_lbl.config(fg=ORANGE)
        self.desc_var.set("Enter a review and\nclick Detect Emotion")
        self.status_var.set("Cleared")

    def _load(self, text):
        self.text_input.delete("1.0", "end")
        self.text_input.insert("1.0", text)
        self.status_var.set("Example loaded — click Detect Emotion")

if __name__ == "__main__":
    root = tk.Tk()
    EmotionApp(root)
    root.mainloop()


