with open('server.py', 'r') as f:
    content = f.read()

old_login = """@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.json
    success, result = auth_manager.login(
        data.get('email', ''),
        data.get('password', '')
    )
    if success:
        user = result
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['full_name'] = user[2]
        session['email'] = user[3]
        return jsonify({'status': 'success', 'message': 'Logged in successfully'})
    return jsonify({'status': 'error', 'message': result}), 401"""

new_login = """@app.route('/api/auth/login', methods=['POST'])
def api_login():
    try:
        data = request.json or {}
        success, result = auth_manager.login(
            data.get('email', ''),
            data.get('password', '')
        )
        if success:
            user = result
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['full_name'] = user[2]
            session['email'] = user[3]
            return jsonify({'status': 'success', 'message': 'Logged in successfully'})
        return jsonify({'status': 'error', 'message': result}), 401
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500"""

content = content.replace(old_login, new_login)
with open('server.py', 'w') as f:
    f.write(content)
