Task Controller is a smart time management tool that learns, auto-prioritizes, and schedules key tasks according to how long they typically take you. It is currently in alpha testing, with local databasing on the user's computer and all prioritization and scheduling work currently done manually by the user.

Once initial bugs are resolved, code will be updated to allow users to create an account on a remote server and pull task lists from across computers and mobile devices. I also need to figure out an effective way of tracking task time without requiring the user to self-report start and completion times, as this introduces significant error which will interfere with predictions. Once that works, I can release initial prediction algorithms that learn task types, times, and priorities, and start to learn the user's optimal schedule (the fun stuff!). 

Key commands are as follows:
add/new task [task], OR addt [task]
add/new project [task], OR addp [task]
prioritize -> activates prompt which allows you to choose your top priorities by index number
list projects -> lists all projects
list [keyword] -> lists all tasks including that keyword (next iteration will change this so it lists all *related* tasks to the keyword)
list all -> lists all tasks and projects (only using list will spit out the top five tasks, though this may change in future versions)
completed/finished [task/unique keyword] -> removes task from list and marks it as completed in the database
remove [task/unique keyword] -> removes task from list and marks it as cancelled in the database
start/begin [task/unique keyword] -> begins timer on selected task, and marks it as initiated. Time taken between start and completion will be included in the database entry for that task, and used to predict future task time.
clear -> clears all projects and tasks
