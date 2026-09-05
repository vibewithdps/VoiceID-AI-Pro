with open('server.py', 'r') as f:
    content = f.read()

# Add exception handling to api_register
old_register = """@app.route('/api/auth/register', methods=['POST'])
def api_register():
    data = request.json
    success, message = auth_manager.register(
        data.get('full_name', ''),
        data.get('username', ''),
        data.get('email', ''),
        data.get('password', ''),
        data.get('confirm_password', '')
    )
    if success:
        return jsonify({'status': 'success', 'message': message})
    return jsonify({'status': 'error', 'message': message}), 400"""

new_register = """@app.route('/api/auth/register', methods=['POST'])
def api_register():
    try:
        data = request.json or {}
        success, message = auth_manager.register(
            data.get('full_name', ''),
            data.get('username', ''),
            data.get('email', ''),
            data.get('password', ''),
            data.get('confirm_password', '')
        )
        if success:
            return jsonify({'status': 'success', 'message': message})
        return jsonify({'status': 'error', 'message': message}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500"""

content = content.replace(old_register, new_register)

with open('server.py', 'w') as f:
    f.write(content)
