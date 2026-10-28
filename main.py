"""Desktop entry point for the Pixel Studio photo editor."""
# from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import cv2
import numpy as np
from PIL import Image, ImageTk

from image_editor.filters import apply_edit


class PixelStudio:
    """A compact Tkinter interface for applying OpenCV edits to images."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Pixel Studio | Photo Editor")
        self.root.geometry("1100x720")
        self.root.minsize(780, 560)
        self.root.configure(bg="#1a1e2a")
        self.original: np.ndarray | None = None
        self.current_file: Path | None = None
        self.preview_image: ImageTk.PhotoImage | None = None
        self.current_filter = tk.StringVar(value="original")
        self.brightness = tk.IntVar(value=0)
        self.contrast = tk.IntVar(value=0)
        self._configure_styles()
        self._build_interface()

    def _configure_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#171b25")
        style.configure("TLabel", background="#171b25", foreground="#00ff00", font=("Segoe UI", 10))
        style.configure("Heading.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Muted.TLabel", foreground="#929bad", font=("Segoe UI", 9))
        style.configure("TButton", font=("Segoe UI", 10), padding=(11, 8))
        style.configure("Accent.TButton", background="#a9f27c", foreground="#182114", font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton", background=[("active", "#baf995"), ("disabled", "#59634f")])
        style.configure("TRadiobutton", background="#171b25", foreground="#d8dce5", font=("Segoe UI", 10))
        style.map("TRadiobutton", background=[("active", "#171b25")], foreground=[("active", "#a9f27c")])
        style.configure("Horizontal.TScale", background="#171b25", troughcolor="#343b4b")

    def _build_interface(self) -> None:
        header = ttk.Frame(self.root, padding=(22, 16))
        header.pack(fill="x")
        ttk.Label(header, text="✳  Pixel Studio", style="Heading.TLabel").pack(side="left")
        ttk.Label(header, text="A simple photo editor powered by OpenCV", style="Muted.TLabel").pack(side="left", padx=(16, 0), pady=(5, 0))
        ttk.Button(header, text="Export image", style="Accent.TButton", command=self.save_image).pack(side="right")

        body = ttk.Frame(self.root)
        body.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        sidebar = ttk.Frame(body, width=255, padding=18)
        sidebar.pack(side="left", fill="y", padx=(0, 14))
        sidebar.pack_propagate(False)
        ttk.Label(sidebar, text="PHOTO EDITOR", style="Muted.TLabel").pack(anchor="w")
        ttk.Label(sidebar, text="Make it yours", style="Heading.TLabel").pack(anchor="w", pady=(4, 18))
        ttk.Button(sidebar, text="＋  Open image", style="Accent.TButton", command=self.open_image).pack(fill="x")
        ttk.Label(sidebar, text="PNG, JPG, JPEG, or WEBP", style="Muted.TLabel").pack(anchor="w", pady=(7, 16))
        ttk.Separator(sidebar).pack(fill="x", pady=5)
        ttk.Label(sidebar, text="FILTERS", style="Muted.TLabel").pack(anchor="w", pady=(14, 9))
        for label, value in [("Original", "original"), ("Monochrome", "grayscale"), ("Sepia", "sepia"), ("Soft blur", "blur"), ("Sharpen", "sharpen")]:
            ttk.Radiobutton(sidebar, text=label, value=value, variable=self.current_filter, command=self.render_preview).pack(anchor="w", pady=4)
        ttk.Separator(sidebar).pack(fill="x", pady=(15, 5))
        ttk.Label(sidebar, text="ADJUSTMENTS", style="Muted.TLabel").pack(anchor="w", pady=(12, 7))
        self._add_slider(sidebar, "Brightness", self.brightness)
        self._add_slider(sidebar, "Contrast", self.contrast)
        ttk.Button(sidebar, text="↺  Reset edits", command=self.reset_edits).pack(fill="x", pady=(14, 0))

        canvas_panel = ttk.Frame(body, padding=12)
        canvas_panel.pack(side="left", fill="both", expand=True)
        self.filename_label = ttk.Label(canvas_panel, text="Untitled project", style="Muted.TLabel")
        self.filename_label.pack(anchor="w", pady=(1, 10))
        self.canvas = tk.Label(canvas_panel, text="Open an image to get started", bg="#131720", fg="#929bad", font=("Segoe UI", 13))
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _event: self.render_preview())
        self.status = ttk.Label(canvas_panel, text="Images stay on your device", style="Muted.TLabel")
        self.status.pack(anchor="w", pady=(10, 0))

    def _add_slider(self, parent: ttk.Frame, label: str, variable: tk.IntVar) -> None:
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=(8, 0))
        ttk.Label(row, text=label).pack(side="left")
        value_label = ttk.Label(row, text="0", style="Muted.TLabel")
        value_label.pack(side="right")
        ttk.Scale(parent, from_=-100, to=100, variable=variable, command=lambda value: self._slider_changed(value_label, value)).pack(fill="x", pady=(4, 0))

    def _slider_changed(self, label: ttk.Label, value: str) -> None:
        label.configure(text=str(round(float(value))))
        self.render_preview()

    def open_image(self) -> None:
        selected = filedialog.askopenfilename(title="Choose an image", filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp *.bmp"), ("All files", "*.*")])
        if not selected:
            return
        try:
            image = cv2.imdecode(np.fromfile(selected, dtype=np.uint8), cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError("OpenCV could not read this image format.")
        except (OSError, ValueError) as error:
            messagebox.showerror("Could not open image", str(error))
            return
        self.original = image
        self.current_file = Path(selected)
        self.current_filter.set("original")
        self.brightness.set(0)
        self.contrast.set(0)
        self.filename_label.configure(text=self.current_file.name)
        height, width = image.shape[:2]
        self.status.configure(text=f"{width} × {height} px  ·  Ready to edit")
        self.render_preview()

    def render_preview(self) -> None:
        if self.original is None or not self.canvas.winfo_exists():
            return
        edited = apply_edit(self.original, {"filter": self.current_filter.get(), "brightness": self.brightness.get(), "contrast": self.contrast.get()})
        image = Image.fromarray(cv2.cvtColor(edited, cv2.COLOR_BGR2RGB))
        image.thumbnail((max(self.canvas.winfo_width() - 30, 100), max(self.canvas.winfo_height() - 30, 100)), Image.Resampling.LANCZOS)
        self.preview_image = ImageTk.PhotoImage(image)
        self.canvas.configure(image=self.preview_image, text="")

    def reset_edits(self) -> None:
        self.current_filter.set("original")
        self.brightness.set(0)
        self.contrast.set(0)
        self.render_preview()

    def save_image(self) -> None:
        if self.original is None:
            messagebox.showinfo("No image", "Open an image before exporting.")
            return
        edited = apply_edit(self.original, {"filter": self.current_filter.get(), "brightness": self.brightness.get(), "contrast": self.contrast.get()})
        stem = self.current_file.stem if self.current_file else "image"
        destination = filedialog.asksaveasfilename(title="Export edited image", initialfile=f"{stem}-edited.png", defaultextension=".png", filetypes=[("PNG image", "*.png"), ("JPEG image", "*.jpg"), ("WEBP image", "*.webp")])
        if not destination:
            return
        extension = Path(destination).suffix.lower()
        extension = ".jpeg" if extension == ".jpg" else extension or ".png"
        success, encoded = cv2.imencode(extension, edited)
        if not success:
            messagebox.showerror("Export failed", "OpenCV could not create that image format.")
            return
        try:
            encoded.tofile(destination)
        except OSError as error:
            messagebox.showerror("Export failed", str(error))
            return
        self.status.configure(text=f"Exported · {Path(destination).name}")


def main() -> None:
    root = tk.Tk()
    PixelStudio(root)
    root.mainloop()


if __name__ == "__main__":
    main()
