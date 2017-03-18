''' utils.py

Utility functions for singularity-nginx

'''

import os
from logman import bot
from glob import glob
from singularity.cli import Singularity

def get_containers(install_dir=None):
    '''get_containers will return a dictionary of installed containers, with the
    actual path as the value, and keys the names (to provide to the user). These
    are stored at startup of the server.
    :param install_dir: the "install directory" of containers, meaning ../data
    '''
    if install_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        install_dir = os.path.abspath(os.path.join(here,'..','data'))
    containers = dict()
    file_paths = glob("%s/*.img" %(install_dir))
    for container in file_paths:
        container_name = os.path.basename(container)
        containers[container_name] = container
    return containers


def get_container_links(name):
    '''retrieve the links relevant to the container to get various input arguments, etc.
    '''
    api_links = {'args':'/api/container/args/%s' %(name),
                 'selflink':'/api/container/%s' %(name),
                 'labels':'/api/container/labels/%s' %(name)}

    actions = {'view':'/container/%s' %(name),
               'run':'/container/run/%s' %(name)}
    response = {'api':api_links,
                'actions': actions }    
    return response


def get_container_args(image_path,cli=None):
    '''parse the arguments from the container
    :param image_path: the path to the image file
    :param cli: a client. Instantiated if not provided
    '''
    if cli is None:
        cli = Singularity()
    return cli.get_args(image_path)


def get_container_labels(image_path,cli=None):
    '''parse the arguments from the container
    :param image_path: the path to the image file
    :param cli: a client. Instantiated if not provided
    '''
    if cli is None:
        cli = Singularity()
    return cli.get_labels(image_path)


def run_container(image_path,args=None,cli=None):
    '''run the container with one or more args
    '''
    if cli is None:
        cli = Singularity()

    if args is not None and len(args) > 0:
        result = cli.run(image_path,args=args)
    else:
        result = cli.run(image_path)
    

def sanitize(value):
    '''sanitize is a simple function for sanitizing arguments. All arguments
    come in as strings, and we currently only will support single arguments 
    (without phrases) so all spaces and quotes, and special characters are removed.'''
    return re.sub('[^A-Za-z0-9.]+', '', value)


def check_install(software,command=None):
    '''check_install will attempt to run the command specified with some argument, 
    and return an error if not installed.
    :param software: the executable to check for
    :param command: the command argument to give to the software (default is --version)
    '''    
    if command == None:
        command = '--version'
    cmd = [software,version]
    version = run_command(cmd,error_message="Cannot find %s. Is it installed?" %software)
    if version != None:
        bot.logger.info("Found %s version %s",software.upper(),version)
        return True
    else:
        return False

def write_json(json_object,filename,mode="w",print_pretty=True):
    '''write_json will (optionally,pretty print) a json object to file
    :param json_object: the dict to print to json
    :param filename: the output file to write to
    :param pretty_print: if True, will use nicer formatting   
    '''
    with open(filename,mode) as filey:
        if print_pretty == True:
            filey.writelines(simplejson.dumps(json_object, indent=4, separators=(',', ': ')))
        else:
            filey.writelines(simplejson.dumps(json_object))
    filey.close()
    return filename
