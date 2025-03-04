from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.meal import Meal
from database import db
from datetime import datetime

meals_bp = Blueprint("meals_bp", __name__)

@meals_bp.route("/meal/register", methods=['POST'])
@login_required
def register_meal():
    print(f"Usuário autenticado: {current_user.is_authenticated}, ID: {current_user.get_id()}")

    if not request.is_json:
        return jsonify({"message": "Content-Type must be application/json"}), 400

    try:
        data = request.json
        print(f"Dados recebidos: {data}")

        name = data.get("name")
        description = data.get("description")
        date_str = data.get("date")
        is_in_diet = data.get("is_in_diet")

        if not all([name, description, date_str, is_in_diet]):
            return jsonify({"message": "Dados incompletos"}), 400

        try:
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return jsonify({"message": "Formato de data inválido"}), 400

        meal = Meal(name=name, description=description, date=date, is_in_diet=is_in_diet)
        db.session.add(meal)
        db.session.commit()

        return jsonify({"message": "Refeição registrada com sucesso"}), 201

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"message": "Erro ao registrar refeição"}), 500


