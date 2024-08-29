import socket
import struct
def robotat_3pi_connect(agent_id):
    if not isinstance(agent_id, int) or agent_id < 0 or agent_id > 19:
        raise ValueError('Invalid agent ID. Allowed IDs: 0 - 19.')

    robot = {}

    if isinstance(agent_id, int):
        robot_id = round(agent_id)
    else:
        raise ValueError('Can only pair with a single 3Pi agent.')

    robot['id'] = robot_id

    if robot_id > 9:
        ip = '192.168.50.1'
    else:
        ip = '192.168.50.10'

    ip = ip + str(robot_id)
    robot['ip'] = ip
    robot['port'] = 9090

    try:
        tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpsock.connect((robot['ip'], robot['port']))
        robot['tcpsock'] = tcpsock
    except Exception as e:
        print('ERROR: Could not connect to the robot.')
        print(e)

    return robot
"""
# Example usage:
try:
    robot = robotat_3pi_connect(5)
    print(f"Connected to robot ID: {robot['id']}, IP: {robot['ip']}, Port: {robot['port']}")
except ValueError as ve:
    print(ve)
except Exception as e:
    print('An error occurred:', e)
"""
def robotat_3pi_disconnect(robot):
    try:
        #robotat_3pi_force_stop(robot)
        del robot
        print('Disconnected from robot.')
    except Exception as e:
        print('An error occurred while disconnecting:', e)

def robotat_3pi_force_stop(robot):
    dphiL = 0.0
    dphiR = 0.0

    # Encode to a simple CBOR array
    cbormsg = bytearray([130, 250]) + struct.pack('<f', dphiL) + bytearray([250]) + struct.pack('<f', dphiR)

    try:
        robot['tcpsock'].sendall(cbormsg)
    except Exception as e:
        print('An error occurred while sending the force stop command:', e)

def robotat_3pi_set_wheel_velocities(robot, dphiL, dphiR):
    wheel_maxvel_rpm = 400
    wheel_minvel_rpm = -400

    if dphiL > wheel_maxvel_rpm:
        print(f'Warning: Left wheel speed saturated to {wheel_maxvel_rpm} rpm')
        dphiL = wheel_maxvel_rpm

    if dphiR > wheel_maxvel_rpm:
        print(f'Warning: Right wheel speed saturated to {wheel_maxvel_rpm} rpm')
        dphiR = wheel_maxvel_rpm

    if dphiL < wheel_minvel_rpm:
        print(f'Warning: Left wheel speed saturated to {wheel_minvel_rpm} rpm')
        dphiL = wheel_minvel_rpm

    if dphiR < wheel_minvel_rpm:
        print(f'Warning: Right wheel speed saturated to {wheel_minvel_rpm} rpm')
        dphiR = wheel_minvel_rpm

    # Encode to a simple CBOR array
    cbormsg = bytearray([130, 250]) + struct.pack('>f', dphiL) + bytearray([250]) + struct.pack('>f', dphiR)

    try:
        robot['tcpsock'].sendall(cbormsg)
    except Exception as e:
        print('An error occurred while sending the wheel velocities command:', e)
