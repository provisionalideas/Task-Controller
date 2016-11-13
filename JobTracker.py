#!/usr/bin/env python

import os
import random
import time
import atexit
import datetime
import operator


#TODO SET SYSTEM THAT, ON OPENING/ON START OF NEW DAY, CHECKS FOR "ACTIVE"
#TASKS AND ZEROS THEM/FIGURE OUT WAY TO DETERMINE/DELINEATE WHEN ONE TASK
#STARTS AND ANOTHER ONE ENDS

codejob,tutorjob,hcjob,tempjob,restojob,toggle = 0,0,0,0,0,0
TaskList = []
ProjectList = []
NumTasks = 0

saveLocation = os.path.expanduser("~") + "/WorkTracker"

#TODO create list of databases in a file, read the file, and for item in list...
#TODO add module to control lists from database

#PRIME DIRECTORIES FOR USE
if not os.path.exists(saveLocation):
    os.makedirs(saveLocation)
saveLocation = saveLocation + "/TaskList.txt"
dbLocation = os.path.expanduser("~") + "/WorkTracker/TrackerDB.txt"
if not os.path.exists(saveLocation):
    storage = open(saveLocation,'w+')
    storage.write(str(time.time()) + "," + str(NumTasks) + "\n")
    storage.close()
if not os.path.exists(dbLocation):
    storage = open(dbLocation,'w+')
    storage.close()

#LOAD ALL ACTIVE ITEMS INTO ACTIVE STORAGE
storage = open(saveLocation,'r+')
CurrentTime = datetime.datetime.today()

#DETERMINE WHETHER NUMTASKS MAPS TO TODAY OR PREVIOUS DAY
if CurrentTime.hour >= 4:
    LowerBound = datetime.datetime(CurrentTime.year,CurrentTime.month, \
    CurrentTime.day,4,0,0,0)
    UpperBound = LowerBound + datetime.timedelta(days = 1)
else:
    UpperBound = datetime.datetime(CurrentTime.year,CurrentTime.month, \
    CurrentTime.day,4,0,0,0)
    LowerBound = UpperBound - datetime.timedelta(days = 1)

for index, line in enumerate(storage):
    if (index == 0):
        line = line.rstrip()
        line = line.split(",")
        NumTasks = int(line[1])                                     #NumTasks tracks the number of tasks completed today
        line = datetime.datetime.fromtimestamp(float(line[0]))      #Sets previous time
        if (line < LowerBound): NumTasks = 0
    elif ("-*-*-*-*-*-*-*-*-*-*-*-*-" not in line) and (toggle == 1):
        line = line.rstrip()
        line = line.split(",")
        TaskList.append(line)
    elif ("-*-*-*-*-*-*-*-*-*-*-*-*-" in line):
        toggle += 1
    elif ("-*-*-*-*-*-*-*-*-*-*-*-*-" not in line) and (toggle == 2):
        ProjectList.append(line.rstrip())

storage.close()

cheers = ['Good job!','Keep going!',"You're doing well!","Keep it up!","Yaaaay!",
            'Go James!',"You're almost there."]

hours,minutes,seconds = 0,0,0

open_time = time.time()

#DEFINE MODULES
def timer(start_time):
    total_time = time.time() - float(start_time)
    hours = int(total_time / 3600)
    minutes = int((total_time - (hours*3600)) / 60)
    seconds = int(total_time - (hours*3600) - (minutes*60))
    print ("--- %s hours, %s minutes, %s seconds ---" % (hours, minutes, seconds))
    #Fix timer so it registers and saves length of current task in progress
    #TODO create storage database for task length

def savelist():
    storage = open(saveLocation,'w+')
    storage.truncate()
    storage.write(str(time.time()) + "," + str(NumTasks) + "\n")
    storage.write("-*-*-*-*-*-*-*-*-*-*-*-*-\n")
    for item in TaskList:
        for index,element in enumerate(item):
            storage.write(str(element))
            if index < (len(item) - 1): storage.write(",")
        # item = str(item).rstrip(")").lstrip("(")
        # storage.write(item)
        storage.write("\n")
    storage.write("-*-*-*-*-*-*-*-*-*-*-*-*-\n")
    for item in ProjectList:
        storage.write(item)
        storage.write("\n")
    storage.close()

def printTodo(toggle):
    os.system('cls' if os.name == 'nt' else 'clear')
    SubTaskList = []
    if toggle == 'tasks':
        print "\033[1;31mTASK LIST:\033[0m"
        for a,b in enumerate(TaskList,1):
            print '\033[1;31m{} \033[0m{}'.format(a,b[0])
    elif toggle == 'current_tasks':
        print "\033[1;31mCURRENT TASKS:\033[0m"
        for a,b in enumerate(TaskList[1:6],1):
            print '\033[1;31m{} \033[0m{}'.format(a,b[0])
    elif toggle == 'projects':
        print "\033[1;34mACTIVE PROJECTS:\033[0m"
        for a,b in enumerate(ProjectList,1):
            print '\033[1;34m{} \033[0m{}'.format(a,b)
    else:
        for a,b in enumerate(TaskList,1):
            if toggle in b[0]:
                SubTaskList.append(b)
        if len(SubTaskList) > 0:
            print "\033[1;31mTASK LIST:\033[0m"
            for a,b in enumerate(SubTaskList,1):
                print '\033[1;31m{} \033[0m{}'.format(a,b[0])
        else:
            printTodo('current_tasks')


atexit.register(timer,start_time = open_time)
atexit.register(savelist)

prompt = ''

while (prompt != 'EXIT') and (prompt != 'exit'):

#TODO Fix to be case-insensitive

    options = []
    counter = 0
    prompt = raw_input('Enter your command. ')
    os.system('cls' if os.name == 'nt' else 'clear')

    if prompt == "help":
        print "Available commands:"
        print "- Apply to jobs."
        print "- list {projects/tasks}"
        print "- add {projects/tasks}"
        print "- start (task)"
        print "- completed (task)"

#NOTE DATABASE INDEX
# name (0)
# input date(1), input time(2)
# start date(3), start time(4)
# completion date(5), completion time(6)
# project(7), type(8), priority(9), status(10)

    elif prompt[:3] == 'add' or prompt[:3] == 'new':

        #TODO make alternative for "add new project"
        if 'project' in prompt[4:12] or (prompt[3] == 'p'):
            if prompt[3] =='p':
                ProjectList.insert(0,prompt[5:])
            else:
                ProjectList.insert(0,prompt[12:])
            printTodo('projects')

        elif 'task' in prompt[4:9] or (prompt[3] == 't'):
            ref = 5 if (prompt[3] == 't') else 9

            TaskList.insert(0,[ \
            #NAME, INPUT DATE, INPUT TIME
            prompt[ref :],  datetime.date.today(),  time.time(), \
            #START DATE, START TIME, COMPLETION DATE, COMPLETION TIME
            "n/a",  "n/a",  "n/a",  "n/a", \
            #TODO PROJECT,TYPE,PRIORITY,STATUS
            "none",  "none",  0,  "queued"])

            printTodo('tasks')

        #TODO convert this into a definition module and fix the else
        else:
            storage = prompt[4:]
            prompt = raw_input("Task or project? ")
            if prompt == 'task':
                TaskList.insert(0,storage)
                printTodo('tasks')
            elif prompt == 'project':
                ProjectList.insert(0,storage)
                printTodo('projects')

        savelist()

                #TODO what to do if someone puts something else in?
                #keyword wcould also be 'task', 'project', 'item', etc.
                #TODO Make everything case-insensitive
                #TODO naturally learn whether something is a task or a project

    #*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_#
    elif ('completed' in prompt) or ('finished' in prompt) or ('remove' in prompt):
    #(prompt[:9] == 'completed') or (prompt[:8] == 'finished') or (prompt[:6] == 'remove'):
        #ALSO MAKE THE REVERSE POSSIBLE
        #COMPLETED IS NOW THE PROTOTYPE FOR THE COMPLETION TYPE

#NOTE DATABASE INDEX
# name (0)
# input date(1), input time(2)
# start date(3), start time(4)
# completion date(5), completion time(6)
# project(7), type(8), priority(9), status(10)

        if (prompt[:9] == 'completed') or (prompt[:8] == 'finished') or (prompt[:6] == 'remove'):
            if (prompt[:9] == 'completed'): ref = 10
            if (prompt[:8] == 'finished' ): ref =  9
            if (prompt[:6] == 'remove'   ): ref =  7

            for index,item in enumerate(TaskList):
                if prompt[ref :] in item[0]:
                    options.append(index)
            if len(options) == 1:
                index = options[0]
                if TaskList[index][4] != "n/a": timer(TaskList[index][4])
                TaskList[index][5] = datetime.date.today() #completion date
                TaskList[index][6] = time.time() #completion time
                if (ref != 7):
                    TaskList[index][10] = "completed"
                    NumTasks += 1
                else:
                    TaskList[index][10] = "cancelled"

        # for index,element in enumerate(item):
        #     storage.write(str(element))
        #     if index < (len(item) - 1): storage.write(",")
        # # item = str(item).rstrip(")").lstrip("(")
        # # storage.write(item)
        # storage.write("\n")

                storage = open(dbLocation,'a+')
                for element in range(0,len(TaskList[index])):
                    storage.write(str(TaskList[index][element]))
                    if element < (len(TaskList[index]) - 1): storage.write(",")
                storage.write("\n")
                random.seed()
                #os.system('say "%(a)s %(b)s. %(c)s"' % {"a":TaskList[index][0],"b":TaskList[index][10], \
                #"c":cheers[random.randint(0,6)]})
                if (NumTasks == 1): print("You've completed %(a)s task so far." % {"a":NumTasks})
                if (NumTasks > 1): print("You've completed %(a)s tasks so far." % {"a":NumTasks})
                TaskList.remove(TaskList[index])

        savelist()

# or (prompt[(len(prompt)-9):] == 'completed')

#TODO UPDATE COMPLETED SYSTEM SO IT CAN BE REVERSIBLE

        #TODO add task removal component
        #TODO remove item from task or project LIST
        #TODO create removal for project list
        #TODO add in announcements like in Countdown Timer


    elif prompt[:4] == 'list':
        os.system('cls' if os.name == 'nt' else 'clear')
        if len(prompt) > 4:
            if prompt[5:12] == 'project':
                printTodo('projects')
            elif prompt[5:9] == 'task':
                printTodo('tasks')
            elif prompt[5:8] == 'all':
                printTodo('projects')
                printTodo('tasks')
            else:
                printTodo(prompt[5:])
        else:
            #printTodo('projects')
            printTodo('current_tasks')


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
        TaskList = [ TaskList[i] for i in prompt]
        printTodo('tasks')

    #TODO RECORD THAT TASK HAS BEEN MANUALLY REPRIORITIZED

    #tasks, todo, --> find first space, then compare item before space to dicitonary?
    #projects, active projects, current projects



#NOTE DATABASE INDEX
# name (0)
# input date(1), input time(2)
# start date(3), start time(4)
# completion date(5), completion time(6)
# project(7), type(8), priority(9), status(10)

#TODO fix for situations where you don't put in exactly the right one

    elif prompt[:5] == 'start' or prompt[:5] == 'begin':
        ref = 6
        for index,item in enumerate(TaskList):
            if prompt[ref :] in item[0]:
                options.append(index)
        if len(options) == 1:
            index = options[0]
            TaskList[index][3]  = datetime.date.today() #start date
            TaskList[index][4]  = time.time() #start time
            TaskList[index][10] = "initiated"
            print "Starting task \"%(x)s\" at %(y)s" % {"x":TaskList[index][0],"y":datetime.datetime.now().strftime("%I:%M:%S %p, %A, %b %d, %Y")}
        #
        # if len(prompt) > 5:
        #     for item in TaskList:
        #         if prompt[6:] in item:
        #             options.append(item)
        #             if len(options) > 1:
        #                 for a,b in enumerate(ProjectList,1):
        #                     print '{} {}'.format(a,b)
        #                 prompt = raw_input("Which task do you want to start? ")
        #                 counter = 0
        #                 for item in options:
        #                     if prompt in item:
        #                         counter = counter + 1
        #                 if counter != 1:
        #                     print "try again"
        #                     counter = 0
        #             else:
        #                 task_start = time.time()
        #                 task_id = options[0]
        #                 task_project = "none" #TODO CHANGE THIS TO CORERSPOND TO PROJECT
        #                 task_type = "n/a" #TODO CHANGE THIS TO CORRESPOND TO TYPE ONCE LEARNED
        #                 print "Starting task \"%(x)s\" at %(y)s" % {"x":task_id,"y":datetime.datetime.now().strftime("%I:%M:%S %p, %A, %b %d, %Y")}
        #                 #fix this so each task has a UID in the database
        # else:
        #     printTodo('tasks')
        #     prompt = raw_input("Which task do you want to start? ")

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
        print "List cleared."
    #TODO IMPROVE CLEAR SYSTEM SO YOU CAN SELECT CLEARING TASK LIST OR PROJECTS LIST OR BOTH
    #TODO SET CLEAR FUNCTION TO SET ALL TASKS IN DATABASE TO "CANCELLED"

        #TODO improve list storage system, change storage location
        #TODO add mechanism to remove completed items from list
        #TODO build task timer




















    #JOB APPLICATION MODULE --> prototype for project/task tracker
    elif prompt == "Apply to jobs.":
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
