from flask import current_app as app, jsonify, request
from .models import Account, db

@app.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = Account.query.all()
    return jsonify([a.to_dict() for a in accounts])

@app.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    new_account = Account(
        name=data['name'],
        email=data['email'],
        address=data.get('address', '')
    )
    db.session.add(new_account)
    db.session.commit()
    return jsonify(new_account.to_dict()), 201

@app.route('/accounts/<int:id>', methods=['GET'])
def get_account(id):
    account = Account.query.get_or_404(id)
    return jsonify(account.to_dict())

@app.route('/accounts/<int:id>', methods=['PUT'])
def update_account(id):
    account = Account.query.get_or_404(id)
    data = request.get_json()
    account.name = data.get('name', account.name)
    account.email = data.get('email', account.email)
    account.address = data.get('address', account.address)
    db.session.commit()
    return jsonify(account.to_dict())

@app.route('/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    account = Account.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    return '', 204
