import socket
import json
import time
from scipy.spatial.transform import Rotation as R
import numpy as np

def robotat_connect():
    ip = '192.168.50.200'
    port = 1883
    try:
        tcp_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_obj.connect((ip, port))
        return tcp_obj
    except Exception as e:
        print('ERROR: Could not connect to Robotat server.')
        return None

def robotat_disconnect(tcp_obj):
    try:
        tcp_obj.send(b'EXIT')
        tcp_obj.close()
        print('Disconnected from Robotat server.')
    except Exception as e:
        print('Error while disconnecting:', e)

def robotat_get_pose(tcp_obj, agent_id):
    try:
        # Clear any existing data
        #probar
        tcp_obj.settimeout(0.01)
        try:
            tcp_obj.recv(4096)
        except:
            pass
        #tcp_obj.recv(2048)
        #tcp_obj.recv(1024)
        tcp_obj.settimeout(None)
        # Prepare the request payload
        request_payload = {
            "dst": 1,   # DST_ROBOTAT
            "cmd": 1,   # CMD_GET_POSE
            "pld": agent_id
        }

        # Send the request as JSON-encoded data
        tcp_obj.send(json.dumps(request_payload).encode())

        # Receive the response
        response_data = tcp_obj.recv(4096)  # Adjust buffer size as needed

        # Decode and process the response
        if response_data:
            pose_data = json.loads(response_data)
            #new experiment
            n = len(agent_id)
            pose = np.array(pose_data).reshape(n,7)
            return pose
        else:
            print("Received empty response from server.")
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def quat2eul(position_quaternion_array, euler_angles_order):
    # Ensure the input is a NumPy array
    position_quaternion_array = np.array(position_quaternion_array)

    # Extract position and quaternion components for all rows
    positions = position_quaternion_array[:, :3]
    quaternions = position_quaternion_array[:, 3:]

    # Roll the quaternions to change their order
    quaternions_eq = np.roll(quaternions, -1, axis=1)

    # Convert quaternions to Euler angles for all rows
    rotations = R.from_quat(quaternions_eq)
    euler_angles = rotations.as_euler(euler_angles_order, degrees=True)

    # Create a new array with positions and Euler angles
    new_array = np.hstack((positions, euler_angles))

    return new_array