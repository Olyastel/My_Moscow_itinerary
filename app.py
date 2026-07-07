from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)

# Файлы для хранения данных
MARKERS_FILE = 'markers.json'
AREAS_FILE = 'areas.json'
ROUTES_FILE = 'routes.json'

# Загружаем маркеры
def load_markers():
    if os.path.exists(MARKERS_FILE):
        with open(MARKERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_markers(markers):
    with open(MARKERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(markers, f, ensure_ascii=False, indent=2)

# Загружаем области (парки)
def load_areas():
    if os.path.exists(AREAS_FILE):
        with open(AREAS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_areas(areas):
    with open(AREAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(areas, f, ensure_ascii=False, indent=2)

# Загружаем маршруты
def load_routes():
    if os.path.exists(ROUTES_FILE):
        with open(ROUTES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_routes(routes):
    with open(ROUTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(routes, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

# === МАРКЕРЫ (точки) ===
@app.route('/add_marker', methods=['POST'])
def add_marker():
    data = request.get_json()
    new_marker = {
        'id': str(uuid.uuid4()),
        'lat': data['lat'],
        'lng': data['lng'],
        'name': data.get('name', 'Новое место'),
        'rating': data.get('rating', 'neutral'),
        'comment': data.get('comment', ''),
        'photo': data.get('photo', ''),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    markers = load_markers()
    markers.append(new_marker)
    save_markers(markers)
    return jsonify({'status': 'success', 'message': 'Маркер добавлен!'})

@app.route('/update_marker', methods=['POST'])
def update_marker():
    data = request.get_json()
    marker_id = data.get('id')
    markers = load_markers()
    for marker in markers:
        if marker['id'] == marker_id:
            marker['name'] = data.get('name', marker['name'])
            marker['rating'] = data.get('rating', marker['rating'])
            marker['comment'] = data.get('comment', marker['comment'])
            marker['photo'] = data.get('photo', marker['photo'])
            save_markers(markers)
            return jsonify({'status': 'success', 'message': 'Маркер обновлен!'})
    return jsonify({'status': 'error', 'message': 'Маркер не найден'})

@app.route('/delete_marker', methods=['POST'])
def delete_marker():
    data = request.get_json()
    marker_id = data.get('id')
    markers = load_markers()
    markers = [m for m in markers if m['id'] != marker_id]
    save_markers(markers)
    return jsonify({'status': 'success', 'message': 'Маркер удален!'})

# === ПАРКИ (области) ===
@app.route('/add_area', methods=['POST'])
def add_area():
    data = request.get_json()
    new_area = {
        'id': str(uuid.uuid4()),
        'name': data.get('name', 'Парк'),
        'coordinates': data['coordinates'],
        'rating': data.get('rating', 'neutral'),
        'comment': data.get('comment', ''),
        'photo': data.get('photo', ''),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    areas = load_areas()
    areas.append(new_area)
    save_areas(areas)
    return jsonify({'status': 'success', 'message': 'Парк добавлен!'})

@app.route('/update_area', methods=['POST'])
def update_area():
    data = request.get_json()
    area_id = data.get('id')
    areas = load_areas()
    for area in areas:
        if area['id'] == area_id:
            area['name'] = data.get('name', area['name'])
            area['rating'] = data.get('rating', area['rating'])
            area['comment'] = data.get('comment', area['comment'])
            area['photo'] = data.get('photo', area['photo'])
            save_areas(areas)
            return jsonify({'status': 'success', 'message': 'Парк обновлен!'})
    return jsonify({'status': 'error', 'message': 'Парк не найден'})

@app.route('/delete_area', methods=['POST'])
def delete_area():
    data = request.get_json()
    area_id = data.get('id')
    areas = load_areas()
    areas = [a for a in areas if a['id'] != area_id]
    save_areas(areas)
    return jsonify({'status': 'success', 'message': 'Парк удален!'})

# === МАРШРУТЫ (пути) ===
@app.route('/add_route', methods=['POST'])
def add_route():
    data = request.get_json()
    new_route = {
        'id': str(uuid.uuid4()),
        'name': data.get('name', 'Маршрут'),
        'points': data['points'],  # список [[lat, lng], ...]
        'color': data.get('color', '#1a73e8'),
        'comment': data.get('comment', ''),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    routes = load_routes()
    routes.append(new_route)
    save_routes(routes)
    return jsonify({'status': 'success', 'message': 'Маршрут добавлен!'})

@app.route('/update_route', methods=['POST'])
def update_route():
    data = request.get_json()
    route_id = data.get('id')
    routes = load_routes()
    for route in routes:
        if route['id'] == route_id:
            route['name'] = data.get('name', route['name'])
            route['color'] = data.get('color', route['color'])
            route['comment'] = data.get('comment', route['comment'])
            save_routes(routes)
            return jsonify({'status': 'success', 'message': 'Маршрут обновлен!'})
    return jsonify({'status': 'error', 'message': 'Маршрут не найден'})

@app.route('/delete_route', methods=['POST'])
def delete_route():
    data = request.get_json()
    route_id = data.get('id')
    routes = load_routes()
    routes = [r for r in routes if r['id'] != route_id]
    save_routes(routes)
    return jsonify({'status': 'success', 'message': 'Маршрут удален!'})

# === ПОЛУЧЕНИЕ ВСЕХ ДАННЫХ ===
@app.route('/get_markers', methods=['GET'])
def get_markers():
    markers = load_markers()
    areas = load_areas()
    routes = load_routes()
    return jsonify({
        'markers': markers,
        'areas': areas,
        'routes': routes
    })

@app.route('/clear_all', methods=['POST'])
def clear_all():
    save_markers([])
    save_areas([])
    save_routes([])
    return jsonify({'status': 'success', 'message': 'Все данные удалены'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)