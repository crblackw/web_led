import time

from thing import PiThing

from flask import *

# Create flask app and pi thing.
app = Flask(__name__)
pi_thing = PiThing()


@app.route("/")
def index():
    # Get the switch state and pass down to index template.
    switch = pi_thing.read_switch()
    return render_template('index.html', switch=switch)

@app.route("/led/<int:led_state>", methods=['POST'])
def led(led_state):
    if led_state == 0:
        pi_thing.set_led(False)
    elif led_state == 1:
        pi_thing.set_led(True)
    else:
        return ('Unknown LED state!', 400)
    return ('', 204)

@app.route('/switch')
def switch():
    def get_switch_values():
        while True:
            switch = pi_thing.read_switch()
            yield 'data: {0}\n\n'.format(switch)
            time.sleep(1.0)
    return Response(get_switch_values(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
