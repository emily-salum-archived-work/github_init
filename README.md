# github_init
Project that communicates with github API, creating and uploading to a repository. 
It is quite simple, but it allowed me to simplify a few things I had to do in a few projects of mine.

## Development stage: Concluded / Open for extension. 

## Functionalities:

1. Creates repository with a given name
2. Adds files in specified paths 
3. Ignores specific files as instructed.
4. Within every path it visits, it will look for a 'behaviour.json' file, which specifies actions that need to be made in that folder. Specifically:
    1. "Replace": Replaces content in specific file to be something different inside github. 
    2. "Create": Creates file in github. 



## How to use:
- Install the package. 
- You now have direct access to the functionalities!

You can use them through the following files: 

### main.js
This file works with [Builder Helper]. Install it and make sure its within reach from importing.
Running main.js will get the latest project submitted to the loaders connection, using that information
to build the repository. 

### github_args.py
This file uses sys arguments to run the commands. This was made to connect to javascrypt code using 
[Python Shell](https://www.npmjs.com/package/python-shell).



## Associated Programs:
-Builder Helper, but only if you were to run main.py. 
