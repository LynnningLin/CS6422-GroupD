# Project: Smart Home Thermostat Controller

Temperature control: It would continuously monitor the room temperature and adjust it to the user's preference by turning the AC/heater on or off. 
In economy mode, it would first try to open windows or curtains to regulate the temperature before using energy.

Energy-saving feature: It could use a combination of millimeter wave sensors and Bluetooth detectors 
(inspired by this quick YouTube video: https://www.youtube.com/watch?v=snVQHsnG_V4—it’s only 7 minutes long, no pressure🤡!). 
The system would adjust the temperature when it detects activity, and if no one is home, it wouldn’t turn on the AC at all.

Integration with other smart devices: To take it a step further, it could integrate with other smart home systems, like lighting, to create more customized and futuristic modes for users.

## Features

## Installation
### Prerequisites
1. Ensure you have Node.js or Python installed (depending on your tech stack).
2. Clone the repository:
    `git clone https://github.com/LynnningLin/CS6422-GroupD.git`

### BE Setup
1. Navigate to the backend/ directory `cd backend`


### FE Setup
1. Navigate to the backend/ directory `cd frontend`

## Common Git Commands
1. Creating a New Branch
To create a new branch for your feature development:
`git checkout -b your-branch-name`

2. Checking Branches
To see all branches in your repository (both local and remote):
`git branch -a`

3. Switching Between Branches
`git checkout your-branch-name`

4. Fetching and Syncing with the Remote Repository
To fetch the latest changes from the remote repository without merging:
`git fetch origin`
To fetch and merge the changes from the remote branch:
`git pull origin branch-name`

5. Staging and Committing Changes and Pushing Changes to the Remote
Stage all your changes:
`git add .`
Commit the staged changes with a message:
`git commit -m "Your commit message"`
To merge changes from another branch (e.g., feature/branch-name) into your current branch:
`git push origin feature/branch-name`

