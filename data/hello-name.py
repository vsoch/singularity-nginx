#!/usr/bin/env python3

import argparse
import os
import json
import sys

def get_parser():

    parser = argparse.ArgumentParser(description="Hello, you!")

    parser.add_argument("--name", 
                        dest='name', 
                        help="The name to say hello to.", 
                        type=str,
                        default=None)

    parser.add_argument("--age", 
                        dest='age', 
                        help="The age of the user", 
                        type=int,
                        default=None)

    parser.add_argument("--weight", 
                        dest='weight', 
                        help="How much does the user weigh?", 
                        type=float,
                        default=None)

    parser.add_argument("--is_dino", 
                        dest='is_dino', 
                        help="Is the user a dinosaur?", 
                        default=False,
                        action='store_true')

    return parser



def main():
    parser = get_parser()
    
    try:
        args = parser.parse_args()
    except:
        sys.exit(0)

    response = dict()
    if args.name is not None:
        response['name'] = "hello %s!" %(args.name)
    if args.age is not None:
        response['age'] = args.age
    if args.weight is not None:
        response['weight'] = args.weight

    if len(response) > 0:
        if not args.is_dino :
            response['species'] = "You are not a dinosaur."
        else:
            response['species'] = "You are a dinosaur! :D"

    # If the user didn't provide anything, tell him or her how to use the image
    if len(response) == 0:
        response = {'message':"Ruhroh! You didn't give any input arguments!",
                    'shell': {"is_dino": "--is_dino", 
                              "age": "--age 10", 
                              "name": "--name Vanessa", 
                              "weight": "--weight 10000" },
                    'web':   {"base":"/container/run/hello-name.img?[ARG1]&[ARG2]",
                              "is_dino": "is_dino=yes", 
                              "age": "age=10",
                              "name": "name=Vanessa", 
                              "weight": "weight=10000" }}

    print(json.dumps(response))


if __name__ == '__main__':
    main()
