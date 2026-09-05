import os
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from werkzeug.utils import secure_filename
from app.auth.auth_manager import AuthManager
from app.ml.predictor import SpeakerPredictor
from app.audio.audio_utils import ensure_directory
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'voiceid_pro_super_secret_key'  # In production, use os.environ.get('SECRET_KEY')

auth_manager = AuthManager()

# Setup paths
UPLOAD_FOLDER = Path("dataset/uploads")
ensure_directory(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

try:
    predictor = SpeakerPredictor()
except Exception as e:
    predictor = None
    print(f"Warning: Predictor failed to load. Models may not be trained yet. {e}")

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('landing'))
    return render_template('dashboard.html', user_name=session.get('full_name'))

@app.route('/api/auth/register', methods=['POST'])
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
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
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
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'status': 'success', 'message': 'Logged out'})

@app.route('/api/predict', methods=['POST'])
def api_predict():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        
    if not predictor:
        return jsonify({'status': 'error', 'message': 'Predictor not initialized (No trained model found)'}), 500
        
    if 'audio' not in request.files:
        return jsonify({'status': 'error', 'message': 'No audio file provided'}), 400
        
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400
        
    if file:
        filename = secure_filename(file.filename or 'recording.wav')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            result = predictor.predict(filepath)
            return jsonify({
                'status': 'success',
                'speaker': result.speaker,
                'confidence': f"{result.confidence:.2f}%"
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500


from app.ml.trainer import AudioTrainer
import joblib

@app.route('/api/dataset/save', methods=['POST'])
def api_save_dataset():
    if 'audio' not in request.files:
        return jsonify({'status': 'error', 'message': 'No audio file provided'}), 400
    
    speaker_name = request.form.get('speaker_name', '').strip()
    if not speaker_name:
        return jsonify({'status': 'error', 'message': 'Speaker name required'}), 400

    file = request.files['audio']
    if file:
        speaker_dir = os.path.join('dataset', speaker_name)
        ensure_directory(speaker_dir)
        # Count existing files to name the new one
        count = len([name for name in os.listdir(speaker_dir) if os.path.isfile(os.path.join(speaker_dir, name))])
        filename = f"voice_{count+1:03d}.wav"
        filepath = os.path.join(speaker_dir, filename)
        file.save(filepath)
        return jsonify({'status': 'success', 'message': f'Saved sample for {speaker_name}'})

@app.route('/api/dataset/train', methods=['POST'])
def api_train_model():
    try:
        trainer = AudioTrainer()
        result = trainer.train()
        
        # Reload predictor globally
        global predictor
        predictor = SpeakerPredictor()
        
        return jsonify({
            'status': 'success', 
            'message': f'Model trained with {result.best_algorithm}. Accuracy: {result.accuracy*100:.2f}%'
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':

    app.run(debug=True, port=5000)
