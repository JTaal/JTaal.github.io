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
# Enable CORS for your entire app
CORS(app)

# This dictionary holds all active environment instances.
active_envs = {}

# --- Helper Functions ---

def convert_numpy_types(obj):
    """
    Recursively converts NumPy and non-standard float types in an object
    to their standard Python equivalents, making them JSON serializable.
    Replaces infinity and NaN with None (which becomes null in JSON).
    """
    if isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    # np.ndarray needs to be treated like a list for recursion
    if isinstance(obj, (list, np.ndarray)):
        return [convert_numpy_types(i) for i in obj]
    if isinstance(obj, np.integer):
        return int(obj)
    # This check handles both standard floats and numpy floats
    if isinstance(obj, (np.floating, float)):
        # Check for infinity or NaN, which are not valid JSON
        if np.isinf(obj) or np.isnan(obj):
            return None  # JSON standard does not support Infinity or NaN, convert to null
        return float(obj)
    return obj

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
        return convert_numpy_types({'type': 'Discrete', 'n': space.n})
    if isinstance(space, gym.spaces.Box):
        # The conversion function will handle any infinity values in low/high
        return convert_numpy_types({
            'type': 'Box',
            'shape': list(space.shape),
            'low': space.low,
            'high': space.high
        })
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
    Manages and interacts with a Gymnasium environment.
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

            response_data = {
                'session_id': session_id,
                'observation': observation,
                'info': info
            }
            return jsonify(convert_numpy_types(response_data))

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

            response_data = {
                'observation': obs,
                'reward': reward,
                'terminated': terminated,
                'truncated': truncated,
                'info': info,
                'frame': frame_to_base64(frame)
            }
            return jsonify(convert_numpy_types(response_data))

        if action == 'get_info':
            response_data = {
                'action_space': serialize_space(env.action_space),
                'observation_space': serialize_space(env.observation_space)
            }
            return jsonify(convert_numpy_types(response_data))

        if action == 'close':
            env.close()
            del active_envs[session_id]
            return jsonify({'status': 'closed', 'session_id': session_id})

        return jsonify({'error': f'Unknown action: {action}'}), 400

    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

