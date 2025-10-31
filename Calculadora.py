#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MI Laser | Calculadora de Medida — REV_01
- Rendimento de Tubo/Barra
- Rendimento de Chapa (por área)
- Pintura (m²): área e fatores para Bling (m²/peça e 1/área)
"""

import tkinter as tk
from tkinter import ttk, messagebox

APP_TITLE = "MI Laser | Calculadora de Medida — REV_01"
APP_WIDTH = 900
APP_HEIGHT = 680
LOGO_PATH = "logo_mi_laser.png"  # coloque o arquivo PNG do logo nessa mesma pasta

def fmt_float(x, nd=6):
    try:
        return f"{float(x):.{nd}f}"
    except Exception:
        return str(x)

def parse_float(entry):
    try:
        return float(entry.get().replace(",", "."))
    except Exception:
        return None

# ---------- Aba Tubo/Barra ----------
class TuboBarraFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=16)
        self._build()

    def _build(self):
        ttk.Label(self, text="Rendimento de Tubo/Barra", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=6, sticky="w", pady=(0,12))

        ttk.Label(self, text="Comprimento da barra (mm):").grid(row=1, column=0, sticky="e", padx=4, pady=4)
        ttk.Label(self, text="Comprimento da peça (mm):").grid(row=2, column=0, sticky="e", padx=4, pady=4)
        ttk.Label(self, text="Perda de corte/serra (mm) [opcional]:").grid(row=3, column=0, sticky="e", padx=4, pady=4)

        self.e_barra = ttk.Entry(self)
        self.e_peca = ttk.Entry(self)
        self.e_perda = ttk.Entry(self)

        self.e_barra.grid(row=1, column=1, sticky="we", padx=4, pady=4)
        self.e_peca.grid(row=2, column=1, sticky="we", padx=4, pady=4)
        self.e_perda.grid(row=3, column=1, sticky="we", padx=4, pady=4)

        self.grid_columnconfigure(1, weight=1)

        ttk.Button(self, text="Calcular", command=self.calcular).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Separator(self, orient="horizontal").grid(row=5, column=0, columnspan=6, sticky="we", pady=10)

        self.out_text = tk.Text(self, height=9, wrap="word")
        self.out_text.grid(row=6, column=0, columnspan=6, sticky="nsew")
        self.grid_rowconfigure(6, weight=1)

        ttk.Button(self, text="Copiar resultado", command=self.copiar).grid(row=7, column=0, columnspan=2, pady=(10,0))

        ttk.Label(self, text="Fator para Bling: unidade de barra por peça (1 / peças por barra).", foreground="#555").grid(row=8, column=0, columnspan=6, sticky="w", pady=(8,0))

    def calcular(self):
        L_barra = parse_float(self.e_barra)
        L_peca  = parse_float(self.e_peca)
        perda   = parse_float(self.e_perda) or 0.0

        if (L_barra is None) or (L_peca is None) or L_barra<=0 or L_peca<=0:
            messagebox.showerror("Erro", "Informe comprimentos válidos (mm).")
            return

        n = int((L_barra + perda) / (L_peca + perda)) if (L_peca + perda) > 0 else 0
        usado = n*L_peca + max(0, n-1)*perda
        sobra = max(0.0, L_barra - usado)
        fator = (1.0/n) if n>0 else 0.0

        linhas = [
            f"Entrada: barra = {fmt_float(L_barra,0)} mm | peça = {fmt_float(L_peca,0)} mm | perda = {fmt_float(perda,0)} mm",
            f"Resultado: 1 barra rende {n} peça(s) | sobra = {fmt_float(sobra,0)} mm",
            f"Fator para Bling (barra/peça): 1/{n} = {fmt_float(fator,6)}" if n>0 else "Fator para Bling: não aplicável (0).",
            "Obs.: considera perda uniforme entre cortes (serra/kerf)."
        ]
        self.out_text.delete("1.0","end")
        self.out_text.insert("1.0","\n".join(linhas))

    def copiar(self):
        texto = self.out_text.get("1.0","end").strip()
        if not texto: return
        self.clipboard_clear(); self.clipboard_append(texto)
        messagebox.showinfo("Copiado","Resultado copiado.")

# ---------- Aba Chapa (Área) ----------
class ChapaAreaFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=16)
        self._build()

    def _build(self):
        ttk.Label(self, text="Rendimento de Chapa (por área)", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=8, sticky="w", pady=(0,12))

        # Entradas
        labels = [
            ("Chapa - Largura (mm):", 1, 0), ("Chapa - Comprimento (mm):", 1, 2),
            ("Peça - Largura (mm):", 2, 0),  ("Peça - Comprimento (mm):", 2, 2)
        ]
        self.e_cw, self.e_ch, self.e_pw, self.e_ph = ttk.Entry(self), ttk.Entry(self), ttk.Entry(self), ttk.Entry(self)
        entries = [self.e_cw, self.e_ch, self.e_pw, self.e_ph]
        for (txt, r, c), ent in zip(labels, entries):
            ttk.Label(self, text=txt).grid(row=r, column=c, sticky="e", padx=4, pady=4)
            ent.grid(row=r, column=c+1, sticky="we", padx=4, pady=4)

        ttk.Label(self, text="Perda estimada de aninhamento (%) [opcional]:").grid(row=3, column=0, columnspan=2, sticky="e", padx=4, pady=4)
        self.e_loss = ttk.Entry(self); self.e_loss.grid(row=3, column=2, sticky="we", padx=4, pady=4)
        ttk.Label(self, text="(Ex.: 10 para 10%)").grid(row=3, column=3, sticky="w")

        for c in (1,3): self.grid_columnconfigure(c, weight=1)

        ttk.Button(self, text="Calcular", command=self.calcular).grid(row=4, column=0, columnspan=8, pady=10)
        ttk.Separator(self, orient="horizontal").grid(row=5, column=0, columnspan=8, sticky="we", pady=10)

        self.out_text = tk.Text(self, height=10, wrap="word")
        self.out_text.grid(row=6, column=0, columnspan=8, sticky="nsew")
        self.grid_rowconfigure(6, weight=1)
        ttk.Button(self, text="Copiar resultado", command=self.copiar).grid(row=7, column=0, columnspan=2, pady=(10,0))

    def calcular(self):
        def p(e):
            try: return float(e.get().replace(",","."))
            except: return None

        cw, ch, pw, ph = p(self.e_cw), p(self.e_ch), p(self.e_pw), p(self.e_ph)
        loss = p(self.e_loss) or 0.0

        if None in (cw, ch, pw, ph) or min(cw, ch, pw, ph) <= 0:
            messagebox.showerror("Erro", "Informe dimensões válidas (mm).")
            return

        area_chapa = cw*ch
        area_peca  = pw*ph
        eficiencia = max(0.0, 1.0 - loss/100.0)
        rendimento = int((area_chapa/area_peca) * eficiencia)
        fator = (1.0/rendimento) if rendimento>0 else 0.0

        texto = [
            f"Chapa: {fmt_float(cw,0)} x {fmt_float(ch,0)} mm  |  Peça: {fmt_float(pw,0)} x {fmt_float(ph,0)} mm",
            f"Perda estimada: {fmt_float(loss,2)}%  → Eficiência: {fmt_float(eficiencia*100,2)}%",
            f"Resultado: 1 chapa rende {rendimento} peça(s)",
            f"Fator para Bling (chapa/peça): 1/{rendimento} = {fmt_float(fator,6)}" if rendimento>0 else "Fator para Bling: não aplicável (0)."
        ]
        self.out_text.delete("1.0","end")
        self.out_text.insert("1.0","\n".join(texto))

    def copiar(self):
        texto = self.out_text.get("1.0","end").strip()
        if not texto: return
        self.clipboard_clear(); self.clipboard_append(texto)
        messagebox.showinfo("Copiado","Resultado copiado.")

# ---------- Aba Pintura (m²) ----------
class PinturaFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=16)
        self._build()

    def _build(self):
        ttk.Label(self, text="Pintura (m²) – área e fatores para Bling", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=10, sticky="w", pady=(0,12))

        ttk.Label(self, text="Largura (mm):").grid(row=1, column=0, sticky="e", padx=4, pady=4)
        ttk.Label(self, text="Comprimento (mm):").grid(row=1, column=2, sticky="e", padx=4, pady=4)
        ttk.Label(self, text="Altura (mm):").grid(row=1, column=4, sticky="e", padx=4, pady=4)

        self.e_w, self.e_l, self.e_h = ttk.Entry(self), ttk.Entry(self), ttk.Entry(self)
        self.e_w.grid(row=1, column=1, sticky="we", padx=4, pady=4)
        self.e_l.grid(row=1, column=3, sticky="we", padx=4, pady=4)
        self.e_h.grid(row=1, column=5, sticky="we", padx=4, pady=4)

        ttk.Label(self, text="Faces a pintar:").grid(row=2, column=0, sticky="e", padx=4, pady=4)
        self.faces = ttk.Combobox(self, values=["Todas as faces", "2 faces opostas", "1 face"], state="readonly")
        self.faces.current(0)
        self.faces.grid(row=2, column=1, sticky="we", padx=4, pady=4)

        ttk.Button(self, text="Calcular", command=self.calcular).grid(row=3, column=0, columnspan=10, pady=10)
        ttk.Separator(self, orient="horizontal").grid(row=4, column=0, columnspan=10, sticky="we", pady=10)

        self.out_text = tk.Text(self, height=14, wrap="word")
        self.out_text.grid(row=5, column=0, columnspan=10, sticky="nsew")
        self.grid_rowconfigure(5, weight=1)
        for c in (1,3,5): self.grid_columnconfigure(c, weight=1)

        ttk.Button(self, text="Copiar resultado", command=self.copiar).grid(row=6, column=0, columnspan=2, pady=(10,0))

        ttk.Label(self, text=("No Bling, cadastre a pintura como item de m².\n"
                              "→ Use o FATOR DIRETO: m² por peça (valor da área)."), foreground="#555").grid(row=7, column=0, columnspan=10, sticky="w", pady=(8,0))

    def calcular(self):
        def to_f(e):
            try: return float(e.get().replace(",", "."))
            except: return None

        w, l, h = to_f(self.e_w), to_f(self.e_l), to_f(self.e_h)
        if None in (w,l,h) or min(w,l,h) <= 0:
            messagebox.showerror("Erro", "Informe dimensões válidas em mm.")
            return

        area_total_mm2 = 2*(w*l + w*h + l*h)  # área total do paralelepípedo
        modo = self.faces.get()
        if modo == "Todas as faces":
            area_mm2 = area_total_mm2
        elif modo == "2 faces opostas":
            area_mm2 = area_total_mm2 / 3.0  # aproximação
        else:
            area_mm2 = area_total_mm2 / 6.0  # aproximação

        area_m2 = area_mm2 * 1e-6  # mm² -> m²
        fator_direto  = area_m2
        fator_inverso = (1.0/area_m2) if area_m2 > 0 else 0.0

        texto = [
            f"Dimensões: {fmt_float(w,0)} x {fmt_float(l,0)} x {fmt_float(h,0)} mm  |  Faces: {modo}",
            f"Área de pintura (m²/peça): {fmt_float(area_m2,6)} m²",
            "——— Para uso na Estrutura do Bling ———",
            f"Fator DIRETO (m²/peça): {fmt_float(fator_direto,6)}  ← usar no Bling",
            f"Fator INVERSO (1/área): 1/{fmt_float(area_m2,6)} = {fmt_float(fator_inverso,6)}  (opcional)"
        ]
        self.out_text.delete("1.0","end")
        self.out_text.insert("1.0","\n".join(texto))

    def copiar(self):
        texto = self.out_text.get("1.0","end").strip()
        if not texto: return
        self.clipboard_clear(); self.clipboard_append(texto)
        messagebox.showinfo("Copiado","Resultado copiado.")

# ---------- Aplicativo ----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.minsize(760, 560)

        style = ttk.Style(self)
        try: self.call("tk", "scaling", 1.15)
        except Exception: pass
        if "vista" in style.theme_names(): style.theme_use("vista")
        elif "clam" in style.theme_names(): style.theme_use("clam")

        banner = ttk.Frame(self, padding=(10,10))
        banner.pack(fill="x")
        try:
            self._logo = tk.PhotoImage(file=LOGO_PATH)
            ttk.Label(banner, image=self._logo).pack(side="left")
        except Exception:
            ttk.Label(banner, text="MI LASER", font=("Segoe UI", 16, "bold")).pack(side="left")
        ttk.Label(banner, text="Calculadora de Medida — REV_01", font=("Segoe UI", 16, "bold")).pack(side="left", padx=12)

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=8, pady=(0,8))
        nb.add(TuboBarraFrame(nb), text="🔩 Tubo/Barra")
        nb.add(ChapaAreaFrame(nb), text="🧱 Chapa (Área)")
        nb.add(PinturaFrame(nb), text="🎨 Pintura (m²)")

if __name__ == "__main__":
    app = App()
    app.mainloop()
