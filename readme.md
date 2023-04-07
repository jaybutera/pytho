### What is it
A small wrapper of the [paperqa](https://github.com/whitead/paper-qa) python library into a cli tool. You can feed pytho a corpus of text data and ask questions from it.

### How To Use
You need an embeddings database which is built from a corpus of text to query.
First build an embedding by providing a path to your data and a name for the embedding.

```bash
# Assuming you have a bunch of text and pdf files in ./data
python pytho.py new -d ./data --name new_embedding
```

Once you have an embedding you can start a conversation with your data:
```bash
python pytho.py -n new_embedding
```

Embeddings are saved in `~/.paperqa/` in case you need to access them.

### To note
- Every query costs money (usually a few cents) so be mindful with your usage.
