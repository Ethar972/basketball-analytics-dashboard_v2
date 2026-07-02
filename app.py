from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/matches', methods=['GET'])
def get_matches():
    matches_data = [
        { "name": "Al Ahly VS City Oilers", "banner": "ahlyciityban.avif", "team1": "Al Ahly", "team2": "City Oilers" },
        { "name": "Al Ittihad VS Rivers Hoopers", "banner": "aiavsrh.jpg", "team1": "Al Ittihad", "team2": "Rivers Hoopers" },
        { "name": "Zamalek VS CTT", "banner": "zamalekctt.jpg", "team1": "Zamalek", "team2": "CTT" }
    ]
    return jsonify(matches_data)

@app.route('/api/news', methods=['GET'])
def get_news():
    return jsonify([])

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Backend is running successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
