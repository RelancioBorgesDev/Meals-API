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
        data = request.get_json()
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

@meals_bp.route("/meal/edit/<int:id_meal>", methods=['POST'])
@login_required
def edit_meal(id_meal):
    data = request.get_json()
    meal = Meal.query.get(id_meal)

    if not meal:
        return jsonify({"message": "Refeição não encontrada"}), 404

    try:
        meal.name = data.get("name", meal.name)
        meal.description = data.get("description", meal.description)
        meal.date_str = data.get("date", meal.date)

        if "is_in_diet" in data:
            if isinstance(data["is_in_diet"], bool):
                meal.is_in_diet = data["is_in_diet"]
            else:
                meal.is_in_diet = str(data["is_in_diet"]).strip().lower() in ["true", "1", "yes"]

        db.session.commit()
        return jsonify({"message": f"Refeição {id_meal} atualizada com sucesso"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao atualizar refeição", "error": str(e)}), 500

@meals_bp.route("/meal/delete/<int:id_meal>", methods=['DELETE'])
@login_required
def delete_meal(id_meal):
    meal = Meal.query.get(id_meal)

    if not meal:
        return jsonify({"message": "Refeição não encontrada"}), 404
    else:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": f"Usuário {id_meal} deletado com sucesso"})



