#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Viaggio Italia Blog - Un'applicazione web vulnerabile per workshop di sicurezza
Copyright (C) 2025 - Creato per il workshop PyCon Italia

Questo è un blog di viaggio in Italia con vulnerabilità realistiche.
L'applicazione è progettata per essere usata in un workshop educativo
sulla sicurezza informatica. Le vulnerabilità includono:
- SQL Injection
- Cross-Site Scripting (XSS)
- Insecure Direct Object Reference (IDOR)
- Command Injection
- Path Traversal
- Cross-Site Request Forgery (CSRF)
"""

import os
import sqlite3
import subprocess
from flask import Flask, render_template, request, redirect, url_for, session, g, abort, send_file
from werkzeug.utils import secure_filename

# Configurazione dell'applicazione
app = Flask(__name__)
app.secret_key = 'workshop_pycon_italia_2025'
app.config['DATABASE'] = 'viaggio_italia.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Assicuriamo che la directory per gli upload esista
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Connessione al database
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Inizializzazione del database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.executescript(f.read())
        db.commit()

# Route per la homepage
@app.route('/')
def home():
    db = get_db()
    posts = db.execute('SELECT blog_posts.*, users.username FROM blog_posts JOIN users ON blog_posts.author_id = users.id ORDER BY publish_date DESC').fetchall()
    return render_template('home.html', posts=posts)

# Route per la visualizzazione di un singolo articolo
@app.route('/post/<int:post_id>')
def view_post(post_id):
    db = get_db()
    post = db.execute('SELECT blog_posts.*, users.username FROM blog_posts JOIN users ON blog_posts.author_id = users.id WHERE blog_posts.id = ?', [post_id]).fetchone()
    
    if not post:
        abort(404)
    
    # Vulnerabilità: SQL Injection nei commenti (nessuna sanitizzazione)
    search_term = request.args.get('search', '')
    if search_term:
        try:
            # Query vulnerabile a SQLi, ma con gestione errori per evitare crash
            query = f"SELECT comments.*, users.username FROM comments JOIN users ON comments.user_id = users.id WHERE comments.post_id = {post_id} AND comments.content LIKE '%{search_term}%'"
            comments = db.execute(query).fetchall()
        except sqlite3.Error:
            # In caso di errore di sintassi SQL, usiamo la query sicura
            comments = db.execute('SELECT comments.*, users.username FROM comments JOIN users ON comments.user_id = users.id WHERE comments.post_id = ?', [post_id]).fetchall()
    else:
        comments = db.execute('SELECT comments.*, users.username FROM comments JOIN users ON comments.user_id = users.id WHERE comments.post_id = ?', [post_id]).fetchall()
    
    return render_template('post.html', post=post, comments=comments, search_term=search_term)

# Route per aggiungere un commento (vulnerabile a XSS)
@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    if not session.get('user_id'):
        return redirect(url_for('login', next=url_for('view_post', post_id=post_id)))
    
    content = request.form.get('content', '')
    user_id = session['user_id']
    
    db = get_db()
    db.execute('INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)',
              [post_id, user_id, content])  # Nessuna sanitizzazione XSS
    db.commit()
    
    return redirect(url_for('view_post', post_id=post_id))

# Route per la ricerca di articoli (vulnerabile a XSS)
@app.route('/search')
def search():
    search_term = request.args.get('q', '')
    db = get_db()
    
    # Ricerca vulnerabile a SQLi ma gestisce correttamente le categorie predefinite
    if search_term:
        # Categorie speciali che potrebbero contenere apostrofi
        if search_term in ["Città d'Arte", "Mare", "Montagna", "Gastronomia", "Campagna"]:
            # Query per categoria specifica usando parametri (sicuro per categorie predefinite)
            posts = db.execute("SELECT blog_posts.*, users.username FROM blog_posts JOIN users ON blog_posts.author_id = users.id WHERE blog_posts.category = ?", 
                              [search_term]).fetchall()
        else:
            # Query vulnerabile a SQLi per altre ricerche
            query = f"SELECT blog_posts.*, users.username FROM blog_posts JOIN users ON blog_posts.author_id = users.id WHERE blog_posts.title LIKE '%{search_term}%' OR blog_posts.content LIKE '%{search_term}%' OR blog_posts.category LIKE '%{search_term}%'"
            posts = db.execute(query).fetchall()
    else:
        posts = []
    
    return render_template('search.html', posts=posts, search_term=search_term)

# Route per il login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    next_url = request.args.get('next', url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        
        # Query vulnerabile a SQL Injection
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        user = db.execute(query).fetchone()
        
        if user:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            return redirect(next_url)
        else:
            error = 'Credenziali non valide'
    
    return render_template('login.html', error=error)

# Route per il logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Route per il profilo utente (vulnerabile a IDOR)
@app.route('/profile/<int:user_id>')
def profile(user_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', [user_id]).fetchone()
    
    if not user:
        abort(404)
    
    # IDOR: qualsiasi utente può vedere informazioni private di altri utenti
    # Nota: abbiamo sostituito i messaggi con attività utente per maggiore realismo
    # ma manteniamo la vulnerabilità IDOR permettendo a chiunque di vedere il profilo
    
    posts = db.execute('SELECT * FROM blog_posts WHERE author_id = ? ORDER BY publish_date DESC', [user_id]).fetchall()
    
    return render_template('profile.html', user=user, posts=posts)

# Route per l'admin dashboard
@app.route('/admin')
def admin():
    if not session.get('is_admin', False):
        return redirect(url_for('login', next=url_for('admin')))
    
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()
    subscriptions = db.execute('SELECT * FROM subscriptions ORDER BY subscribed_at DESC').fetchall()
    
    return render_template('admin.html', users=users, subscriptions=subscriptions)

# Route per l'esecuzione di comandi (vulnerabile a Command Injection)
@app.route('/admin/system', methods=['GET', 'POST'])
def admin_system():
    if not session.get('is_admin', False):
        return redirect(url_for('login', next=url_for('admin_system')))
    
    output = None
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'disk_space':
            # Vulnerabile a Command Injection
            directory = request.form.get('directory', '/')
            command = f"du -sh {directory}"
            output = subprocess.check_output(command, shell=True, text=True)
        
        elif action == 'network':
            # Vulnerabile a Command Injection
            host = request.form.get('host', 'localhost')
            command = f"ping -c 3 {host}"
            try:
                output = subprocess.check_output(command, shell=True, text=True)
            except subprocess.CalledProcessError:
                output = "Errore nell'esecuzione del comando"
    
    return render_template('system.html', output=output)

# Route per il download di file (vulnerabile a Path Traversal)
@app.route('/download')
def download():
    filename = request.args.get('file')
    
    if not filename:
        abort(400)
    
    # Vulnerabile a Path Traversal
    return send_file(filename)

# Route per la modifica password (vulnerabile a CSRF)
@app.route('/settings/password', methods=['GET', 'POST'])
def change_password():
    if not session.get('user_id'):
        return redirect(url_for('login', next=url_for('change_password')))
    
    error = None
    success = None
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE id = ? AND password = ?', 
                         [session['user_id'], current_password]).fetchone()
        
        if not user:
            error = 'Password attuale non corretta'
        elif new_password != confirm_password:
            error = 'Le nuove password non corrispondono'
        elif len(new_password) < 6:
            error = 'La nuova password deve essere di almeno 6 caratteri'
        else:
            db.execute('UPDATE users SET password = ? WHERE id = ?', 
                      [new_password, session['user_id']])
            db.commit()
            success = 'Password modificata con successo'
    
    return render_template('change_password.html', error=error, success=success)

# Route per l'iscrizione alla newsletter
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    name = request.form.get('name', '')
    
    if not email:
        return redirect(url_for('home'))
    
    db = get_db()
    db.execute('INSERT INTO subscriptions (email, name) VALUES (?, ?)', [email, name])
    db.commit()
    
    return redirect(url_for('home', subscribed=True))

# Funzione per eseguire l'app
if __name__ == '__main__':
    # Inizializzare il database se non esiste
    if not os.path.exists(app.config['DATABASE']):
        init_db()
    
    app.run(debug=True)
