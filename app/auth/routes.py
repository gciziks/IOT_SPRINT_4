from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import select
from .. import db
from ..models import User
from ..face_utils import get_face_embedding_from_base64, match_face

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.get("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("register.html")


@auth_bp.post("/register")
def register_post():
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    face_data = request.form.get("face_data")

    if not username or not email or not password:
        flash("Preencha todos os campos.", "error")
        return redirect(url_for("auth.register"))

    existing = db.session.execute(select(User).where((User.username == username) | (User.email == email))).scalar_one_or_none()
    if existing:
        flash("Usuário ou email já existe.", "error")
        return redirect(url_for("auth.register"))

    user = User(username=username, email=email)
    user.set_password(password)

    if face_data:
        embedding = get_face_embedding_from_base64(face_data)
        if embedding is None:
            flash("Não foi possível capturar o rosto. Tente novamente.", "error")
            return redirect(url_for("auth.register"))
        user.face_embedding = {"vector": embedding}

    db.session.add(user)
    db.session.commit()
    flash("Registro realizado com sucesso. Faça login.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("login.html")


@auth_bp.post("/login")
def login_post():
    username_or_email = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    user = db.session.execute(
        select(User).where((User.username == username_or_email) | (User.email == username_or_email.lower()))
    ).scalar_one_or_none()

    if not user or not user.check_password(password):
        flash("Credenciais inválidas.", "error")
        return redirect(url_for("auth.login"))

    login_user(user)
    return redirect(url_for("main.dashboard"))


@auth_bp.get("/login-face")
def login_face():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("login_face.html")


@auth_bp.post("/login-face")
def login_face_post():
    data = request.get_json(silent=True) or {}
    data_url = data.get("face_data")

    if not data_url:
        return jsonify({"ok": False, "message": "Imagem não recebida"}), 400

    embedding = get_face_embedding_from_base64(data_url)
    if embedding is None:
        return jsonify({"ok": False, "message": "Rosto não detectado"}), 400

    candidates = db.session.execute(select(User).where(User.face_embedding.is_not(None))).scalars().all()
    best_user = None
    best_score = -1.0
    for u in candidates:
        stored = (u.face_embedding or {}).get("vector")
        if not stored:
            continue
        matched, score = match_face(embedding, stored)
        if score > best_score and matched:
            best_score = score
            best_user = u

    if not best_user:
        return jsonify({"ok": False, "message": "Usuário não reconhecido"}), 401

    login_user(best_user)
    return jsonify({"ok": True, "redirect": url_for("main.dashboard")})


@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
