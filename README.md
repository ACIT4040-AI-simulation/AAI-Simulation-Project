# AAI-Simulation-Project
Project repository for code and documentation


To see what the SIR model looks like you can run EpidemicModel.py

The development team is working with the sir.py and ODESolver.py file

# DEPENDENCIES
Matplotlib
numpy
scipy

# RANDOM JSON API
https://next.json-generator.com/api/json/get/Nyak4bMHF, did also add a file if API does not work, some of the numbers are from VG

# HOW TO WORK WITH BRANCHES

Before you start you will have two branches available : Master and develop branch
To see what branches you have: 
```
COMMAND: "git branch -a" in terminal 
```
When you are going to start working on a new feature, you create a new branch inside the develop branch, without the "" in Name:
```
COMMAND: git checkout feature/"NAME_OF_FEATURE" develop
```
This command will create a branch inside the develop

When you are ready to push your work to the develop branch:
```
COMMAND: git add . 
COMMAND: git commit -m "Write a message here which explains what you did breifly"
COMMAND: git push
```
Then go to github.com and create a pull request and assign someone to review the code. The person reviewing will approve your code. If approved you can click merge on github.com. Then your work will be available in develop branch.

After merging (and fixing merge conflicts), you should delete your "old" branch, by first doing this if you still are in the new branch you created e.g. feature/task1 branch:
```
COMMAND: git checkout develop
COMMAND: git pull
COMMAND: git branch -a
COMMAND (this wil delete the old branch): git branch -d feature/task1
```

**LASTLY**: THE NEXT TIME YOU LOG IN TO YOUR COMPUTER, ALWAYS type this command to check if something new has been added in your branch:
```
COMMAND: git status
COMMAND (if status had changed): git pull
```
THEN start continuing your work in your branch

**WHEN EVERYTHING IS FINISHED**, we will merge the develop branch into master.

## Gitk - see changes made in the repository
From time to time it is useful to run this command:
```
COMMAND: gitk &
```
It will open a graphical user interface where you can browse the commit-history, see which files were changed in each commit, by which person, and the commit-messages.
