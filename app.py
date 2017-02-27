#!/usr/bin/env python

# Bo Zhu, http://zhuzhu.org
# MIT License

import json
import string
from zipfile import is_zipfile, ZipFile
from flask import Flask, Response, request, abort

APP_ID = 'pcjapmajcpcdahldndhkhbnglkhpeaaj'
CRX_FILE_LOC = 'travianGuo.crx'

SERVER_PROTOCOL = 'https'
SERVER_ADDRESS = 'travian-extension-server.herokuapp.com'
SERVER_PORT = 8888

assert len(APP_ID) == 32
assert is_zipfile(CRX_FILE_LOC)
with ZipFile(CRX_FILE_LOC, 'r') as zf:
    assert 'manifest.json' in zf.namelist()
    with zf.open('manifest.json', 'r') as mf:
        json_content = json.loads(mf.read())
        assert 'version' in json_content
        APP_VERSION = json_content['version']

XML_FILE_CONTENT = string.Template("""<?xml version='1.0' encoding='UTF-8'?>
<gupdate xmlns='http://www.google.com/update2/response' protocol='2.0'>
  <app appid='${app_id}'>
    <updatecheck codebase='${protocol}://${address}/crx'
                 version='${version}' />
  </app>
</gupdate>
""").substitute(
    app_id=APP_ID,
    protocol=SERVER_PROTOCOL,
    address=SERVER_ADDRESS,
    version=APP_VERSION
)


app = Flask(__name__, static_folder='')


@app.route("/xml")
def xml():
    if 'x' in request.args and APP_ID in request.args['x']:
        return Response(
            XML_FILE_CONTENT,
            mimetype='text/xml'
        )
    else:
        abort(404)


@app.route("/crx")
def crx():
    return app.send_static_file(CRX_FILE_LOC)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=SERVER_PORT,
        debug=True  # remove this in production servers
    )
