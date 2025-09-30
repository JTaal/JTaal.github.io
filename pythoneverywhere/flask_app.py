from flask import Flask, request, jsonify
from flask_cors import CORS
import gymnasium as gym
import numpy as np
import base64
from PIL import Image
import io
import uuid

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# This dictionary holds all active environment instances.
active_envs = {}

# --- Helper Functions ---

def frame_to_base64(frame: np.ndarray):
    """Converts a numpy array frame from gym to a Base64 encoded PNG."""
    img = Image.fromarray(frame)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_str}"

def serialize_space(space):
    """Converts a gym space object into a simple, JSON-friendly dictionary."""
    if isinstance(space, gym.spaces.Discrete):
        return {'type': 'Discrete', 'n': space.n}
    if isinstance(space, gym.spaces.Box):
        return {
            'type': 'Box',
            'shape': list(space.shape),
            'low': space.low.tolist(),
            'high': space.high.tolist()
        }
    return {'type': 'Unknown'}

# --- Flask Routes ---

@app.route('/', methods=['GET'])
def home():
    """A simple homepage to confirm the Flask app is running."""
    return """
    <html>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
            <h1>Flask Gymnasium API is Running!</h1>
            <p>This is the GET endpoint. The main API logic is at the <code>/gym</code> endpoint, which only accepts POST requests.</p>
        </body>
    </html>
    """

@app.route('/gym', methods=['POST'])
def environment_manager():
    """
    A single endpoint to manage and interact with a Gymnasium environment.
    Handles 'reset', 'step', 'get_info', and 'close' actions.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request must be JSON'}), 400

        action = data.get('action')
        if not action:
            return jsonify({'error': 'No action provided in request body'}), 400

        if action == 'reset':
            env_id = data.get('env_id')
            if not env_id:
                return jsonify({'error': 'env_id is required for the reset action'}), 400

            session_id = str(uuid.uuid4())
            env = gym.make(env_id, render_mode="rgb_array")
            observation, info = env.reset()
            active_envs[session_id] = env

            return jsonify({
                'session_id': session_id,
                'observation': observation.tolist(),
                'info': info
            })

        session_id = data.get('session_id')
        if not session_id or session_id not in active_envs:
            return jsonify({'error': 'A valid session_id is required for this action'}), 400

        env = active_envs[session_id]

        if action == 'step':
            step_action = data.get('step_action')
            if step_action is None:
                return jsonify({'error': 'step_action is required for the step action'}), 400

            obs, reward, terminated, truncated, info = env.step(step_action)
            frame = env.render()

            return jsonify({
                'observation': obs.tolist(),
                'reward': reward,
                'terminated': terminated,
                'truncated': truncated,
                'info': info,
                'frame': frame_to_base64(frame)
            })

        if action == 'get_info':
            return jsonify({
                'action_space': serialize_space(env.action_space),
                'observation_space': serialize_space(env.observation_space)
            })

        if action == 'close':
            env.close()
            del active_envs[session_id]
            return jsonify({'status': 'closed', 'session_id': session_id})

        return jsonify({'error': f'Unknown action: {action}'}), 400

    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

