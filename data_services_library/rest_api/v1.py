import data_services_library as dsl

from flask import Blueprint, Response, request, render_template, abort, jsonify

api = Blueprint('v1', __name__, template_folder='templates')


@api.route("/")
def index():
    html = """
                <!DOCTYPE html>
                  <html>
                    <body>
                      <h1>Data Service Library Web API</h1>
                        <ul> 
                          <li> <b>http://127.0.0.1:5000/v1/providers</b> : List of available providers</li>
                          <li> <b>http://127.0.0.1:5000/v1/providers/&ltid&gt</b> : list particular provider</li>
                          <li> <b>http://127.0.0.1:5000/v1/services</b> : List of available services (use ?group=True to group by provider)</li>
                          <li> <b>http://127.0.0.1:5000/v1/services?provider=&ltprovider_id&gt</b> : filter list of available services by provider</li>
                          <li> <b>http://127.0.0.1:5000/v1/services/&ltid&gt</b> : list particular service</li>
                          <li> <b>http://127.0.0.1:5000/v1/services/&ltid&gt/locations</b> : Get locations full bbox extent</li>
                          <li> <b>http://127.0.0.1:5000/v1/services/&ltid&gt/locations?bbox=&ltxmin,ymin,xmax,ymax&gt</b> : Get locations, specifying bbox extent</li>
                          <li> <b>http://127.0.0.1:5000/v1/filters</b> : List of available filters
                          <li> <b>http://127.0.0.1:5000/v1/filters/&ltid&gt</b> : List particular filter
                          <li> <b>http://127.0.0.1:5000/v1/filters?datatype=&lttype&gt</b> : List of available filters for data type
                    </body>
                  </html>
            """
    return html


@api.route("/datasets")
@api.route("/datasets/<uid>")
def datasets(uid=None):
    datatype = request.args.get('datatype')
    js = dsl.api.get_datasets(uid=uid, as_json=True)
    return Response(js, status=200, mimetype='application/json')


@api.route("/filters")
@api.route("/filters/<uid>")
def filters(uid=None):
    datatype = request.args.get('datatype')
    js = dsl.api.get_filters(uid=uid, as_json=True, datatype=datatype)
    return Response(js, status=200, mimetype='application/json')


@api.route("/services")
@api.route("/services/<uid>")
def services(uid=None):
    provider = request.args.get('provider')
    group = request.args.get('group')
    js = dsl.api.get_services(uid=uid, as_json=True, group=group, provider=provider)
    return Response(js, status=200, mimetype='application/json')


@api.route("/services/<uid>/locations")
def locations(uid):
    bbox = request.args.get('bbox')
    if bbox:
        bbox = [float(x) for x in bbox.split(',')]
    js = dsl.api.get_locations(uid, bbox=bbox)
    return Response(js, status=200, mimetype='application/json')


@api.route("/services/<uid>/download/options")
def download_options(uid):
    js = dsl.api.download(uid, options=True)

    return Response(js, status=200, mimetype='application/json')


@api.route("/services/<uid>/download")
def download_data(uid):
    js = dsl.api.download(uid, **request.args)

    return Response(js, status=200, mimetype='application/json')


@api.route("/providers")
@api.route("/providers/<id>")
def providers(id=None):
    js = dsl.api.get_providers(id=id, as_json=True)
    return Response(js, status=200, mimetype='application/json')


@api.route("/collections", methods=['GET', 'POST', 'DELETE'])
def collections():
  if request.method=='GET':
      return jsonify(dsl.api.list_collections())

  if request.method=='DELETE':
      name = request.form.get('id')
      return jsonify(dsl.api.delete_collection(name))

  if request.method=='POST':
      name = request.form.get('id')
      return jsonify(dsl.api.create_collection(name))


@api.route("/collections/<id>", methods=['GET', 'POST', 'DELETE'])
def collection(id):
  if request.method=='GET':
      return jsonify(dsl.api.retrieve_collection(id))

  if request.method=='DELETE':
      service = request.form.get('service')
      features = request.form.get('features').split(',')
      return jsonify(dsl.api.delete_from_collection(id, service, features))

  if request.method=='POST':
      service = request.form.get('service')
      features = request.form.get('features').split(',')
      features = dsl.api.get_locations(service, features=features, as_json=False)
      return jsonify(dsl.api.add_to_collection(id, service, features))

