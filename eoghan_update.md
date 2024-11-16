## User Input
* NOTE: This is all meandering and not very useful but I will try to explain my changes while they still make sense to me

* Updated frontend & backend so that changes to the target temperature can be sent between the two
    * Changes are sent via a new JSON file, separate to the existing JSON file for updating room temperature readings/occupancy status
        * JSON files have been named/renamed `target_data.json` and `sensor_data.json`, respectively
    * Might be better practice to store all data to a single JSON file. This would necessitate that the file be initialized before anything else, however, and I'm not sure where/when to do that given that it can be accessed by both `basic_test.py` and `app.py`. Currently the JSON files are effectively reinitialized every time they are updated
    * Also, with a single JSON file system I worry that we might accidentally overwrite incoming data when trying to send out new data. This might be totally avoidable but I'd have to think about it, and the current system works so I'll leave it for now

* Added a few buttons to allow user to adjust target
    * These buttons look terrible and mess up the homepage...
        * ... but I might let someone with a little more Flask experience clean up the mess <3
    * Basically the data-transfer functionality is already there so it's just a matter of making it all look nice