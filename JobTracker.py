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

atexit.register(timer)

# def NewTask():


print 'JOB COUNTER:'
print 'GOALS:'
print '- 5 programming (1), 10 tutoring (2), 5 healthcare (3)'
print '- 5 temp jobs (4), 5 restaurants (5)'
print 'TOTAL:       [                               ] 0'
print 'PROGRAMMING: [                               ] 0'
print 'TUTORING:    [                               ] 0'
print 'HEALTHCARE:  [                               ] 0'
print 'TEMP:        [                               ] 0'
print 'RESTAURANTS: [                               ] 0'

prompt = ''

while (prompt != 'EXIT'):
    prompt = raw_input('Which have you filed? ')

    if prompt == '1':
        codejob += 1
        os.system('clear')
    elif prompt == '2':
        tutorjob += 1
        os.system('clear')
    elif prompt == '3':
        hcjob += 1
        os.system('clear')
    elif prompt == '4':
        tempjob += 1
        os.system('clear')
    elif prompt == '5':
        restojob += 1
        os.system('clear')
    elif prompt[:3] == 'add':
        TaskList.insert(0,prompt[4:])
        print TaskList

    print "~~JAMES' JOB APPLICATION TRACKER:~~"
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

    random.seed()
    print cheers[random.randint(0,6)]
