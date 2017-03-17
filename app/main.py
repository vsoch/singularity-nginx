from flask import (
    Flask, 
    url_for,
    render_template, 
    request,
    jsonify
)

from singularity.cli import Singularity
from flask_restful import Resource, Api
from werkzeug import secure_filename
from utils import (
    get_containers,
    get_container_links,
    get_container_args,
    get_container_labels,
    run_container as runc
)

from random import choice
import webbrowser
import tempfile
import shutil
import random
import os


# SERVER CONFIGURATION ##############################################
class SinginxServer(Flask):

    def __init__(self, *args, **kwargs):
        super(SinginxServer, self).__init__(*args, **kwargs)

        # Set up temporary directory on start of application
        self.containers = get_containers()
        self.tmpdir = tempfile.mkdtemp()
        self.image = None # Holds image to run
        self.cli = Singularity()


# API VIEWS #########################################################

app = SinginxServer(__name__)
api = Api(app)

class apiContainers(Resource):
    '''apiContainers
    Main view for REST API to display all available containers
    '''
    def get(self):
        # Generate the url list for each container
        response = {}
        for cname,cpath in app.containers:
            response[cname] = url_for('.api_container',cname)
        return response


class apiContainerArgs(Resource):
    '''apiContainerArgs
    '''
    def get(self, name):
        if name in app.containers:
            image_path = app.containers[name]
            return get_container_args(image_path,cli=app.cli)
        else:
            return {'error':'Not Found'}

class apiContainerLabels(Resource):
    '''apiContainerLabels
    '''
    def get(self, name):
        if name in app.containers:
            image_path = app.containers[name]
            return get_container_labels(image_path,cli=app.cli)
        else:
            return {'error':'Not Found'}


class apiContainer(Resource):
    '''apiContainer
     display metadata and endpoints for a container
    '''
    def get(self, name):
        if name in app.containers:
            response = dict()
            image_path = app.containers[name]
            response['links'] = get_container_links(name) 
            response['args'] = get_container_args(image_path,cli=app.cli)
            response['labels'] = get_container_labels(image_path,cli=app.cli)
            response['name'] = name
            return response
        else:
            return {'error':'Not Found'}

    
api.add_resource(apiContainers,'/api/containers')
api.add_resource(apiContainer,'/api/container/<string:name>')
api.add_resource(apiContainerArgs,'/api/container/args/<string:name>')
api.add_resource(apiContainerLabels,'/api/container/labels/<string:name>')


# CONTAINER VIEWS ###################################################

@app.route('/')
def index():
    container_names = list(app.containers.keys())
    return render_template('index.html', containers=container_names)


@app.route('/containers/random')
def random():
    container = choice(list(app.containers.keys()))
    return get_container(container)


@app.route('/container/<container>')
def get_container(container):
    links = get_container_links(container) 
    args = get_container_args(app.containers[container],cli=app.cli)
    labels = get_container_labels(app.containers[container],cli=app.cli)
    return render_template('container.html', container=container,
                                             links=links,
                                             args=args,
                                             labels=labels)


@app.route('/container', methods=['GET','POST'])
def container():
    '''POST view to see a container from a form'''  
    if request.method == 'POST':
        container = request.form['container']
        return get_container(container)
    return index()


@app.route('/container/run/<container>')
def run_container(container):

    if container in app.containers:
        image_path = app.containers[container]
        all_args = get_container_args(image_path,cli=app.cli)
        str_args = all_args['str']
        bool_args = all_args['bool']
        int_args = all_args['int']
        float_args = all_args['float']

        contenders = list(request.args.keys())
        args = []
        for contender in contenders:
            value = request.args.get(contender)
            flag = "--%s" %(contender)
            if contender in bool_args:
                args.append(flag)
            elif contender in str_args:
                args = args + [flag,'"%s"' %value]
            elif contender in int_args:
                args = args + [flag,int(value)]
            elif contender in float_args:
                args = args + [flag,float(value)]
        result = runc(image_path,args=args,cli=app.cli)

        # Dictionary gets rendered as json
        if isinstance(result,dict):
            return jsonify(result)    

        # Otherwise text
        return result


    # Not a value container, return to index  
    return index()

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
