import json

import requests
from flask import Blueprint, g, redirect, render_template, request, url_for, jsonify

bp = Blueprint(__name__, 'home')

otoku_world = "https://openapi-test.otoku-world.com/v2"


def refresh_token():
    print("=============refresh token=================")
    data = {
        "client_id": "hsktest",
        "client_secret": "hsktest",
        "redirect_uri": "http://127.0.0.1:5000/otoku_world/authorize",
        "grant_type": "refresh_token",
        "refresh_token": g.refresh_token
    }
    resp = requests.post(
        otoku_world + "/oauth/token",
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data))
    f = open('token.json', 'r')
    token_data = json.loads(f.read())
    f.close()
    token_data["access_token"] = resp.json()["access_token"]
    f = open('token.json', 'w')
    f.write(json.dumps(token_data))
    f.close()
    return token_data


def otoku_world_post(path, data):
    headers = {
        "Authorization": "Bearer %s" % g.token,
        "Content-Type": "application/json"
    }
    url = otoku_world + path
    r = requests.post(url, headers=headers, data=json.dumps(data))
    if r.status_code == 401:
        token_data = refresh_token()
        g.token = token_data["access_token"]
        return otoku_world_post(path, data)
    elif 200 <= r.status_code < 300:
        return r.json()["data"]
    else:
        return r.json()


def otoku_world_get(path):
    headers = {
        "Authorization": "Bearer %s" % g.token
    }
    url = otoku_world + path
    r = requests.get(url, headers=headers)
    if r.status_code == 401:
        token_data = refresh_token()
        g.token = token_data["access_token"]
        return otoku_world_get(path)
    elif 200 <= r.status_code < 300:
        return r.json()["data"]
    else:
        return r.json()


def otoku_world_upload(path, files):
    url = url = otoku_world + path
    headers = {
        "Authorization": "Bearer %s" % g.token,
    }
    _files = {
        'files': (
            files["files"].filename,
            files["files"],
            files["files"].content_type
        )
    }
    r = requests.post(url, files=_files, headers=headers)
    if r.status_code == 401:
        token_data = refresh_token()
        g.token = token_data["access_token"]
        return otoku_world_upload(path, files)
    elif 200 <= r.status_code < 300:
        return r.json()["data"]
    else:
        return r.json()


def otoku_world_authorize_required(func):
    def wrapper(*args, **kwargs):
        try:
            f = open('token.json', 'r')
            token_data = json.loads(f.read())
            f.close()
            g.token = token_data["access_token"]
            g.refresh_token = token_data["refresh_token"]
            return func(*args, **kwargs)
        except FileNotFoundError:
            return redirect(url_for("website.routes.otoku_world-unauthorize"))
    return wrapper


@bp.route('/', endpoint="index")
def home():
    try:
        f = open('token.json', 'r')
        f.close()
        authorized = True
    except FileNotFoundError:
        authorized = False
    return render_template("home.html", authorized=authorized)


@bp.route('/otoku_world/unauthorize', endpoint="otoku_world-unauthorize")
def otoku_world_unauthorize():
    return render_template("unauthorize.html")


@bp.route('/otoku_world/authorize', endpoint="otoku_world-authorize")
def otoku_world_authorize():
    code = request.args.get('code')
    state = request.args.get('state')
    url = otoku_world + "/oauth/token"
    data = {
        "client_id": "hsktest",
        "client_secret": "hsktest",
        "redirect_uri": "http://127.0.0.1:5000/otoku_world/authorize",
        "code": code,
        "state": state,
        "grant_type": "authorization_code"
    }
    resp = requests.post(url, headers={'Content-Type': 'application/json'},
                         data=json.dumps(data))
    f = open('token.json', 'w')
    f.write(json.dumps(resp.json()))
    f.close()
    return redirect("/")


@bp.route('/otoku_world/products', methods=['GET', 'POST'],
          endpoint="otoku_world-products")
@otoku_world_authorize_required
def otoku_world_products():
    if request.method == 'GET':
        regions = otoku_world_get("/regions")
        store_categories = otoku_world_get("/store-categories")
        categories = otoku_world_get("/categories?depth=3")
        specs = otoku_world_get("/specs")
        first_region_id = regions[0]["id"]
        warehouses = otoku_world_get("/warehouses?region_id=%s" % first_region_id)
        context = {
            "regions": regions,
            "store_categories": store_categories,
            "categories": categories,
            "specs": specs,
            "warehouses": warehouses
        }
        return render_template("create_products.html", **context)
    elif request.method == 'POST':
        data = request.get_json()
        print(data)
        return jsonify(otoku_world_post("/products", data))


@bp.route('/otoku_world/warehouses',  methods=['GET'],
          endpoint="otoku_world-warehouses")
@otoku_world_authorize_required
def otoku_world_warehouses():
    if request.method == 'GET':
        region_id = request.args.get("region_id")
        warehouses = otoku_world_get("/warehouses?region_id=%s" % region_id)
        return jsonify(warehouses)


@bp.route('/otoku_world/spec-values',  methods=['GET'],
          endpoint="otoku_world-spec-values")
@otoku_world_authorize_required
def otoku_world_spec_values():
    if request.method == 'GET':
        spec_id = request.args.get("spec_id")
        spec_values = otoku_world_get("/spec-values?spec_id=%s" % spec_id)
        return jsonify(spec_values)


@bp.route('/otoku_world/upload-images',  methods=['POST'],
          endpoint="otoku_world-upload-images")
@otoku_world_authorize_required
def otoku_world_upload_images():
    files = request.files
    return jsonify(otoku_world_upload("/product-images", files))
