## TEST LOCAL API server with Flask
import flask
from flask import request, redirect, jsonify
import json
import test_api_data

###### BELOW IS THE PARAMS INFO FOR FLASK.RUN()
###### THESE ARE PULLED FROM "../flask/app.py"
###### pip PACKAGE ROOT
##def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
##"""Runs the application on a local development server.
##
##Do not use ``run()`` in a production setting. It is not intended to
##meet security and performance requirements for a production server.
##Instead, see :ref:`deployment` for WSGI server recommendations.
##
##If the :attr:`debug` flag is set the server will automatically reload
##for code changes and show a debugger in case an exception happened.
##
##If you want to run the application in debug mode, but disable the
##code execution on the interactive debugger, you can pass
##``use_evalex=False`` as parameter.  This will keep the debugger's
##traceback screen active, but disable code execution.
##
##It is not recommended to use this function for development with
##automatic reloading as this is badly supported.  Instead you should
##be using the :command:`flask` command line script's ``run`` support.
##
##.. admonition:: Keep in Mind
##
##Flask will suppress any server error with a generic error page
##unless it is in debug mode.  As such to enable just the
##interactive debugger without the code reloading, you have to
##invoke :meth:`run` with ``debug=True`` and ``use_reloader=False``.
##Setting ``use_debugger`` to ``True`` without being in debug mode
##won't catch any exceptions because there won't be any to
##catch.
##
##:param host: the hostname to listen on. Set this to ``'0.0.0.0'`` to
##have the server available externally as well. Defaults to
##``'127.0.0.1'`` or the host in the ``SERVER_NAME`` config variable
##if present.
##:param port: the port of the webserver. Defaults to ``5000`` or the
##port defined in the ``SERVER_NAME`` config variable if present.
##:param debug: if given, enable or disable debug mode. See
##:attr:`debug`.
##:param load_dotenv: Load the nearest :file:`.env` and :file:`.flaskenv`
##files to set environment variables. Will also change the working
##directory to the directory containing the first file found.
##:param options: the options to be forwarded to the underlying Werkzeug
##server. See :func:`werkzeug.serving.run_simple` for more
##information.
###########################################################################

app = flask.Flask(__name__)
app_unsecure = flask.Flask(__name__)

def launch_unsecure_api():
    return app_unsecure
    
## Below r attempts to do redirects to https but not working ######
##@app.before_request
##def before_request():
##    if not request.url.startswith("https://127.0.0.1"):
##        print("Non Request to loopback")
##        url = request.url.replace('http://', 'https://', 1)
##        code = 301
##        return redirect(url, code=code)
##@app.before_request
##def before_request():
##    if not request.is_secure:# and app.env != "development":
##        url = request.url.replace("http://", "https://", 1)
##        code = 301
##        return redirect(url, code=code)

## ENABLE DEBUG... Which never works
#app.config["DEBUG"] = True

## BEGIN API paths for requests #####################
    
@app.route("/", methods=["GET"])
def home():
    return "<h1>Dev5 RESTful API - Testing Server</h1><p>This site is a prototype API for locating the droids you are looking for. </p>\n" \
           "<p>Just FYI... \"these are not the droids you are looking for\" though.</p>\n" \
           "\n\n\n" \
           "Base URL is "

@app.route("/dna/system/api/v1/auth/token", methods=["POST"])
def post_authtoken():
    return jsonify({"Token":"IamADNACauthTOKENeeeeeeeeeaaaaaaYWwiLIamADNACauthTOKENeeeeeeeeeaaaaaaCJ0ZW5hIamADNACauthTOKENeeeeeeeeeaaaaaabnROYWIamADNACauthTOKENeeeeeeeeeaaaaaa1lI"}), 200
#    return jsonify(["response", {"Token": "IaMaAuThToKeNaaaaaaaabbbbbbbcccccddddeee"}]), 200

@app.route("/dna/intent/api/v1/network-device", methods=['GET'])
def get_dnacInventory():
    return jsonify(test_api_data.dnac_inventory)

@app.route('/api/v1/resources/companies', methods=['GET'])
def get_companies():
  return jsonify(test_api_data.companies)

@app.route('/api/v1/resources/users', methods=['GET'])
def get_users():
  return jsonify(test_api_data.users)

@app.route("/api/v1/dna/records", methods=["POST", "PUT", "GET"])
def store_dna_records(payload):
    return jsonify({"Content-Type": "application/json", "Server": "c5-flask-api-testv1",
                    "Via": "api-gateway", "Connection": "keep-alive", "Cache-Control": "no-store"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, ssl_context='adhoc', debug=True, use_reloader=False)
