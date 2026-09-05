import os
with open('server.py', 'r') as f:
    content = f.read()

new_endpoints = """
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
"""

content = content.replace("if __name__ == '__main__':", new_endpoints)

with open('server.py', 'w') as f:
    f.write(content)
