🛡️ SHIELD-HUB v41.0

SHIELD-HUB एक एडवांस्ड साइबर-सिक्योरिटी डैशबोर्ड है जिसे Python (CustomTkinter) और Jarvis Voice Engine के साथ बनाया गया है। यह टूल Reconnaissance (टोही), Exploitation, Real-time Defense और AI-driven Analysis को एक ही इंटरफेस में जोड़ता है।

🚀 मुख्य फीचर्स (Core Features)

Phase 1: Recon (📡) - Nmap आधारित एडवांस्ड पोर्ट स्कैनिंग, नेटवर्क मैपिंग और वाई-फाई डिस्कवरी।

Phase 2: Exploit (⚡) - ऑटोमैटिक पेलोड जनरेशन (Msfvenom) और वन-क्लिक Metasploit लिसनर सेटअप।

Phase 3: Defense (☣️) - YARA आधारित मालवेयर डिटेक्शन और रियल-टाइम सस्पिशियस प्रोसेस मॉनिटरिंग।

Phase 4: Intel (🤖) - AI आधारित वल्नरेबिलिटी एनालिसिस और ऑटो-जेनरेटेड PDF रिपोर्ट्स।

Jarvis Voice System - हर एक्शन पर वॉइस फीडबैक और सिक्योरिटी अलर्ट्स।
Self-Destruct (🔥) - एक क्लिक में सभी लॉग्स और पेलोड्स को क्लीन करने की सुविधा।



🛠️ इंस्टॉलेशन (Installation)

1. सिस्टम की ज़रूरतें (Prerequisites)
इस टूल को चलाने के लिए आपके सिस्टम में नीचे दिए गए टूल्स होने ज़रूरी हैं:
Python 3.x

Nmap (नेटवर्क स्कैनिंग के लिए)

Metasploit Framework (पेलोड बनाने के लिए)

Ngrok (Port Forwarding के लिए - ऑप्शनल)


🚀 Setup
Kali Linux या अन्य नए Linux वर्ज़न्स पर 'Externally Managed Environment' एरर से बचने के लिए Virtual Environment का उपयोग करना सबसे बेहतर तरीका है।

यह आपके सिस्टम की पाइथन फाइलों को सुरक्षित रखता है और प्रोजेक्ट की लाइब्रेरीज़ को अलग से मैनेज करता है।
Virtual Environment बनाएं:
bash
python3 -m venv env

इसे एक्टिवेट (Activate) करें:
bash
source env/bin/activate

1. सबसे पहले टर्मिनल खोलें और प्रोजेक्ट डाउनलोड करें or रिपॉजिटरी को क्लोन करें:

**git clone https://github.com/246435F/Shield-Hub**

2. जरूरी सिस्टम टूल्स इंस्टॉल करें (Linux/Kali):
3. sudo apt update
4. sudo apt install nmap msfconsole xterm espeak ngrok
5. Python लाइब्रेरीज इंस्टॉल करें:
6. pip install -r requirements.txt
7. (अगर requirements.txt नहीं है, तो pip install customtkinter psutil requests pyttsx3 reportlab yara-python pillow चलाएं)

नोट: जब भी आप दोबारा इस प्रोजेक्ट पर काम करें, तो पहले source env/bin/activate ज़रूर चलाएं। काम खत्म होने के बाद आप deactivate टाइप करके बाहर आ सकते हैं।
💡 बोनस टिप (Short-cut)
अगर आप वर्चुअल एनवायरनमेंट इस्तेमाल नहीं करना चाहते, तो आप सीधे यह कमांड इस्तेमाल कर सकते हैं (हालांकि यह कम सुरक्षित है):
bash
pip install -r requirements.txt --break-system-packages

ऐप शुरू करने के लिए कमांड चलाएं:

**sudo python3 main.py**


Target IP डालें और Discovery Scan शुरू करें।

AI Analysis बटन दबाकर खतरों की जांच करें।

Export PDF से अपनी प्रोफेशनल रिपोर्ट प्राप्त करें।

काम खत्म होने पर Exit & Cleanup बटन दबाकर अपने डिजिटल फुटप्रिंट्स मिटाएं।


⚠️ डिस्क्लेमर (Disclaimer)

यह प्रोजेक्ट केवल Educational और Ethical Hacking उद्देश्यों के लिए बनाया गया है। बिना अनुमति के किसी भी सिस्टम पर इसका उपयोग अवैध है। डेवलपर किसी भी दुरुपयोग के लिए जिम्मेदार नहीं होगा।
