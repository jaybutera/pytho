#!/usr/bin/env python3

import pickle
import argparse
from paperqa import Docs
import os
import sys

def embed_docs(data_dir: str, name: str):
    files = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, file))]

    docs = Docs()
    for d in files:
        docs.add(d)

    return docs

def main(docs):
    while True:
        query = input("> ")
        answer = docs.query(query)
        print(answer.formatted_answer)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build embeddings and query them')

    parser.add_argument('command', nargs='?', default='default_command', help='Command (optional)')
    parser.add_argument('-n', '--name', required=True, help='Name of the embeddings database file')
    parser.add_argument('-d', '--data_dir', help='Path to the directory containing data to build an embedding')

    args = parser.parse_args()

    path = os.path.expanduser(f'~/.paperqa/{args.name}.pkl')
    if args.command == 'new':
        if args.data_dir == None:
            print('You need to specify a directory where your data to build the new embeddings is with -d')
            sys.exit(0)

        print('Building embedding from text corpus...')
        docs = embed_docs(args.data_dir, args.name)
        with open(f'{path}', 'wb') as f:
            pickle.dump(docs, f)
        print(f'Saved embedding at ~/.paperqa/{args.name}.pkl')

    elif args.command == 'default_command':
        if not os.path.exists(path):
            print(f'No embedding file exists at {path}')
            sys.exit(0)

        with open(f'{path}', 'rb') as f:
            docs = pickle.load(f)
            main(docs)
    else:
        print(f"Unknown command '{args.command}' with model name '{args.name}'.")

    args = parser.parse_args()
