import os
import random
import time
import atexit

codejob = 0
tutorjob = 0
hcjob = 0
tempjob = 0
restojob = 0

TaskList = []
storage = open('TaskList.txt','r')
for line in storage:
    TaskList.append(line)
storage.close()

cheers = ['Good job!','Keep going!',"You're doing well!","Keep it up!","Yaaaay!",
            'Go James!',"You're almost there."]

hours = 0
minutes = 0
seconds = 0

start_time = time.time()

def timer():
    total_time = time.time() - start_time
    hours = int(total_time / 3600)
    minutes = int((total_time - (hours*3600)) / 60)
    seconds = int(total_time - (hours*3600) - (minutes*60))
    print ("--- %s hours, %s minutes, %s seconds ---" % (hours, minutes, seconds))

def savelist():
    storage = open('TaskList.txt','w+')
    storage.truncate()
    for item in TaskList:
        storage.write(item)
        storage.write("\n")
    storage.close()

atexit.register(timer)
atexit.register(savelist)

prompt = ''

while (prompt != 'EXIT') and (prompt != 'exit'):
#TODO Fix to be case-insensitive
    prompt = raw_input('Enter your command. ')
    os.system('clear')

    if prompt == "Apply to jobs.":
        while prompt in ['Apply to jobs.','1','2','3','4','5']:

            print "~~JAMES' JOB APPLICATION TRACKER:~~"
            #TODO ADD GOAL SETTING MODULE
            print 'GOALS:'
            print '- 5 programming (1), 10 tutoring (2), 5 healthcare (3)'
            print '- 5 temp jobs (4), 5 restaurants (5)'

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

    elif prompt[:3] == 'add':
        TaskList.insert(0,prompt[4:])
        print "TASK LIST:"
        for a,b in enumerate(TaskList,1):
            print '{} {}'.format(a,b)

    elif (prompt[:9] == 'completed') or (prompt[:8] == 'finished'):
        if prompt[:9] == 'completed':
            for item in TaskList:
                if prompt[10:] in item:
                    print item
        elif prompt[:8] == 'finished':
            for item in TaskList:
                if prompt[9:] in item:
                    print item


    elif prompt[:4] == 'list':
        print "TASK LIST:"
        for a,b in enumerate(TaskList,1):
            print '{} {}'.format(a,b)

    elif prompt[:5] == 'clear':
        TaskList = []
        storage = open('TaskList.txt','w+')
        storage.truncate()
        storage.close()

        #TODO improve list storage system, change storage location
        #TODO add mechanism to remove completed items from list
