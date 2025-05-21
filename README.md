# Python e Cybersecurity: Caccia alle vulnerabilità
## Workshop PyCon Italia 2025

Questo repository contiene il materiale necessario per il workshop "Python e Cybersecurity: Caccia alle vulnerabilità" presentato al PyCon Italia 2025.

## File necessari per il Workshop

Ecco i file essenziali che utilizzerai durante il workshop:

### 1. Applicazione vulnerabile
- `app.py` - L'applicazione web Flask "Viaggio Italia Blog"
- `schema.sql` - Schema del database SQLite
- `init_db.py` - Script per inizializzare il database
- `viaggio_italia.db` - Database SQLite preconfigurato
- `requirements.txt` - Dipendenze Python

### 2. Componenti web
- `static/` - Fogli di stile e immagini
- `templates/` - Template HTML dell'applicazione
- `uploads/` - Directory per upload di file

### 3. Strumenti per la Caccia alle Vulnerabilità
**Da sviluppare nel corso del workshop**

## Setup del Workshop

1. Clona questo repository
2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
3. Inizializza il database (SOLO se non è già presente il file `viaggio_italia.db`):
   ```bash
   python init_db.py
   ```
4. Avvia l'applicazione web:
   ```bash
   python app.py
   ```

## Struttura del Workshop

Il workshop si articola in 4 fasi principali:

1. **Ricognizione**: Analisi della superficie di attacco dell'applicazione
   
2. **Scansione**: Ricerca di vulnerabilità comuni

3. **Exploitation**: Sfruttamento delle vulnerabilità trovate
   
4. **Mitigazione**: Mitigazione delle vulnerabilità con implementazioni più sicure

## Credenziali per il Testing

Per accedere all'applicazione:
- **Admin**: Username: `admin`, Password: `admin123`
- **Utente**: Username: `maria`, Password: `password`

## Vulnerabilità Coperte

- SQL Injection
- Cross-Site Scripting (XSS)
- Command Injection
- Path Traversal / Local File Inclusion
- Insecure Direct Object References (IDOR)
- Cross-Site Request Forgery (CSRF)

## Note Importanti

- Questa applicazione è stata creata **solo per scopi educativi**
- Le tecniche mostrate in questo workshop devono essere utilizzate solo su sistemi per cui si ha autorizzazione
- L'applicazione "Viaggio Italia Blog" contiene vulnerabilità intenzionali per dimostrare concetti di sicurezza

---

© 2025 Giovanni Pedroncelli