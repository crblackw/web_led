import time
import json

from thing import PiThing

from flask import *

# Create flask app and pi thing.
app = Flask(__name__)
pi_thing = PiThing()


# Define app routes.
# Index toure renders the main HTML page
@app.route("/")
def index():
    # Get the switch state and pass down to index template.
    switch = pi_thing.read_switch()
    return render_template('index.html', switch=switch)

# LED route allows changing the LED state with a POST request.
@app.route("/led/<int:led_state>", methods=['POST'])
def led(led_state):
    if led_state == 0:
        pi_thing.set_led(False)
    elif led_state == 1:
        pi_thing.set_led(True)
    else:
        return ('Unknown LED state!', 400)
    return ('', 204)

# Server-sent event endpoint that streams the data every second.
@app.route("/thing")
def thing():
    def read_thing_state():
        while True:
            thing_state = {
                'switch': pi_thing.read_switch(),
                'temperature': pi_thing.get_temperature(),
                'light': pi_thing.get_light()
            }
            yield 'data: {0}\n\n'.format(json.dumps(thing_state))
            time.sleep(1.0)
    return Response(read_thing_state(), mimetype='text/event-stream')

# State the flask debug server listening on the pi port 5000 by default.
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
