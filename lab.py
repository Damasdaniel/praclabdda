from flask import Flask, jsonify, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///directories.db'
db = SQLAlchemy(app)

class Directory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    emails = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'emails': self.emails.split(',') if self.emails else []
        }

@app.route('/status/')
def status():
    return "pong"

@app.route('/directories/', methods=['GET'])
def get_directories():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Ajustable
    directories = Directory.query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'count': directories.total,
        'next': url_for('get_directories', page=directories.next_num) if directories.has_next else None,
        'previous': url_for('get_directories', page=directories.prev_num) if directories.has_prev else None,
        'results': [directory.to_dict() for directory in directories.items]
    })

@app.route('/directories/', methods=['POST'])
def create_directory():
    data = request.get_json()
    directory = Directory(name=data['name'], emails=','.join(data['emails']))
    db.session.add(directory)
    db.session.commit()
    return jsonify(directory.to_dict()), 201

@app.route('/directories/<int:id>', methods=['GET'])
def get_directory(id):
    directory = Directory.query.get_or_404(id)
    return jsonify(directory.to_dict())

@app.route('/directories/<int:id>', methods=['PUT'])
def update_directory(id):
    directory = Directory.query.get_or_404(id)
    data = request.get_json()
    directory.name = data['name']
    directory.emails = ','.join(data['emails'])
    db.session.commit()
    return jsonify(directory.to_dict())

@app.route('/directories/<int:id>', methods=['PATCH'])
def partial_update_directory(id):
    directory = Directory.query.get_or_404(id)
    data = request.get_json()
    if 'name' in data:
        directory.name = data['name']
    if 'emails' in data:
        directory.emails = ','.join(data['emails'])
    db.session.commit()
    return jsonify(directory.to_dict())

@app.route('/directories/<int:id>', methods=['DELETE'])
def delete_directory(id):
    directory = Directory.query.get_or_404(id)
    db.session.delete(directory)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
