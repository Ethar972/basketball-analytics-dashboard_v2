from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
# تفعيل الـ CORS عشان يسمح للـ Angular يكلم السيرفر بدون قيود
CORS(app)

TEAMS_FILE = 'teams.json'
MATCHES_FILE = 'matches.json'
NEWS_FILE = 'news.json'
PLAYERS_FILE = 'players.json'

UPLOAD_CSVS = 'static/csvs'
UPLOAD_IMAGES = 'static/images'
os.makedirs(UPLOAD_CSVS, exist_ok=True)
os.makedirs(UPLOAD_IMAGES, exist_ok=True)

def read_json(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        try: return json.load(f)
        except: return []

def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def admin_home():
    return render_template('index.html')

# ----------------- TEAMS & PLAYERS API -----------------
@app.route('/api/teams', methods=['GET', 'POST'])
def handle_teams():
    teams = read_json(TEAMS_FILE)
    if request.method == 'POST':
        data = request.json
        if not data or not data.get('name'):
            return jsonify({"error": "Missing name"}), 400
        new_team = {
            "id": len(teams) + 1,
            "name": data.get('name').strip(),
            "category": data.get('category', 'First Team')
        }
        teams.append(new_team)
        write_json(TEAMS_FILE, teams)
        return jsonify({"message": "Saved successfully"}), 201
    return jsonify(teams)

@app.route('/api/teams/<int:item_id>', methods=['DELETE'])
def delete_team(item_id):
    teams = read_json(TEAMS_FILE)
    write_json(TEAMS_FILE, [t for t in teams if t.get('id') != item_id])
    return jsonify({"message": "Deleted successfully"})

@app.route('/api/players', methods=['GET', 'POST'])
def handle_players():
    players = read_json(PLAYERS_FILE)
    if request.method == 'POST':
        name = request.form.get('name')
        number = request.form.get('number')
        position = request.form.get('position')
        team_id = request.form.get('team_id')
        
        if not name or not number or not position or not team_id:
            return jsonify({"error": "Missing fields"}), 400
            
        img_filename = ""
        if 'player_img' in request.files:
            file = request.files['player_img']
            if file and file.filename != '':
                img_filename = file.filename
                file.save(os.path.join(UPLOAD_IMAGES, img_filename))
                
        new_player = {
            "id": len(players) + 1,
            "name": name.strip(),
            "number": number.strip(),
            "position": position.strip(),
            "team_id": int(team_id),
            "image": img_filename
        }
        players.append(new_player)
        write_json(PLAYERS_FILE, players)
        return jsonify({"message": "Saved successfully"}), 201
    return jsonify(players)

@app.route('/api/players/<int:item_id>', methods=['DELETE'])
def delete_player(item_id):
    players = read_json(PLAYERS_FILE)
    write_json(PLAYERS_FILE, [p for p in players if p.get('id') != item_id])
    return jsonify({"message": "Deleted successfully"})

# ----------------- MATCHES API (UPDATED WITH COLORS) -----------------
@app.route('/api/matches', methods=['GET', 'POST'])
def handle_matches():
    matches = read_json(MATCHES_FILE)
    if request.method == 'POST':
        title = request.form.get('title')
        team1 = request.form.get('team1')
        team2 = request.form.get('team2')
        primary_color = request.form.get('primary_color', '#ff6600')
        secondary_color = request.form.get('secondary_color', '#0066cc')
        match_video = request.form.get('match_video', '')
        highlights = request.form.get('highlights', '')
        
        if not title or not team1 or not team2:
            return jsonify({"error": "Missing fields"}), 400
            
        banner_filename = ""
        if 'match_banner' in request.files:
            b_file = request.files['match_banner']
            if b_file and b_file.filename != '':
                banner_filename = b_file.filename
                b_file.save(os.path.join(UPLOAD_IMAGES, banner_filename))

        csv1_filename = ""
        csv2_filename = ""
        if 'match_csv1' in request.files:
            file1 = request.files['match_csv1']
            if file1 and file1.filename != '':
                csv1_filename = file1.filename
                file1.save(os.path.join(UPLOAD_CSVS, csv1_filename))
                
        if 'match_csv2' in request.files:
            file2 = request.files['match_csv2']
            if file2 and file2.filename != '':
                csv2_filename = file2.filename
                file2.save(os.path.join(UPLOAD_CSVS, csv2_filename))
        
        new_match = {
            "id": len(matches) + 1,
            "title": title.strip(),
            "name": title.strip(),
            "banner": banner_filename,
            "team1": team1.strip(),
            "team2": team2.strip(),
            "primary_color": primary_color.strip(),
            "secondary_color": secondary_color.strip(),
            "csv_file1": csv1_filename,
            "csv_file2": csv2_filename,
            "match_video": match_video.strip(),
            "highlights": highlights.strip()
        }
        matches.append(new_match)
        write_json(MATCHES_FILE, matches)
        return jsonify({"message": "Saved successfully"}), 201
    return jsonify(matches)

@app.route('/api/matches/<int:item_id>', methods=['DELETE'])
def delete_match(item_id):
    matches = read_json(MATCHES_FILE)
    write_json(MATCHES_FILE, [m for m in matches if m.get('id') != item_id])
    return jsonify({"message": "Deleted successfully"})

# ----------------- NEWS API (WITH DATE) -----------------
@app.route('/api/news', methods=['GET', 'POST'])
def handle_news():
    news = read_json(NEWS_FILE)
    if request.method == 'POST':
        data = request.json
        if not data or not data.get('title') or not data.get('content'):
            return jsonify({"error": "Cannot be added"}), 400
        
        news_date = data.get('date') if data.get('date') else datetime.now().strftime('%Y-%m-%d')
        
        new_story = {
            "id": len(news) + 1,
            "title": data.get('title').strip(),
            "content": data.get('content').strip(),
            "image": data.get('image', '').strip(),  
            "video": data.get('video', '').strip(),
            "date": news_date
        }
        news.append(new_story)
        write_json(NEWS_FILE, news)
        return jsonify({"message": "Saved successfully"}), 201
    return jsonify(news)

@app.route('/api/news/<int:item_id>', methods=['DELETE'])
def delete_news(item_id):
    news = read_json(NEWS_FILE)
    write_json(NEWS_FILE, [n for n in news if n.get('id') != item_id])
    return jsonify({"message": "Deleted successfully"})

# التعديل هنا: تشغيل السيرفر على host='0.0.0.0' لحل مشكلة الاتصال مع الـ Angular
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)