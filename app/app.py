from flask import Flask, render_template, jsonify, request
import threading
import webbrowser
import time
import subprocess
import sys
import argparse

"""
    Frontend nipple control over a network 
"""

# Construct Server
app = Flask(__name__)

# User data accessed by server requests
app.data = {
}

@app.route('/')
def index():
    return "TODO"

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

# @app.route('/orientation')
# def orientation():
#     """
#         Returns pitch, yaw and roll
#     """
#     nipple_stream = app.data["nipple_stream"]

#     with nipple_stream.lock:
#         return jsonify({
#             "pitch": nipple_stream.pitch,
#             "yaw": nipple_stream.yaw,
#             "roll": nipple_stream.roll
#     })

# @app.route("/set_deep_freeze")
# def set_deep_freeze():
#     nipple_stream = app.data["nipple_stream"]
#     with nipple_stream.lock:
#         nipple_stream.set_deep_freeze()

#     return "done"

# @app.route("/set_mode", methods=["POST"])
# def set_mode():
#     """
#         Set a NippleStream mode
#     """
#     nipple_stream = app.data["nipple_stream"]
#     mode = request.form["mode"]

#     with nipple_stream.lock:
#         nipple_stream.set_mode(mode)

#     return "done"

# @app.route("/set_control", methods=["POST"])
# def set_control():
#     """
#         Set a NippleStream control
#     """
#     nipple_stream = app.data["nipple_stream"]
#     control = request.form["control"]
#     val = request.form["val"]

#     with nipple_stream.lock:
#         if control == "pitchOffset":
#             nipple_stream.pitch_offset = float(val)

#         elif control == "yawOffset":
#             nipple_stream.yaw_offset = float(val)

#         elif control == "rollOffset":
#             nipple_stream.roll_offset = float(val)

#         elif control == "pitchWidth":
#             nipple_stream.pitch_width = float(val)

#         elif control == "yawWidth":
#             nipple_stream.yaw_width = float(val)

#         elif control == "rollWidth":
#             nipple_stream.roll_width = float(val)

#         elif control == "pitchMute":
#             nipple_stream.pitch_mute = val == 'true'

#         elif control == "yawMute":
#             nipple_stream.yaw_mute = val == 'true'

#         elif control == "rollMute":
#             nipple_stream.roll_mute = val == 'true'

#         else:
#             raise Exception("Unkonwn control %s"%control)

#     return "done"

# @app.route("/map", methods=["POST"])
# def map_axis():
#     """
#         Send 0 over midi to a given axis
#     """
#     axis = request.form["axis"]
#     nipple_stream = app.data["nipple_stream"]

#     with nipple_stream.lock:
#         nipple_stream.send_midi(axis, 0)

#     return "done"


def main(args):
    """
        Run server
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--open", action="store_true")
    parser.add_argument("--host", default="127.0.0.1", help="host")
    parser.add_argument("--port", default=5000, help="port")

    parsed = parser.parse_args(args)

    # # Open page
    # # HACK: Best to launch page on a server run event, but this works on osx =]
    # if parsed.open and sys.platform == "darwin":
    #     chrome_thread = threading.Thread(target=lambda: subprocess.call([
    #         "open", 
    #         "http://%s:%i"%(parsed.host, parsed.port)
    #     ]))
    #     chrome_thread.run()

    # Run Server
    app.run(debug=parsed.debug, host=parsed.host, port=parsed.port)

if __name__ == '__main__':
    main(sys.argv[1:])