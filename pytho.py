#!/usr/bin/env python3

import pickle
import argparse
from paperqa import Docs
import os
import sys
import struct
import socket

def recv_msg(sock) -> str:
    length_binary = sock.recv(4)
    # Extract the 32-bit unsigned integer representing the length
    length = struct.unpack('>I', length_binary)[0]
    # Extract the UTF-8 binary data
    utf8_binary = sock.recv(length)
    return utf8_binary.decode('utf-8')

def encode_string_with_length(s: str) -> bytes:
    # Convert the string to UTF-8 binary
    utf8_binary = s.encode('utf-8')
    
    # Get the length of the encoded string
    length = len(utf8_binary)
    
    # Prepend a 32-bit unsigned integer representing the length
    length_binary = struct.pack('>I', length)
    
    # Return the combined binary data
    return length_binary + utf8_binary

def embed_docs(data_dir: str, name: str):
    files = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, file))]

    docs = Docs()
    for d in files:
        docs.add(d)

    return docs

def main(docs, port):
    conn = None
    if port != None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', port))
        sock.listen(1)
        conn, addr = sock.accept()
        with conn:
            while True:
                query = recv_msg(conn)
                answer = docs.query(query)
                #answer = 'hello\nworld\n'
                conn.sendall(encode_string_with_length(answer.formatted_answer))
    else:
        query = input("> ")
        answer = docs.query(query)
        print(answer.formatted_answer)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build embeddings and query them')

    parser.add_argument('command', nargs='?', default='default_command', help='Command (optional)')
    parser.add_argument('-n', '--name', required=True, help='Name of the embeddings database file')
    parser.add_argument('-d', '--data_dir', help='Path to the directory containing data to build an embedding')
    parser.add_argument('-p', '--port', type=int, help='Establish a socket connection on the port instead of stdin. Messages are length pre-fixed and utf8')

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
            main(docs, args.port)
    else:
        print(f"Unknown command '{args.command}' with model name '{args.name}'.")

    args = parser.parse_args()
