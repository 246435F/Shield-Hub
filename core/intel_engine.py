import os, time, re
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class IntelEngine:
    def analyze_scan_data(self, data, cb):
        cb("\n[🤖 AI] Cross-referencing scan logs with malware signatures...\n")
        time.sleep(1.5) 
        
        recommendations = []
        data_lower = data.lower()
        
        # --- NEW FEATURE: Malware Detection Awareness ---
        # अगर पिछले मालवेयर स्कैन का रिजल्ट कंसोल में मौजूद है
        if "malware detected!" in data_lower or "heuristic" in data_lower:
            recommendations.append("🚨 [CRITICAL] ACTIVE MALWARE FOUND! A suspicious file (Payload/Backdoor) was identified during analysis. \n   IMMEDIATE ACTION: Isolate the system and delete the infected file.")

        # 1. Firewall & Port Analysis (Saved Features)
        if "filtered" in data_lower:
            recommendations.append("🛡️ [FIREWALL] Detection active. Some reconnaissance attempts were blocked.")
        
        if "445/tcp" in data_lower and "open" in data_lower:
            recommendations.append("🔴 [SMB] Port 445 is OPEN. High risk of Ransomware (WannaCry). \n   Fix: Disable SMBv1 and apply MS17-010 patches.")
        
        if "21/tcp" in data_lower or "23/tcp" in data_lower:
            recommendations.append("🚨 [INSECURE SERVICE] FTP/Telnet detected. FIX: Use SFTP/SSH for encrypted communication.")

        # 2. Web Vulnerability Awareness
        if "80/tcp" in data_lower and "open" in data_lower:
            recommendations.append("🟠 [HTTP] Port 80 is OPEN. Risk: Man-in-the-Middle attacks. \n   Fix: Upgrade to HTTPS (Port 443).")

        if "cve-" in data_lower:
            recommendations.append("⚠️ [VULN] Exploit signatures found in Vuln Audit! Check scan logs for patch references.")

        # Final AI Verdict Logic
        if not recommendations:
            report = "✅ AI VERDICT: System looks secure based on current scan data."
        else:
            # खतरे के हिसाब से वर्डिक्ट बदलें
            prefix = "🛡️ SHIELD-HUB AI SECURITY ALERT:\n" if any("🔴" in r or "🚨" in r for r in recommendations) else "🛡️ AI RECOMMENDATIONS:\n"
            report = prefix + "\n".join(recommendations)

        cb(f"{report}\n" + "="*60 + "\n")

    def export_pdf(self, data, cb):
        os.makedirs("reports", exist_ok=True)
        filename = f"SHIELD_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        path = os.path.join("reports", filename)
        
        try:
            doc = SimpleDocTemplate(path, pagesize=letter)
            styles = getSampleStyleSheet()
            content = []
            
            # PDF Header Logic (Saved Features)
            content.append(Paragraph("🛡️ SHIELD-HUB MASTER SUITE - SECURITY REPORT", styles['Title']))
            content.append(Paragraph(f"Analysis Date: {datetime.now().strftime('%d %B %Y, %H:%M:%S')}", styles['Normal']))
            content.append(Spacer(1, 20))
            
            content.append(Paragraph("TECHNICAL ANALYSIS & RECOMMENDATIONS:", styles['Heading2']))
            
            # Formatting text for PDF
            clean_data = data.replace("\n", "<br/>").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
            content.append(Paragraph(clean_data, styles['Normal']))
            
            content.append(Spacer(1, 20))
            content.append(Paragraph("--- CONFIDENTIAL REPORT: END ---", styles['Italic']))
            
            doc.build(content)
            cb(f"✅ SUCCESS: PDF Report generated: {path}\n")
        except Exception as e: 
            cb(f"❌ ERROR: PDF Export Failed: {str(e)}\n")
