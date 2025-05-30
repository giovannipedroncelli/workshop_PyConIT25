# Python e Cybersecurity: Caccia alle vulnerabilità
## Workshop PyCon Italia 2025

Questo repository contiene il materiale per il workshop "Python e Cybersecurity: Caccia alle vulnerabilità" presentato al PyCon Italia 2025. Un'esperienza pratica di ethical hacking usando Python contro un'applicazione web vulnerabile.

## 🎯 Obiettivo del Workshop

Imparare le basi dell'ethical hacking attraverso un approccio pratico:
- **Scoprire** vulnerabilità comuni nelle web application
- **Sfruttare** le vulnerabilità usando Python
- **Implementare** difese efficaci
- **Sviluppare** una mentalità di sicurezza

## 📁 Struttura del Repository

### Applicazione Vulnerabile: "Viaggio Italia Blog"
- `app.py` - Applicazione Flask con vulnerabilità intenzionali
- `viaggio_italia.db` - Database SQLite preconfigurato
- `requirements.txt` - Dipendenze Python essenziali

### Template e Assets
- `templates/` - Template HTML (login, profili, admin, etc.)
- `static/` - CSS, immagini e assets
- `uploads/` - Directory per upload di file

## 🚀 Setup del Workshop

### Installazione
```bash
# 1. Clona il repository
git clone https://github.com/giovannipedroncelli/workshop_PyConIT25.git
cd workshop_PyConIT25

# 2. Installa le dipendenze
pip install -r requirements.txt

# 3. Avvia l'applicazione vulnerabile
python app.py

# 4. Apri il browser
# http://localhost:5000
```

### Test dell'Installazione
```bash
# Verifica che l'app sia raggiungibile
curl http://localhost:5000
```

## 🏗️ Struttura del Workshop

Il workshop segue un approccio pratico strutturato in **5 fasi**:

### **📋 Fase 1: Setup & HTTP Fundamentals**
- Configurazione dell'ambiente
- Comprensione delle basi HTTP
- Presentazione del target "Viaggio Italia Blog"

### **🔍 Fase 2: Reconnaissance** 
- Mappatura dell'applicazione
- Identificazione della superficie di attacco
- **Tool**: `scripts/recon.py`

### **🔎 Fase 3: Vulnerability Discovery**
- Analisi delle vulnerabilità presenti
- Testing manuale e automatico
- **Tools**: Scripts di exploitation specifici

### **⚔️ Fase 4: Ethical Exploitation**
- Demonstration pratica degli attacchi
- Automation con Python
- **Tools**: Tutti gli script in `scripts/`

### **🛡️ Fase 5: Protection & Mitigation**
- Implementazione delle difese
- Best practices di sicurezza
- Principi OWASP
## 🎯 Vulnerabilità Implementate

L'applicazione "Viaggio Italia Blog" contiene le seguenti vulnerabilità intenzionali:

### **💉 SQL Injection**
- **Endpoint**: `/login` (POST), `/search` (GET)
- **Causa**: Input utente direttamente nelle query SQL

### **🔥 Cross-Site Scripting (XSS)**
- **Endpoint**: `/post/<id>/comment` (POST)
- **Tipo**: Stored XSS nei commenti

### **🔓 Insecure Direct Object References (IDOR)**
- **Endpoint**: `/profile/<user_id>` (GET)
- **Causa**: Nessun controllo di accesso sui profili
- **Test**: Accesso diretto a profili di altri utenti

### **💻 Command Injection**
- **Endpoint**: `/admin/system` (POST)
- **Causa**: shell=True con input utente non validato

### **📁 Path Traversal**
- **Endpoint**: `/download` (GET)
- **Causa**: Nessuna validazione dei percorsi file
- **Test**: `../../../etc/passwd`

### **🔄 Cross-Site Request Forgery (CSRF)**
- **Endpoint**: `/settings/password` (POST)
- **Causa**: Nessun token CSRF

## 🔐 Credenziali di Test

### Account Predefiniti
```
👑 Admin:  admin / admin123
👤 User:   maria / password123
👤 User:   luca / password123
👤 User:   giulia / password123
```

### Endpoints Principali
```
🏠 Home:           /
🔍 Search:         /search
👤 Login:          /login
🏛️ Admin Panel:    /admin
⚙️ System Tools:   /admin/system
📁 File Download:  /download
🔧 Settings:       /settings/password
👥 Profiles:       /profile/<id>
```

## 🛡️ Tecniche di Mitigazione

Durante il workshop imparerai a implementare:

- **Prepared Statements** per prevenire SQL Injection
- **Input Sanitization** per prevenire XSS
- **Access Control** per prevenire IDOR
- **Input Validation** per prevenire Command Injection
- **Path Validation** per prevenire Path Traversal
- **CSRF Tokens** per prevenire CSRF

## ⚠️ Note Importanti

- 🎓 **Solo scopi educativi**: Questa applicazione è creata esclusivamente per formazione
- 🎯 **Ethical Hacking**: Le tecniche mostrate devono essere usate solo su sistemi autorizzati
- 🔒 **Ambiente controllato**: Non utilizzare mai questi attacchi su sistemi di produzione
- 📖 **Apprendimento responsabile**: L'obiettivo è imparare a difendere, non ad attaccare

## 📚 Risorse Aggiuntive

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [Flask Security Documentation](https://flask.palletsprojects.com/en/2.3.x/security/)

---

**👨‍💻 Autore**: Giovanni Pedroncelli  
**📧 Contatto**: gi.pedroncelli@gmail.com  
**🐙 GitHub**: github.com/giovannipedroncelli  
**🎓 Evento**: PyCon Italia 2025