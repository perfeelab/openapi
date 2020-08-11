import json

import requests
from flask import Blueprint, g, redirect, render_template, request, url_for, jsonify

bp = Blueprint(__name__, 'home')

perfee = "https://openapi-dev.perfee.com/v2"


def refresh_token():
    print("=============refresh token=================")
    data = {
        "client_id": "hsktest",
        "client_secret": "hsktest",
        "redirect_uri": "http://127.0.0.1:5000/perfee/authorize",
        "grant_type": "refresh_token",
        "refresh_token": g.refresh_token
    }
    resp = requests.post(
        perfee + "/oauth/token",
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


def perfee_post(path, data):
    headers = {
        "Authorization": "Bearer %s" % g.token,
        "Content-Type": "application/json"
    }
    url = perfee + path
    r = requests.post(url, headers=headers, data=json.dumps(data))
    if r.status_code == 401:
        token_data = refresh_token()
        g.token = token_data["access_token"]
        return perfee_post(path, data)
    elif 200 <= r.status_code < 300:
        return r.json()["data"]
    else:
        return r.json()


def perfee_get(path):
    headers = {
        "Authorization": "Bearer %s" % g.token
    }
    url = perfee + path
    r = requests.get(url, headers=headers)
    if r.status_code == 401:
        token_data = refresh_token()
        g.token = token_data["access_token"]
        return perfee_get(path)
    elif 200 <= r.status_code < 300:
        return r.json()["data"]
    else:
        return r.json()


def perfee_upload(path, files):
    url = url = perfee + path
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
        return perfee_upload(path, files)
    elif 200 <= r.status_code < 300:
        return r.json()["data"]
    else:
        return r.json()


def perfee_authorize_required(func):
    def wrapper(*args, **kwargs):
        try:
            f = open('token.json', 'r')
            token_data = json.loads(f.read())
            f.close()
            g.token = token_data["access_token"]
            g.refresh_token = token_data["refresh_token"]
            return func(*args, **kwargs)
        except FileNotFoundError:
            return redirect(url_for("website.routes.perfee-unauthorize"))
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


@bp.route('/perfee/unauthorize', endpoint="perfee-unauthorize")
def perfee_unauthorize():
    return render_template("unauthorize.html")


@bp.route('/perfee/authorize', endpoint="perfee-authorize")
def perfee_authorize():
    code = request.args.get('code')
    state = request.args.get('state')
    url = perfee + "/oauth/token"
    data = {
        "client_id": "hsktest",
        "client_secret": "hsktest",
        "redirect_uri": "http://127.0.0.1:5000/perfee/authorize",
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


@bp.route('/perfee/products', methods=['GET', 'POST'],
          endpoint="perfee-products")
@perfee_authorize_required
def perfee_products():
    if request.method == 'GET':
        regions = perfee_get("/regions")
        store_categories = perfee_get("/store-categories")
        categories = perfee_get("/categories?depth=3")
        specs = perfee_get("/specs")
        first_region_id = regions[0]["id"]
        warehouses = perfee_get("/warehouses?region_id=%s" % first_region_id)
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
        return jsonify(perfee_post("/products", data))


@bp.route('/perfee/warehouses',  methods=['GET'],
          endpoint="perfee-warehouses")
@perfee_authorize_required
def perfee_warehouses():
    if request.method == 'GET':
        region_id = request.args.get("region_id")
        warehouses = perfee_get("/warehouses?region_id=%s" % region_id)
        return jsonify(warehouses)


@bp.route('/perfee/spec-values',  methods=['GET'],
          endpoint="perfee-spec-values")
@perfee_authorize_required
def perfee_spec_values():
    if request.method == 'GET':
        spec_id = request.args.get("spec_id")
        spec_values = perfee_get("/spec-values?spec_id=%s" % spec_id)
        return jsonify(spec_values)


@bp.route('/perfee/upload-images',  methods=['POST'],
          endpoint="perfee-upload-images")
@perfee_authorize_required
def perfee_upload_images():
    files = request.files
    return jsonify(perfee_upload("/product-images", files))
