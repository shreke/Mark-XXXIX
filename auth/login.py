import tkinter as tk
from tkinter import messagebox
import urllib.request
import urllib.parse
import json
from pathlib import Path
import sys

TMS_API = "https://app.maman.com.ar/api"

def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent

def show_login() -> bool:
    """Muestra ventana de login. Retorna True si login exitoso, False si canceló."""

    result = {"success": False}

    root = tk.Tk()
    root.title("MAIA — Iniciar sesión")
    root.geometry("400x500")
    root.configure(bg="#0f172a")
    root.resizable(False, False)

    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - 200
    y = (root.winfo_screenheight() // 2) - 250
    root.geometry(f"400x500+{x}+{y}")

    # Logo / título
    tk.Label(root, text="M.A.I.A", font=("Courier", 28, "bold"),
             fg="#38bdf8", bg="#0f172a").pack(pady=(40, 4))
    tk.Label(root, text="Maman AI Assistant", font=("Courier", 11),
             fg="#64748b", bg="#0f172a").pack(pady=(0, 40))

    # Email
    tk.Label(root, text="EMAIL", font=("Courier", 10),
             fg="#94a3b8", bg="#0f172a", anchor="w").pack(fill="x", padx=50)
    email_var = tk.StringVar()
    email_entry = tk.Entry(root, textvariable=email_var, font=("Courier", 12),
                           bg="#1e293b", fg="#f1f5f9", insertbackground="#38bdf8",
                           relief="flat", bd=8)
    email_entry.pack(fill="x", padx=50, pady=(4, 20), ipady=8)

    # Password
    tk.Label(root, text="CONTRASEÑA", font=("Courier", 10),
             fg="#94a3b8", bg="#0f172a", anchor="w").pack(fill="x", padx=50)
    pass_var = tk.StringVar()
    pass_entry = tk.Entry(root, textvariable=pass_var, font=("Courier", 12),
                          bg="#1e293b", fg="#f1f5f9", insertbackground="#38bdf8",
                          relief="flat", bd=8, show="●")
    pass_entry.pack(fill="x", padx=50, pady=(4, 8), ipady=8)

    error_label = tk.Label(root, text="", font=("Courier", 10),
                           fg="#ef4444", bg="#0f172a")
    error_label.pack(pady=(0, 20))

    def do_login(event=None):
        email = email_var.get().strip()
        password = pass_var.get().strip()
        if not email or not password:
            error_label.config(text="Completá email y contraseña.")
            return

        btn.config(text="VERIFICANDO...", state="disabled")
        root.update()

        try:
            data = json.dumps({"email": email, "password": password}).encode()
            req = urllib.request.Request(
                f"{TMS_API}/auth/login",
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = json.loads(resp.read())

            # Extraer datos del usuario del token response
            token = body.get("access_token", "")
            usuario = body.get("usuario", {})
            nombre = usuario.get("nombre_corto") or usuario.get("nombres", "Usuario")
            rol = usuario.get("rol", "operaciones")
            email_resp = usuario.get("email", email)

            # Verificar que tenga acceso a MAIA
            if not usuario.get("acceso_maia", False) and rol not in ("admin",):
                error_label.config(text="Tu usuario no tiene acceso a MAIA.")
                btn.config(text="► INGRESAR", state="normal")
                return

            # Guardar session.json
            session_path = get_base_dir() / "config" / "session.json"
            session_path.parent.mkdir(exist_ok=True)
            session_data = {
                "nombre": nombre,
                "email": email_resp,
                "rol": rol,
                "token": token
            }
            session_path.write_text(json.dumps(session_data, ensure_ascii=False, indent=2), encoding="utf-8")

            result["success"] = True
            root.destroy()

        except urllib.error.HTTPError as e:
            if e.code == 401:
                error_label.config(text="Email o contraseña incorrectos.")
            else:
                error_label.config(text=f"Error del servidor: {e.code}")
            btn.config(text="► INGRESAR", state="normal")
        except Exception as e:
            error_label.config(text=f"Sin conexión al servidor.")
            btn.config(text="► INGRESAR", state="normal")

    btn = tk.Button(root, text="► INGRESAR", font=("Courier", 12, "bold"),
                    bg="#38bdf8", fg="#0f172a", relief="flat", bd=0,
                    cursor="hand2", command=do_login)
    btn.pack(fill="x", padx=50, ipady=12)

    # Enter para loguear
    root.bind("<Return>", do_login)
    email_entry.focus()

    # Si cierra la ventana sin loguear
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()

    return result["success"]
