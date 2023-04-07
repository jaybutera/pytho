socat TCP-LISTEN:1234,fork,reuseaddr EXEC:'python pytho.py -n test',pipes
