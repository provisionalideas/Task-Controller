import os
import random
import time
import atexit
import datetime

codejob = 0
tutorjob = 0
hcjob = 0
tempjob = 0
restojob = 0
toggle = 0
options = []

saveLocation = os.path.expanduser("~") + "/WorkTracker"
#create list of databases in a file, read the file, and for item in list...
if not os.path.exists(saveLocation):
    os.makedirs(saveLocation)
saveLocation = saveLocation + "/TaskList.txt"
dbLocation = os.path.expanduser("~") + "/WorkTracker/TrackerDB.txt"
if not os.path.exists(saveLocation):
    storage = open(saveLocation,'w+')
    storage.close()
if not os.path.exists(dbLocation):
    storage = open(dbLocation,'w+')
    storage.close()


TaskList = []
TaskData = []
ProjectList = []

storage = open(saveLocation,'r+')
for line in storage:
    if ("-*-*-*-*-*-*-*-*-*-*-*-*-" not in line) and (toggle == 0):
        line = line.split("\t")
        TaskList.append(line[0])
        TaskData.append(line[1].rstrip())

    elif "-*-*-*-*-*-*-*-*-*-*-*-*-" in line:
        toggle = 1
    else:
        ProjectList.append(line.rstrip())
storage.close()

print TaskData

cheers = ['Good job!','Keep going!',"You're doing well!","Keep it up!","Yaaaay!",
            'Go James!',"You're almost there."]

hours = 0
minutes = 0
seconds = 0

open_time = time.time()

def timer(start_time):
    total_time = time.time() - start_time
    hours = int(total_time / 3600)
    minutes = int((total_time - (hours*3600)) / 60)
    seconds = int(total_time - (hours*3600) - (minutes*60))
    print ("--- %s hours, %s minutes, %s seconds ---" % (hours, minutes, seconds))
    #Fix timer so it registers and saves length of current task in progress
    #TODO create storage database for task length

def savelist():
    storage = open(saveLocation,'w+')
    storage.truncate()
    for index,item in enumerate(TaskList):
        print item,index
        #storage.write(item)
        print TaskData[index]
        storage.write("%(item)s\t%(data)s" % {"item":item,"data":TaskData[index]})
        #TODO: FIX SO THAT TASKDATA IS STORED IN AN ARRAY WHEN LOADED
        storage.write("\n")
    storage.write("-*-*-*-*-*-*-*-*-*-*-*-*-\n")
    for item in ProjectList:
        storage.write(item)
        storage.write("\n")
    storage.close()

def printTodo(toggle):
    if toggle == 'tasks':
        print "\033[1;31mTASK LIST:\033[0m"
        for a,b in enumerate(TaskList,1):
            print '\033[1;31m{} \033[0m{}'.format(a,b)
    elif toggle == 'projects':
        print "\033[1;34mACTIVE PROJECTS:\033[0m"
        for a,b in enumerate(ProjectList,1):
            print '\033[1;34m{} \033[0m{}'.format(a,b)

atexit.register(timer,start_time = open_time)
atexit.register(savelist)

prompt = ''

while (prompt != 'EXIT') and (prompt != 'exit'):

#TODO Fix to be case-insensitive
    options = []
    counter = 0
    prompt = raw_input('Enter your command. ')
    os.system('clear')

    if prompt == "help":
        print "Available commands:"
        print "- Apply to jobs."
        print "- list {projects/tasks}"
        print "- add {projects/tasks}"
        print "- start (task)"
        print "- completed (task)"

    if prompt == "Apply to jobs.":
        while prompt in ['Apply to jobs.','1','2','3','4','5']:

            print "~~JAMES' JOB APPLICATION TRACKER:~~"
            #TODO ADD GOAL SETTING MODULE
            print 'GOALS:'
            print '- 5 programming (1), 10 tutoring (2), 5 healthcare (3)'
            print '- 5 temp jobs (4), 5 restaurants (5)'

            # if "goal" in prompt:
            #TODO BUILD GOALSETTING MODULE

            # biggest = 0
            # for item in targetList:
            #     if len(item) > biggest:
            #         biggest = len(item)
            # print goal + ": " + (len(biggest) - len(goal))*' ' + "[",


            print 'PROGRAMMING: [',
            for i in range(0,codejob):
                print "|||||",
            for i in range(0,(5-codejob)):
                print "     ",
            print "]",codejob

            print 'TUTORING:    [',
            for i in range(0,tutorjob):
                print "||",
            for i in range(0,(10-tutorjob)):
                print "  ",
            print "]",tutorjob

            print 'HEALTHCARE:  [',
            for i in range(0,hcjob):
                print "|||||",
            for i in range(0,(5-hcjob)):
                print "     ",
            print "]",hcjob

            print 'TEMP:        [',
            for i in range(0,tempjob):
                print "|||||",
            for i in range(0,(5-tempjob)):
                print "     ",
            print "]",tempjob

            print 'RESTAURANTS: [',
            for i in range(0,restojob):
                print "|||||",
            for i in range(0,(5-restojob)):
                print "     ",
            print "]",restojob

            print "TOTAL:       [",
            print '|' * (codejob+tutorjob+hcjob+tempjob+restojob),
            print ' ' * (28-(codejob+tutorjob+hcjob+tempjob+restojob)),']',(codejob+tutorjob+hcjob+tempjob+restojob)

            prompt = raw_input('Which have you filed? ')

            if prompt == '1':
                codejob += 1
            elif prompt == '2':
                tutorjob += 1
            elif prompt == '3':
                hcjob += 1
            elif prompt == '4':
                tempjob += 1
            elif prompt == '5':
                restojob += 1

            #TODO set dynamic number of job types, autonomously set goals, etc. in goal setting component.

            os.system('clear')

            if prompt in ['Apply to jobs.','1','2','3','4','5']:
                random.seed()
                print cheers[random.randint(0,6)]

    elif prompt[:3] == 'add' or prompt[:3] == 'new':

        #TODO make alternative for "add new project"
        if 'project' in prompt[4:12] or (prompt[3] == 'p'):
            if prompt[3] =='p':
                ProjectList.insert(0,prompt[5:])
            else:
                ProjectList.insert(0,prompt[12:])
            printTodo('projects')

        elif 'task' in prompt[4:9] or (prompt[3] == 't'):
            if prompt[3] == 't':
                TaskList.insert(0,prompt[5:])
                TaskData.insert(0,(datetime.date.today(),time.strftime("%H:%M",time.localtime(time.time())),1,"automatic"))
                print TaskData
                #date, time, priority, manual/automatic
            else:
                TaskList.insert(0,prompt[9:])
            printTodo('tasks')

        else:
            storage = prompt[4:]
            prompt = raw_input("Task or project? ")
            if prompt == 'task':
                TaskList.insert(0,storage)
                printTodo('tasks')
            elif prompt == 'project':
                ProjectList.insert(0,storage)
                printTodo('projects')

                #TODO what to do if someone puts something else in?
                #keyword wcould also be 'task', 'project', 'item', etc.
                #TODO make a help command system

        #TODO Make everything case-insensitive

    #TODO naturally learn whether something is a task or a project

    elif ('completed' in prompt) or ('finished' in prompt) or ('remove' in prompt):
    #(prompt[:9] == 'completed') or (prompt[:8] == 'finished') or (prompt[:6] == 'remove'):
        #ALSO MAKE THE REVERSE POSSIBLE
        #COMPLETED IS NOW THE PROTOTYPE FOR THE COMPLETION TYPE
        if (prompt[:9] == 'completed') or (prompt[(len(prompt)-9):] == 'completed'):
            for item in TaskList:
                if prompt[10:] in item:
                    options.append(item)
            if len(options) == 1:
                if "task_id" in globals():
                    if (task_id == options[0]):
                        if "task_start" in globals():
                            timer(task_start)
                            storage = open(dbLocation,'a+')
                            storage.write("%(name)s,%(date)s,%(start_time)s,%(end_time)s,%(total_time)s,%(project)s,%(type)s" % \
                            {"name":task_id,"date":datetime.date.today(),"start_time":task_start,"end_time":time.time(), \
                            "total_time":time.time()-task_start,"project":task_project,"type":task_type})
                            storage.close()
                TaskList.remove(options[0])
                random.seed()
                os.system('say "%(a)s completed. %(b)s"' % {"a":options[0],"b":cheers[random.randint(0,6)]})

            #INSERT INDICATOR TO UPDATE TASK AS COMPLETED
        elif prompt[:8] == 'finished':
            for item in TaskList:
                if prompt[9:] in item:
                    options.append(item)
            if len(options) == 1:
                if (task_id == options[0]):
                    if "task_start" in globals():
                        timer(task_start)
                TaskList.remove(prompt[9:])
            #INSERT INDICATOR TO UPDATE TASKAS REMOVED

                    #OPTIONS....
            #GENERALIZE THIS PIECE AS DEFINED FUNCTION
        elif prompt[:6] == 'remove':
            for item in TaskList:
                if prompt[7:] in item:
                    options.append(item)
            if len(options) == 1:
                if (task_id == options[0]):
                    if "task_start" in globals():
                        timer(task_start)
                TaskList.remove(prompt[7:])
                #CHANGE STORAGE VALUE AS "TERMINATED"
            # else:
            #

        #TODO add task removal component
        #TODO remove item from task or project LIST
        #TODO create removal for project list
        #TODO add in announcements like in Countdown Timer

    elif prompt[:4] == 'list':
        if len(prompt) > 4:
            if prompt[5] == 'p':
                printTodo('projects')
            elif prompt[5] == 't':
                printTodo('tasks')
            else:
                printTodo('projects')
                printTodo('tasks')
        else:
            printTodo('projects')
            printTodo('tasks')

    elif prompt[:10] == 'prioritize':
        printTodo('tasks')
        prompt = raw_input("set new order. ")
        prompt = prompt.split(",")
        prompt = map(int,prompt)
        if len(prompt) < len(TaskList):
            for i in range(0,len(TaskList)):
                if (i+1) not in prompt:
                    prompt.append(i+1)
        for i,j in enumerate(prompt):
            prompt[i] = prompt[i] - 1
        print [ TaskList[i] for i in prompt]
        TaskList = [ TaskList[i] for i in prompt]
        printTodo('tasks')

    #tasks, todo, --> find first space, then compare item before space to dicitonary?
    #projects, active projects, current projects

    elif prompt[:5] == 'start':
        if len(prompt) > 5:
            for item in TaskList:
                if prompt[6:] in item:
                    options.append(item)
                    if len(options) > 1:
                        for a,b in enumerate(ProjectList,1):
                            print '{} {}'.format(a,b)
                        prompt = raw_input("Which task do you want to start? ")
                        counter = 0
                        for item in options:
                            if prompt in item:
                                counter = counter + 1
                        if counter != 1:
                            print "try again"
                            counter = 0
                    else:
                        task_start = time.time()
                        task_id = options[0]
                        task_project = "none" #TODO CHANGE THIS TO CORERSPOND TO PROJECT
                        task_type = "n/a" #TODO CHANGE THIS TO CORRESPOND TO TYPE ONCE LEARNED
                        print "Starting task \"%(x)s\" at %(y)s" % {"x":task_id,"y":datetime.datetime.now().strftime("%I:%M:%S %p, %A, %b %d, %Y")}
                        #fix this so each task has a UID in the database
        else:
            printTodo('tasks')
            prompt = raw_input("Which task do you want to start? ")

            #TODO enable search by index
            #TODO start by

    #TODO accord tasks to projects
    #TODO task list prioritization engine
    #TODO online syncing of projects and tasks across machine via login

    #TODO add responsive follow-throughs -- i.e. add command after proj --> add proj.

    elif prompt[:5] == 'clear':
        TaskList = []
        ProjectList = []
        storage = open(saveLocation,'w+')
        storage.truncate()
        storage.close()
    #TODO IMPROVE CLEAR SYSTEM SO YOU CAN SELECT CLEARING TASK LIST OR PROJECTS LIST OR BOTH

        #TODO improve list storage system, change storage location
        #TODO add mechanism to remove completed items from list
        #TODO build task timer
