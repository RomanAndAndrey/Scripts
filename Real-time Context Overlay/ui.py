import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ContextOverlay(ctk.CTk):
    def __init__(self, clear_callback):
        super().__init__()

        self.clear_callback = clear_callback

        # Window configuration
        self.title("Context Overlay")
        self.geometry("400x300")
        self.overrideredirect(True)  # Remove title bar and borders
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-alpha", 0.85)  # Semi-transparent

        # Position in top-right corner
        screen_width = self.winfo_screenwidth()
        # screen_height = self.winfo_screenheight()
        x_pos = screen_width - 420
        y_pos = 20
        self.geometry(f"400x320+{x_pos}+{y_pos}")

        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Bullets area
        self.grid_rowconfigure(1, weight=0)  # Button area

        # Bullets Frame
        self.bullets_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bullets_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Labels for bullets
        self.bullet_labels = []
        for i in range(3):
            lbl = ctk.CTkLabel(
                self.bullets_frame,
                text=f"",
                font=("Arial", 16, "bold"),
                anchor="w",
                justify="left",
                wraplength=380,
            )
            lbl.pack(fill="x", pady=5, anchor="w")
            self.bullet_labels.append(lbl)

        # Clear Button
        self.clear_btn = ctk.CTkButton(
            self,
            text="Очистить",
            command=self.on_clear,
            fg_color="#CC0000",
            hover_color="#AA0000",
            height=30,
        )
        self.clear_btn.grid(row=1, column=0, pady=10)

        # Drag functionality (since no title bar)
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.do_move)
        self.x = 0
        self.y = 0

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def update_bullets(self, bullets):
        # Update labels safely
        # Ensure we have enough labels or just update first 3
        for i, lbl in enumerate(self.bullet_labels):
            if i < len(bullets):
                # Clean up bullet text if it starts with "- " or "* "
                txt = bullets[i]
                if txt.startswith("- ") or txt.startswith("* "):
                    txt = txt[2:]
                lbl.configure(text=f"• {txt}")
            else:
                lbl.configure(text="")

    def on_clear(self):
        # Clear UI
        for lbl in self.bullet_labels:
            lbl.configure(text="")
        # Call backend clear
        if self.clear_callback:
            self.clear_callback()
