import argparse
from paperqa import Docs
import os

def main(data_dir):
    files = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, file))]

    docs = Docs()
    for d in files:
        docs.add(d)

    query = input("> ")
    answer = docs.query(query)
    print(answer.formatted_answer)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List files in a directory')
    parser.add_argument('-d', '--data_dir', default='./data', help='Path to the directory containing context data')
    args = parser.parse_args()

    main(args.data_dir)
