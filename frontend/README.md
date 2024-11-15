**Todo:**
1. `<meta http-equiv="refresh" content="1">` shouldn't apply for setting page
2. `/homepage` pictures change according to detection
    - Occupation: User input in settings can enable or stop the change
    - HVAC movement
    - HVAC on and off
3. `/rooms` temperature change
4. `/settings` target temperature validate
    - field is required (I don't know why it doesn't work) 
        - (If I can't fix it, when we demonstrate it make sure every time we go to `/settings`, set the target temperature)
    - when it is economy mode, Target temperature can be set only in [19, 23]

**Done:**
1. `/homepage` shows default/economy mode
2. `/homepage` shows target temperature