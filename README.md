# github_init
Project that communicates with github API, creating and uploading to a repository. 
It allowed me to simplify a few things I had to do in a few projects of mine.
Mainly written to work with my [Portfolio Builder](https://github.com/emilymarquessalum/portfolio-builder). 

  
## How to use:

- Install the package. 
- Add your github information to the info.json file
- You now have direct access to the functionalities!

You can use them already through the following files: 


- github_args.py

This file uses sys arguments to run the commands. This was made to connect to javascrypt code using [Python Shell](https://www.npmjs.com/package/python-shell).

- Otherwise, connect directly to 'github_behaviour.py' and use your own methods.

If you are interested in making some quick tests before starting, you can modify and use the file "release.py" 


## Examples
 
 
``` 

from togit import github_behaviour as gb

# We will use github_init function from github_behaviour
#  github_init(repository name, file paths to commit, ocnfigurations dict)


# Creates repository with a welcome.txt file
gb.github_init('my_lib', ["./welcome.txt"])

# Commits that same file, but now named "production_welcome.txt"
gb.github_init('my_lib', [ { "str": "./welcome.txt", "rename": "production_welcome.txt" } ] )

# Gets files in number_helpers, passes them to parent folder (`helpers`)   
gb.github_init('my_lib', [ { "str": "./helpers/number_helpers/", "options": {"extract": true } }  ] )


# configures a commit_message used when sending the files, ignores developerSettings.json, specifies the branch as you need it to be. 
gb.github_init('my_lib', [ { "str": "./welcome.txt", "rename": "production_welcome.txt" } ], 
                    {"commit_message": "giving-welcome", "ignore_files": ["developerSettings.json"], "branch": "main", "is_public": True})
 
              
# We can use "replace" to replace text. In this case, we replace "e" with "eee" and "i" for "a". But you can do actually useful stuff, I am sure!
gb.github_init('my_lib', [ { "str": "./welcome.txt", "rename": "production_welcome.txt", "options": { "replace": {
                                                                                                        "e" : "eee",
                                                                                                        "i" : "a"
                                                                                                        }  
                                                                                                }  } ] )
                                                                                                
                                                                                                
# Configure specific files, when they are inside a folder that is already being commited. "fileOptions"
gb.github_init('my_lib', [ { "str": "./", 
            "options": {"fileOptions": {"welcome.txt": {"replace": { "e" : "eee", "i" : "a" }  }  }  } ])             
                                                                                                     
                                                                                                
 
```



 

## Functionalities:
 A quick review of what github_init can do.
1. Creates repository with a given name and adds files in specified paths 
2. Ignores files as instructed.
3. Receives commit configuration to ignore files, specify branch, specify if the repository is public (only used in creation). 
4. Can extract files from a folder to its parent and can receive "replace" commands to modify particular contents of a file  


Although most of the configurations can be done by arguments, you can also tell the github_init to look for a "build_configurations.json" file in every folder it visits, to specify some behaviour to it
    1. "Replace": Replaces content in specific file to be something different inside github. 
    2. "Create": Creates file in github. 



### Why this matters to me:

- Github communication can be done through any program that connects to this. 

For Portfolio Builder for example (see below), it updates the portfolio repository with contents inside of a "dist" folder, extracting it. It also uses "replace" so relative importing can work differently from development to production.

- Offers specific commands and possibility for expansion. 



## Development stage:
Concluded / Open for extension. 


## Related:
 
- [portfolio_builder](https://github.com/emilymarquessalum/portfolio-builder).
