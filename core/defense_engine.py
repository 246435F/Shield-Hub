import psutil, time, threading

class DefenseEngine:
    def __init__(self, alert_callback):
        self.alert_callback = alert_callback
        # खतरनाक टूल्स की लिस्ट
        self.suspicious = ['msfvenom', 'meterpreter', 'nc', 'hydra', 'msfconsole', 'ettercap', 'wireshark']
        # सुरक्षित प्रोसेस की लिस्ट
        self.safe_list = ['dbus', 'at-spi', 'kworker', 'systemd', 'xorg', 'bash', 'python3', 'gnome-shell']
        self.monitoring = True

    def start_monitoring(self):
        """बैकग्राउंड थ्रेड में मॉनिटरिंग शुरू करें"""
        monitor_thread = threading.Thread(target=self._run_monitor, daemon=True)
        monitor_thread.start()

    def _run_monitor(self):
        while self.monitoring:
            for proc in psutil.process_iter(['name', 'cmdline', 'cpu_percent']):
                try:
                    pname = proc.info['name'].lower()
                    cmdline = " ".join(proc.info['cmdline'] or []).lower()
                    
                    # 1. Nmap logic: Shield-Hub के अपने स्कैन्स को इग्नोर करें
                    if 'nmap' in pname:
                        if '-pn' in cmdline or '--min-rate' in cmdline:
                            continue

                    # 2. Safe list चेक करें
                    if any(safe in pname for safe in self.safe_list): 
                        continue
                    
                    # 3. Suspicious tools डिटेक्शन
                    if any(s in pname for s in self.suspicious):
                        self.alert_callback(f"⚠️ THREAT DETECTED: {pname.upper()}")
                        # अलर्ट के बाद थोड़ा रुकें ताकि एक ही चीज बार-बार अलर्ट न करे
                        time.sleep(2) 

                    # 4. CPU Spike Check (Optional: For hidden miners)
                    if proc.info['cpu_percent'] > 80.0:
                        self.alert_callback(f"🔥 HIGH CPU ALERT: {pname} ({proc.info['cpu_percent']}%)")

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            # CPU पर लोड कम करने के लिए 3 सेकंड का गैप
            time.sleep(3)

    def stop_monitoring(self):
        self.monitoring = False
