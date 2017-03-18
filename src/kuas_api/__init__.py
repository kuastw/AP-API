# -*- coding: utf-8 -*-
"""
Created on 08/29/2015
@Author: Louie Lu
"""

from flask import Flask
from flask.ext.compress import Compress

__version__ = "2.0"

app = Flask(__name__)
app.config.from_object("config")

# Let secret key go in
import redis
red = redis.StrictRedis(db=2)
red.set("SECRET_KEY", str(app.config["SECRET_KEY"]))


# Compress please
compress = Compress()
compress.init_app(app)


from kuas_api.views.v2.doc import auto, doc
auto.init_app(app)


from kuas_api.views.v1 import api_v1
app.register_blueprint(api_v1)


# I'm lazy
from kuas_api.views.v2 import api_v2
app.register_blueprint(api_v2)


# Lazy about it
from kuas_api.views.latest import latest
app.register_blueprint(latest)

# register doc
app.register_blueprint(doc)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
