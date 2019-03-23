# -*- coding: utf-8 -*-

import datetime
import json
import os
import requests

from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

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

    return app


app = create_app()
