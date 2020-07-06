## test API server with Falcon and gUnicorn HTTP server

import falcon
import json


class CompaniesResource(object):
  companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]
  def on_get(self, req, resp):
    resp.body = json.dumps(self.companies)

api = falcon.API()
companies_endpoint = CompaniesResource()
api.add_route('/companies', companies_endpoint)
##
##
## A More Structured Falcon GET Request
##
##Like Flask, Falcon can be installed using pip. At the same time, you can install gunicorn, an HTTP server:
##pip install falcon gunicorn
##
##Unlike Flask, Falcon does not have a built-in server. Now open up a new text file and copy-paste these contents:
##
##import falcon, json
##
##class CompaniesResource(object):
##  companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]
##  def on_get(self, req, resp):
##    resp.body = json.dumps(self.companies)
##
##api = falcon.API()
##companies_endpoint = CompaniesResource()
##api.add_route('/companies', companies_endpoint)
##
##There’s a bit more to the boilerplate for Falcon. It uses a class for each resource and connects routes to instances of a resource. Due to the use of a class, it makes more sense to declare the hard-coded array of companies within the company resource class. The result is the same as our previous example, returning the JSON version of the company list.
##
##Save the code as
##and then run it using gunicorn: gunicorn falconapi:api. Follow the local URL provided, and tack on our endpoint, such as
##
##Your results should be identical to the previous example:
##
##[
##   {
##      "id":1,
##      "name":"Company One"
##   },
##   {
##      "id":2,
##      "name":"Company Two"
##   }
##]
