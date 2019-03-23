# -*- coding: utf-8 -*-

import datetime
import json
import os
import requests

from flask import Flask, render_template, request


def create_app():
    app = Flask(__name__)

    def find_store_by_postcode(postcode):
        url = f"http://api.postcodes.io/postcodes/{postcode}"
        response = requests.get(url)
        return response.json()

    @app.route("/")
    def stores_list():
        """Provides an alphabetical ordered list of stores with there longitude and
        latitude."""
        # read stores.json
        file_uri = os.path.join(os.path.dirname(__file__), 'stores.json')
        with open(file_uri, 'r', encoding='utf-8') as file:
            file_data=file.read().replace('\n', '')
            json_data=json.loads(file_data)
            postcodes = [store['postcode'] for store in json_data]
        # retrieve longitude and latitude from postcodes.io
            response = requests.post('http://api.postcodes.io/postcodes',
                              data={ 'postcodes': postcodes })
            response_json = response.json()
            for store in json_data:
                response_list = response_json['result']
                index = [i for i,_ in enumerate(response_list) if _['query'] == store['postcode']][0]
                if response_list[index]['result']:
                    store['longitude'] = response_list[index]['result']['longitude']
                    store['latitude'] = response_list[index]['result']['latitude']
        # sort into alphabetical order.
            sorted_data = sorted(json_data, key=lambda kv: kv['name'])
        # render via template
            return render_template('stores.html',
                                   stores=sorted_data,
                                   now=datetime.datetime.utcnow())

    @app.route("/find/")
    def find_stores():
        """Provides a of finding stores within a given radius of a postcode"""
        postcode = request.args.get('postcode', '')
        radius = request.args.get('radius', 20000)
        # retrieve longitude and latitude from postcodes.io
        response_json = find_store_by_postcode(postcode)
        stores = []
        if response_json['result']:
            # assuming only 1 entry
            longitude = response_json['result']['longitude']
            latitude = response_json['result']['latitude']
            data = { 'longitude': longitude, 'latitude': latitude, 'radius': radius }
            response = requests.get('http://api.postcodes.io/postcodes',
                                    params=data)
            response_json = response.json()
            file_uri = os.path.join(os.path.dirname(__file__), 'stores.json')
            unsorted_data = []
            with open(file_uri, 'r', encoding='utf-8') as file:
                file_data=file.read().replace('\n', '')
                json_data=json.loads(file_data)
                for entry in response_json['result']:
                    found_stores = [store for store in json_data if store['postcode'] == entry['postcode']]
                    for store in found_stores:
                        response_json = find_store_by_postcode(postcode)
                        if response_json['result']:
                            store['longitude'] = response_json['result']['longitude']
                            store['latitude'] = response_json['result']['latitude']
                        unsorted_data.append(store)
            stores = sorted(unsorted_data, key=lambda kv: kv['latitude'], reverse = True)
        return json.dumps(stores)

    return app


app = create_app()
