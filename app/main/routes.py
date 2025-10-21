from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from .. import db
from ..models import BetEvent

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
@login_required
def dashboard():
    events = current_user.bet_events
    total = sum(e.amount for e in events)
    return render_template("dashboard.html", events=events, total=total)


@main_bp.post("/add-event")
@login_required
def add_event():
    amount_str = request.form.get("amount", "").strip()
    notes = request.form.get("notes", "").strip()
    try:
        amount = float(amount_str)
    except ValueError:
        flash("Valor inválido.", "error")
        return redirect(url_for("main.dashboard"))

    event = BetEvent(user_id=current_user.id, amount=amount, notes=notes or None)
    db.session.add(event)
    db.session.commit()
    flash("Evento registrado.", "success")
    return redirect(url_for("main.dashboard"))


@main_bp.post("/clear-db")
@login_required
def clear_db():
    if not current_app.debug:
        flash("Operação não permitida fora de modo de desenvolvimento.", "error")
        return redirect(url_for("main.dashboard"))

    db.drop_all()
    db.create_all()
    flash("Banco de dados limpo e recriado.", "success")
    return redirect(url_for("auth.login"))
