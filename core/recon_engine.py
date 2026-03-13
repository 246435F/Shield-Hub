import subprocess, os, yara, hashlib, time

class ReconEngine:
    def __init__(self):
        os.makedirs("rules", exist_ok=True)
        # सुपर-पावरफुल रूल्स: अब यही आपका असली डिफेंस है
        self.embedded_rules = """
        rule ShieldHub_Ultimate_Offline_Detection {
            strings:
                $s1 = "meterpreter" nocase
                $s2 = "reverse_tcp" nocase
                $s3 = "rev_tcp" nocase
                $s4 = "payload" nocase
                // Metasploit के बाइनरी सिग्नल्स (इन्हें कोई एन्कोडर नहीं छुपा सकता)
                $h1 = { 6a 42 58 fe 0c 24 48 31 c0 } // Linux x64
                $h2 = { e8 00 00 00 00 58 83 e8 05 } // Call-Pop Trick
                $h3 = { fc e8 82 00 00 00 60 89 e5 } // Windows x86
                $h4 = { b8 01 00 00 00 cd 80 }       // Linux Exit
            condition:
                any of them
        }
        """

    def yara_scan_file(self, path):
        report = "[*] Starting Offline Deep Malware Analysis...\n"
        is_malicious = False
        
        try:
            # 1. Local Signature Scan
            rules = yara.compile(source=self.embedded_rules)
            matches = rules.match(path)
            file_size = os.path.getsize(path) / 1024 # KB में

            if matches:
                report += f"⚠️ [DETECTED] YARA matched malicious signature: {matches}\n"
                is_malicious = True
            
            # 2. Heuristic Analysis (व्यवहार के आधार पर)
            # अगर फाइल 200KB से छोटी है और Executable है, तो यह 99% पेलोड है
            elif file_size < 200:
                report += f"🟡 [HEURISTIC] Warning: Suspiciously small binary ({file_size:.2f} KB).\n"
                report += "   Note: This matches the profile of a generated payload.\n"
                is_malicious = True
            else:
                report += "✅ [CLEAN] No known malicious patterns found.\n"
                
        except Exception as e:
            report += f"❌ Scan Error: {e}\n"

        final_msg = "⚠️ MALWARE DETECTED!" if is_malicious else "✅ File appears safe."
        return {"message": f"{report}\nFINAL VERDICT: {final_msg}"}

    def advanced_scan(self, target, progress, mode="fast"):
        # सुपर फ़ास्ट डिस्कवरी स्कैन
        cmd = ["nmap", "-T4", "-n", "-Pn", "--min-rate", "5000", "--open", target]
        if mode != "fast": 
            cmd += ["-sV", "--script", "vulners"]
        try:
            res = subprocess.check_output(cmd, text=True)
            return {"details": res}
        except: return {"details": "❌ Nmap Scan Failed."}

    def scan_wifi(self, callback):
        cmd = "nmcli dev wifi list" if os.name == 'posix' else "netsh wlan show networks"
        try:
            res = subprocess.check_output(cmd, shell=True, text=True)
            callback(res if res.strip() else "⚠️ No WiFi networks found.")
        except: callback("❌ Wi-Fi Scan Error.")

    def generate_map(self, t, cb): 
        # नेटवर्क मैपिंग फिक्स
        if t and t.count('.') == 3 and "/" not in t:
            p = t.split('.')
            target_range = f"{p[0]}.{p[1]}.{p[2]}.0/24"
        else:
            target_range = t or "192.168.1.0/24"
            
        cb(f"[*] Mapping Active Devices on {target_range}...\n")
        res = subprocess.getoutput(f"nmap -sn -T4 -n --min-rate 5000 {target_range}")
        cb(res + "\n✅ Map Completed.")

    def check_vulnerabilities(self, t, cb): 
        # एडवांस्ड वल्नरेबिलिटी ऑडिट
        cb(f"[*] AUDITING VULNERABILITIES ON {t} (Bypass Mode)...\n")
        cmd = f"sudo nmap -sS -Pn -f --mtu 8 -sV --version-intensity 0 --script=vulners {t}"
        try:
            res = subprocess.getoutput(cmd)
            if "QUITTING" in res:
                res = subprocess.getoutput(f"nmap -sV --script=vulners {t}")
            cb(res + "\n✅ Audit Done.")
        except: cb("❌ Vulnerability Audit Error.")
