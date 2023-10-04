from app import app

from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from .forms import RegisterForm, LoginForm, SearchForm
from .models import db, User

import requests as r

def get_pokemon(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = r.get(url)
    if response.ok:
        data = response.json()
        
        output = {
            'pokemon_name': data['species']['name'],
            'ability-name': data['abilities'][0]['ability']['name'],
            'image_url': data['sprites']['front_default'],
            'attack': data['stats'][1]['base_stat'],
            'hp': data['stats'][0]['base_stat'],
            'defense': data['stats'][2]['base_stat']
            }
        return output 

@app.route("/")
def index():
    return render_template("index.html")

    
    
@app.route("/register", methods=["GET","POST"])
def register_page():
    form = RegisterForm()

    if request.method == "POST":
        if form.validate():
            email = form.email.data
            password = form.password.data
            
            new_user = User(email=email, password=password)
            new_user.save()
            
            return redirect(url_for('login_page'))

        else:
            return render_template("register.html", form=form)
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET","POST"])
def login_page():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            email = form.email.data
            password = form.password.data
            
            user = User.query.filter_by(email=email).first()
            if not user:
                return render_template("login.html", form=form)
            else:       
                if user.check_password(password):
                    login_user(user)
                    return redirect(url_for('search_page'))
                else:
                    return render_template("login.html", form=form)
        else:
            return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form) 
        
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login_page'))
    
@app.route("/search", methods=["GET", "POST"])
@login_required
def search_page():
    form = SearchForm()
    if request.method == 'POST':
        if form.validate():
            pokesearch = form.pokesearch.data
            data = get_pokemon(pokesearch)
            return render_template('search.html', form = form, data = data)
    return render_template('search.html', form = form)
            
   