import customtkinter as ctk
import threading, os, psutil, socket, time, requests, shutil, pyttsx3
from tkinter import filedialog, messagebox
from datetime import datetime
from PIL import Image, ImageTk

try:
    from core.recon_engine import ReconEngine
    from core.exploit_engine import ExploitEngine
    from core.defense_engine import DefenseEngine
    from core.intel_engine import IntelEngine
except ImportError as e:
    print(f"❌ Error: Core engines missing! {e}")

ctk.set_appearance_mode("Dark")

class ShieldHubApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🛡️ SHIELD-HUB v41.0 - JARVIS EDITION")
        self.geometry("1450x950")
        self.configure(fg_color="#050505")

        # --- JARVIS VOICE ENGINE ---
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150) # बोलने की रफ़्तार

        # Icon Setup
        try:
            if os.path.exists("icon.png"):
                img = Image.open("icon.png")
                self.tk_icon = ImageTk.PhotoImage(img)
                self.wm_iconphoto(False, self.tk_icon)
        except: pass

        # Init Folders
        for f in ["logs", "reports", "rules", "payloads_output"]:
            os.makedirs(f, exist_ok=True)
        
        self.local_ip = self.get_local_ip()
        self.public_ip = "Fetching..."
        self.last_net_io = psutil.net_io_counters()
        
        self.recon = ReconEngine()
        self.exploit = ExploitEngine()
        self.defense = DefenseEngine(self.alert_threat)
        self.intel = IntelEngine()

        # Background threads
        threading.Thread(target=self.defense.start_monitoring, daemon=True).start()
        threading.Thread(target=self.fetch_public_ip, daemon=True).start()

        self.setup_ui()
        self.update_sys_stats()
        self.update_clock()
        
        # Welcome Voice
        self.speak("Shield Hub initialized. System secure. Welcome back, Agent.")

    def speak(self, text):
        """Jarvis Voice Function"""
        def run_voice():
            self.engine.say(text)
            self.engine.runAndWait()
        threading.Thread(target=run_voice, daemon=True).start()

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80)); ip = s.getsockname(); s.close()
            return ip
        except: return "127.0.0.1"

    def fetch_public_ip(self):
        try:
            res = requests.get("https://api.ipify.org", timeout=10)
            self.public_ip = res.text
            self.after(0, lambda: self.ip_label.configure(text=f"L-IP: {self.local_ip} | P-IP: {self.public_ip}"))
        except: self.public_ip = "OFFLINE"

    def alert_threat(self, msg):
        self.after(0, lambda: self.threat_label.configure(text=msg, text_color="#FF0000"))
        self.speak("Security Alert! Suspicious activity detected.")
        self.update_console_live(f"\n[⚠️ ALERT] {msg}\n")

    def setup_ui(self):
        # --- Top Bar with Jarvis Stats ---
        self.top_bar = ctk.CTkFrame(self, height=60, fg_color="#0a0a0a")
        self.top_bar.pack(side="top", fill="x")
        
        self.sys_info = ctk.CTkLabel(self.top_bar, text="CPU: 0% | RAM: 0%", font=("Consolas", 11), text_color="#00FF00")
        self.sys_info.pack(side="left", padx=15)

        self.net_speed_label = ctk.CTkLabel(self.top_bar, text="DN: 0 KB/s | UP: 0 KB/s", font=("Consolas", 11), text_color="#FFA500")
        self.net_speed_label.pack(side="left", padx=15)
        
        self.ip_label = ctk.CTkLabel(self.top_bar, text=f"L-IP: {self.local_ip} | P-IP: Fetching...", font=("Consolas", 11, "bold"), text_color="#00FFFF")
        self.ip_label.pack(side="left", padx=25)
        
        self.threat_label = ctk.CTkLabel(self.top_bar, text="🛡️ SYSTEM SECURE", font=("Consolas", 12, "bold"), text_color="#00FF00")
        self.threat_label.pack(side="left", padx=40)
        
        self.clock_label = ctk.CTkLabel(self.top_bar, text="", font=("Consolas", 12, "bold"), text_color="#00FF00")
        self.clock_label.pack(side="right", padx=20)

        # --- Sidebar ---
        self.sidebar = ctk.CTkScrollableFrame(self, width=280, fg_color="#080808", border_width=1, border_color="#1a1a1a")
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)
        ctk.CTkLabel(self.sidebar, text="🛡️", font=("Impact", 60), text_color="#00FF00").pack(pady=(20,0))
        ctk.CTkLabel(self.sidebar, text="SHIELD-HUB", font=("Impact", 35), text_color="#00FF00").pack(pady=(0,20))

        # Buttons (Phase 1-4)
        self.create_lbl("[ PHASE 1: RECON ]", "#555")
        self.add_btn("📡 Discovery Scan", lambda: self.start_scan("fast"), "#00FF00")
        self.add_btn("🗺️ Network Map", self.run_mapping, "#00FFFF")
        self.add_btn("📡 Wi-Fi Scanner", self.run_wifi_scan, "#FF00FF")
        self.create_lbl("[ PHASE 2: EXPLOIT ]", "#555")
        self.add_btn("⚡ MSF-Auto-Engine", self.run_attack_automated, "#FF3300")
        self.add_btn("🔍 Vuln Audit", self.run_vuln_audit, "#FF8C00")
        self.create_lbl("[ PHASE 3: DEFENSE ]", "#555")
        self.add_btn("☣️ YARA Malware Scan", self.run_yara_scan, "#E74C3C")
        self.create_lbl("[ PHASE 4: INTEL ]", "#555")
        self.add_btn("🤖 AI Analysis", self.run_ai_analysis, "#BB86FC")
        self.add_btn("📊 Export PDF Report", self.export_pdf, "#228B22")
        
        ctk.CTkButton(self.sidebar, text="🔥 EXIT & CLEANUP", fg_color="#440000", hover_color="#880000", command=self.self_destruct_exit).pack(side="bottom", pady=30, padx=20, fill="x")

        # --- Console Area ---
        self.main_work = ctk.CTkFrame(self, fg_color="transparent")
        self.main_work.pack(side="right", expand=True, fill="both", padx=10, pady=10)
        self.entry = ctk.CTkEntry(self.main_work, placeholder_text="Target IP / LHOST", height=45, font=("Consolas", 14), text_color="#00FF00")
        self.entry.pack(fill="x", pady=5)
        self.progress = ctk.CTkProgressBar(self.main_work, width=400, progress_color="#00FF00")
        self.progress.set(0); self.progress.pack(pady=5)
        self.console = ctk.CTkTextbox(self.main_work, font=("Consolas", 14), fg_color="#000", text_color="#00FF00")
        self.console.pack(fill="both", expand=True)

        self.console.tag_config("info", foreground="#00FFFF")
        self.console.tag_config("success", foreground="#00FF00")
        self.console.tag_config("alert", foreground="#FF0000")
        self.console.tag_config("intel", foreground="#BB86FC")

    def create_lbl(self, txt, col): ctk.CTkLabel(self.sidebar, text=txt, font=("Consolas", 11, "bold"), text_color=col).pack(pady=(15,2))
    def add_btn(self, txt, cmd, col): ctk.CTkButton(self.sidebar, text=txt, command=cmd, fg_color="transparent", border_width=1, border_color=col, text_color=col, anchor="w").pack(pady=3, padx=15, fill="x")

    def update_console_live(self, t):
        tag = "info" if "[*]" in t else "success" if "✅" in t or "safe" in t else "alert" if "MALWARE" in t or "⚠️" in t else "intel" if "[🤖 AI]" in t else None
        self.console.insert("end", t, tag); self.console.see("end")
        try:
            with open("logs/shield_activity.log", "a", encoding="utf-8") as log_file:
                ts = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
                if t.strip(): log_file.write(f"{ts} {t.strip()}\n")
        except: pass

    def clear_console(self, m): self.console.delete("1.0", "end"); self.update_console_live(f"[*] {m}\n" + "="*60 + "\n")

    # --- Scanning with Voice Notifications ---
    def start_scan(self, mode):
        t = self.entry.get().strip()
        if t:
            self.speak(f"Starting discovery scan on {t}")
            self.clear_console(f"DISCOVERY SCAN: {t}")
            self.progress.configure(mode="indeterminate"); self.progress.start()
            threading.Thread(target=lambda: self.run_scan_thread(t, mode), daemon=True).start()

    def run_scan_thread(self, t, mode):
        res = self.recon.advanced_scan(t, None, mode)
        self.after(0, self.stop_progress)
        self.after(0, lambda: self.update_console_live(res["details"]))
        self.speak("Scan completed. Analysis inbound.")
        self.after(800, self.run_ai_analysis)

    def stop_progress(self): self.progress.stop(); self.progress.configure(mode="determinate"); self.progress.set(1.0)

    def run_mapping(self):
        t = self.entry.get().strip() or f"{self.local_ip.rsplit('.', 1)}.0/24"
        self.speak("Mapping local network architecture.")
        self.clear_console(f"MAPPING NETWORK: {t}")
        def map_cb(res): self.update_console_live(res); self.speak("Map completed."); self.after(800, self.run_ai_analysis)
        threading.Thread(target=lambda: self.recon.generate_map(t, map_cb), daemon=True).start()

    def run_yara_scan(self):
        f = filedialog.askopenfilename()
        if f: 
            self.speak("Analyzing file for malicious signatures.")
            self.clear_console(f"MALWARE SCAN: {os.path.basename(f)}")
            res = self.recon.yara_scan_file(f)
            self.update_console_live(res["message"] + "\n")
            if "MALWARE DETECTED!" in res["message"]:
                self.speak("Warning! Malicious payload identified on the system.")

    # --- System Monitoring (Traffic Speed) ---
    def update_sys_stats(self):
        curr_net = psutil.net_io_counters()
        dn = (curr_net.bytes_recv - self.last_net_io.bytes_recv) / 1024
        up = (curr_net.bytes_sent - self.last_net_io.bytes_sent) / 1024
        self.last_net_io = curr_net
        self.sys_info.configure(text=f"CPU: {psutil.cpu_percent()}% | RAM: {psutil.virtual_memory().percent}%")
        self.net_speed_label.configure(text=f"DN: {dn:.1f} KB/s | UP: {up:.1f} KB/s")
        self.after(1000, self.update_sys_stats)

    def update_clock(self):
        self.clock_label.configure(text=datetime.now().strftime("%H:%M:%S"))
        self.after(1000, self.update_clock)

    def self_destruct_exit(self):
        """सभी डेटा मिटाएं और सुरक्षित रूप से बाहर निकलें"""
        self.speak("Initiating self-destruct protocol. Cleaning all tracks.")
        self.update_console_live("\n[🔥 SELF-DESTRUCT] Wiping logs, payloads, and session data...\n")
        
        # उन फोल्डर्स की लिस्ट जिन्हें साफ़ करना है
        folders_to_clean = ["logs", "payloads_output", "rules"]
        
        try:
            for folder in folders_to_clean:
                if os.path.exists(folder):
                    # फोल्डर के अंदर की सभी फाइलें डिलीट करें
                    for filename in os.listdir(folder):
                        file_path = os.path.join(folder, filename)
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    self.update_console_live(f"[*] Cleared: /{folder}\n")
            
            self.update_console_live("✅ SYSTEM CLEAN. SHUTTING DOWN.\n")
            self.after(2000, self.destroy) # 2 सेकंड बाद ऐप बंद करें
            
        except Exception as e:
            messagebox.showerror("Error", f"Cleanup failed: {e}")
            self.destroy()


    def run_wifi_scan(self): self.speak("Scanning for nearby wireless networks."); self.clear_console("SCANNING WIFI"); threading.Thread(target=lambda: self.recon.scan_wifi(self.update_console_live), daemon=True).start()
    def run_attack_automated(self): self.speak("Exploit engine engaged."); threading.Thread(target=lambda: self.exploit.run_automated_attack(self.entry.get(), "4444", "win", "local", self.update_console_live), daemon=True).start()
    def run_ai_analysis(self): self.intel.analyze_scan_data(self.console.get("1.0", "end"), self.update_console_live)
    def export_pdf(self): self.speak("Generating intelligence report."); self.intel.export_pdf(self.console.get("1.0", "end"), self.update_console_live)
    def run_vuln_audit(self): 
        t = self.entry.get().strip()
        if t:
            self.speak(f"Auditing {t} for vulnerabilities."); self.clear_console(f"VULN AUDIT: {t}")
            self.progress.configure(mode="indeterminate"); self.progress.start()
            def vuln_cb(res): self.after(0, self.stop_progress); self.update_console_live(res); self.after(800, self.run_ai_analysis)
            threading.Thread(target=lambda: self.recon.check_vulnerabilities(t, vuln_cb), daemon=True).start()

if __name__ == "__main__":
    app = ShieldHubApp(); app.mainloop()
