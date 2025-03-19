from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 儲存網格狀態
grid_state = {
    'size': 5,
    'start': None,
    'end': None,
    'obstacles': []
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/init_grid', methods=['POST'])
def init_grid():
    global grid_state
    size = int(request.json['size'])
    if 5 <= size <= 9:
        grid_state = {
            'size': size,
            'start': None,
            'end': None,
            'obstacles': []
        }
        return jsonify({'success': True, 'size': size})
    return jsonify({'success': False, 'message': 'Size must be between 5 and 9'})


@app.route('/update_cell', methods=['POST'])
def update_cell():
    global grid_state
    data = request.json
    x, y = data['x'], data['y']
    cell_type = data['type']

    if cell_type == 'start':
        grid_state['start'] = (x, y)
    elif cell_type == 'end':
        grid_state['end'] = (x, y)
    elif cell_type == 'obstacle':
        if len(grid_state['obstacles']) < grid_state['size'] - 2:
            grid_state['obstacles'].append((x, y))

    return jsonify(grid_state)


if __name__ == '__main__':
    app.run(debug=True)