from flask import Flask, render_template, request, make_response
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic

from config import CONFIG, SECRET

app = Flask(__name__)
authomatic = Authomatic(CONFIG, SECRET, report_errors=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    trusted_proxies = {'127.0.0.1'}
    route = request.access_route + [request.remote_addr]

    remote_addr = next((addr for addr in reversed(route) 
                        if addr not in trusted_proxies), request.remote_addr)
    if remote_addr != "106.69.202.65" and provider_name == "twitch":
        return render_template('sorry.html', msg="This feature is in development! Please come back later or ask me about it in IRC.")
    if not provider_name in CONFIG:
        return render_template('sorry.html', msg="Login endpoint not found.")
    response = make_response()
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)
    if result:
        if result.user:
            result.user.update()
        return render_template('login.html', result=result)
    return response

if __name__ == '__main__':
    app.run(debug=False, port=5343)