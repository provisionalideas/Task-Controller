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

class colours:
    red = '\033[1;31m'
    clear = '\033[0m'
    blue = '\033[1;34m'

class clearscreen:
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

class JobTracker:
  codejob,tutorjob,hcjob,tempjob,restojob = 0,0,0,0,0
  TaskList = []
  ProjectList = []
  NumTasks = 0
  colours = colours()
  my_clear = clearscreen()

  saveLocation = ''
  open_time = 0

  cheers = ['Good job!','Keep going!',"You're doing well!","Keep it up!","Yaaaay!",
              'Hooray!',"You're almost there."]

  def init(self):
      self.saveLocation = os.path.expanduser("~") + "/WorkTracker"

      #TODO create list of databases in a file, read the file, and for item in list...
      #TODO add module to control lists from database

      #PRIME DIRECTORIES FOR USE
      if not os.path.exists(self.saveLocation):
          os.makedirs(self.saveLocation)
      self.saveLocation = self.saveLocation + "/TaskList.txt"
      self.dbLocation = os.path.expanduser("~") + "/WorkTracker/TrackerDB.txt"
      if not os.path.exists(self.saveLocation):
          storage = open(self.saveLocation,'w+')
          storage.write(str(time.time()) + "," + str(self.NumTasks) + "\n")
          storage.close()
      if not os.path.exists(self.dbLocation):
          storage = open(self.dbLocation,'w+')
          storage.close()

      #LOAD ALL ACTIVE ITEMS INTO ACTIVE STORAGE
      storage = open(self.saveLocation,'r+')
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

      toggle_read = 0
      for index, line in enumerate(storage):
          if (index == 0):
              line = line.rstrip()
              line = line.split(",")
              self.NumTasks = int(line[1])                                     #NumTasks tracks the number of tasks completed today
              line = datetime.datetime.fromtimestamp(float(line[0]))      #Sets previous time
              if (line < LowerBound): self.NumTasks = 0
          elif ("-*-*-*-*-*-*-*-*-*-*-*-*-" not in line) and (toggle_read == 1):
              line = line.rstrip()
              line = line.split(",")
              self.TaskList.append(line)
          elif ("-*-*-*-*-*-*-*-*-*-*-*-*-" in line):
              toggle_read += 1
          elif ("-*-*-*-*-*-*-*-*-*-*-*-*-" not in line) and (toggle_read == 2):
              self.ProjectList.append(line.rstrip())

      storage.close()

      self.open_time = time.time()

  #DEFINE MODULES
  def timer(self,start_time):
      total_time = time.time() - float(start_time)
      hours = int(total_time / 3600)
      minutes = int((total_time - (hours*3600)) / 60)
      seconds = int(total_time - (hours*3600) - (minutes*60))
      print ("--- %s hours, %s minutes, %s seconds ---" % (hours, minutes, seconds))
      #Fix timer so it registers and saves length of current task in progress
      #TODO create storage database for task length

  def savelist(self):
      storage = open(self.saveLocation,'w+')
      storage.truncate()
      storage.write(str(time.time()) + "," + str(self.NumTasks) + "\n")
      storage.write("-*-*-*-*-*-*-*-*-*-*-*-*-\n")
      for item in self.TaskList:
          for index,element in enumerate(item):
              storage.write(str(element))
              if index < (len(item) - 1): storage.write(",")
          # item = str(item).rstrip(")").lstrip("(")
          # storage.write(item)
          storage.write("\n")
      storage.write("-*-*-*-*-*-*-*-*-*-*-*-*-\n")
      for item in self.ProjectList:
          storage.write(item)
          storage.write("\n")
      storage.close()

  def printTodo(self,toggle):
      #os.system('cls' if os.name == 'nt' else 'clear')
      SubTaskList = []
      if toggle == 'tasks':
          print colours.red + "TASK LIST:" + colours.clear
          for a,b in enumerate(self.TaskList,1):
              print colours.red + '{} '.format(a) + colours.clear + '{}'.format(b[0])
      elif toggle == 'current_tasks':
          print colours.red + "CURRENT TASKS:" + colours.clear
          for a,b in enumerate(self.TaskList[0:5],1):
              print colours.red + '{} '.format(a) + colours.clear + '{}'.format(b[0])
      elif toggle == 'projects':
          print colours.blue + "ACTIVE PROJECTS:" + colours.clear
          for a,b in enumerate(self.ProjectList,1):
              print colours.blue + '{} '.format(a) + colours.clear + '{}'.format(b)
      else:
          for a,b in enumerate(self.TaskList,1):
              if toggle in b[0]:
                  SubTaskList.append(b)
          if len(SubTaskList) > 0:
              print colours.red + "TASK LIST:" + colours.clear
              for a,b in enumerate(SubTaskList,1):
                  print colours.red + '{} '.format(a) + colours.clear + '{}'.format(b[0])
          else:
              self.printTodo('current_tasks')


  def run(self):
      atexit.register(self.timer,start_time = self.open_time)
      atexit.register(self.savelist)

      prompt = ''

      while (prompt != 'EXIT') and (prompt != 'exit'):

      #TODO Fix to be case-insensitive

          options = []
          counter = 0
          prompt = raw_input('Enter your command. ')
          self.my_clear.clear() #os.system('cls' if os.name == 'nt' else 'clear')

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
                      self.ProjectList.insert(0,prompt[5:])
                  else:
                      self.ProjectList.insert(0,prompt[12:])
                  self.printTodo('projects')

              elif 'task' in prompt[4:9] or (prompt[3] == 't'):
                  ref = 5 if (prompt[3] == 't') else 9

                  self.TaskList.insert(0,[ \
                  #NAME, INPUT DATE, INPUT TIME
                  prompt[ref :],  datetime.date.today(),  time.time(), \
                  #START DATE, START TIME, COMPLETION DATE, COMPLETION TIME
                  "n/a",  "n/a",  "n/a",  "n/a", \
                  #TODO PROJECT,TYPE,PRIORITY,STATUS
                  "none",  "none",  0,  "queued"])

                  self.printTodo('tasks')

              #TODO convert this into a definition module and fix the else
              else:
                  storage = prompt[4:]
                  prompt = raw_input("Task or project? ")
                  if prompt == 'task':
                      self.TaskList.insert(0,storage)
                      self.printTodo('tasks')
                  elif prompt == 'project':
                      self.ProjectList.insert(0,storage)
                      self.printTodo('projects')

              self.savelist()

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

                  for index,item in enumerate(self.TaskList):
                      if prompt[ref :] in item[0]:
                          options.append(index)
                  if len(options) == 1:
                      index = options[0]
                      if self.TaskList[index][4] != "n/a": self.timer(self.TaskList[index][4])
                      self.TaskList[index][5] = datetime.date.today() #completion date
                      self.TaskList[index][6] = time.time() #completion time
                      if (ref != 7):
                          self.TaskList[index][10] = "completed"
                          self.NumTasks += 1
                      else:
                          self.TaskList[index][10] = "cancelled"

              # for index,element in enumerate(item):
              #     storage.write(str(element))
              #     if index < (len(item) - 1): storage.write(",")
              # # item = str(item).rstrip(")").lstrip("(")
              # # storage.write(item)
              # storage.write("\n")

                      storage = open(self.dbLocation,'a+')
                      for element in range(0,len(self.TaskList[index])):
                          storage.write(str(self.TaskList[index][element]))
                          if element < (len(self.TaskList[index]) - 1): storage.write(",")
                      storage.write("\n")
                      random.seed()
                      #os.system('say "%(a)s %(b)s. %(c)s"' % {"a":TaskList[index][0],"b":TaskList[index][10], \
                      #"c":self.cheers[random.randint(0,6)]})
                      if (self.NumTasks == 1): print("You've completed %(a)s task so far." % {"a":self.NumTasks})
                      if (self.NumTasks > 1): print("You've completed %(a)s tasks so far." % {"a":self.NumTasks})
                      self.TaskList.remove(self.TaskList[index])

              self.savelist()

      # or (prompt[(len(prompt)-9):] == 'completed')

      #TODO UPDATE COMPLETED SYSTEM SO IT CAN BE REVERSIBLE

              #TODO add task removal component
              #TODO remove item from task or project LIST
              #TODO create removal for project list
              #TODO add in announcements like in Countdown Timer


          elif prompt[:4] == 'list':
              self.my_clear.clear() #os.system('cls' if os.name == 'nt' else 'clear')
              if len(prompt) > 4:
                  if prompt[5:12] == 'project':
                      self.printTodo('projects')
                  elif prompt[5:9] == 'task':
                      self.printTodo('tasks')
                  elif prompt[5:8] == 'all':
                      self.printTodo('projects')
                      self.printTodo('tasks')
                  else:
                      self.printTodo(prompt[5:])
              else:
                  #self.printTodo('projects')
                  self.printTodo('current_tasks')


          elif prompt[:10] == 'prioritize':
              self.printTodo('tasks')
              prompt = raw_input("set new order. ")
              prompt = prompt.split(",")
              prompt = map(int,prompt)
              if len(prompt) < len(self.TaskList):
                  for i in range(0,len(self.TaskList)):
                      if (i+1) not in prompt:
                          prompt.append(i+1)
              for i,j in enumerate(prompt):
                  prompt[i] = prompt[i] - 1
              self.TaskList = [ self.TaskList[i] for i in prompt]
              self.printTodo('tasks')

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
              for index,item in enumerate(self.TaskList):
                  if prompt[ref :] in item[0]:
                      options.append(index)
              if len(options) == 1:
                  index = options[0]
                  self.TaskList[index][3]  = datetime.date.today() #start date
                  self.TaskList[index][4]  = time.time() #start time
                  self.TaskList[index][10] = "initiated"
                  print "Starting task \"%(x)s\" at %(y)s" % {"x":self.TaskList[index][0],"y":datetime.datetime.now().strftime("%I:%M:%S %p, %A, %b %d, %Y")}
              #
              # if len(prompt) > 5:
              #     for item in self.TaskList:
              #         if prompt[6:] in item:
              #             options.append(item)
              #             if len(options) > 1:
              #                 for a,b in enumerate(self.ProjectList,1):
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
              #     self.printTodo('tasks')
              #     prompt = raw_input("Which task do you want to start? ")

                  #TODO enable search by index
                  #TODO start by

          #TODO accord tasks to projects
          #TODO task list prioritization engine
          #TODO online syncing of projects and tasks across machine via login

          #TODO add responsive follow-throughs -- i.e. add command after proj --> add proj.

          elif prompt[:5] == 'clear':
              self.TaskList = []
              self.ProjectList = []
              storage = open(self.saveLocation,'w+')
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
                  for i in range(0,self.codejob):
                      print "|||||",
                  for i in range(0,(5-self.codejob)):
                      print "     ",
                  print "]",self.codejob

                  print 'TUTORING:    [',
                  for i in range(0,self.tutorjob):
                      print "||",
                  for i in range(0,(10-self.tutorjob)):
                      print "  ",
                  print "]",self.tutorjob

                  print 'HEALTHCARE:  [',
                  for i in range(0,self.hcjob):
                      print "|||||",
                  for i in range(0,(5-self.hcjob)):
                      print "     ",
                  print "]",self.hcjob

                  print 'TEMP:        [',
                  for i in range(0,self.tempjob):
                      print "|||||",
                  for i in range(0,(5-self.tempjob)):
                      print "     ",
                  print "]",self.tempjob

                  print 'RESTAURANTS: [',
                  for i in range(0,self.restojob):
                      print "|||||",
                  for i in range(0,(5-self.restojob)):
                      print "     ",
                  print "]",self.restojob

                  print "TOTAL:       [",
                  print '|' * (self.codejob+self.tutorjob+self.hcjob+self.tempjob+self.restojob),
                  print ' ' * (28-(self.codejob+self.tutorjob+self.hcjob+self.tempjob+self.restojob)),']',(self.codejob+self.tutorjob+self.hcjob+self.tempjob+self.restojob)

                  prompt = raw_input('Which have you filed? ')

                  if prompt == '1':
                      self.codejob += 1
                  elif prompt == '2':
                      self.tutorjob += 1
                  elif prompt == '3':
                      self.hcjob += 1
                  elif prompt == '4':
                      self.tempjob += 1
                  elif prompt == '5':
                      self.restojob += 1

                  #TODO set dynamic number of job types, autonomously set goals, etc. in goal setting component.

                  self.my_clear.clear() #os.system('clear')

                  if prompt in ['Apply to jobs.','1','2','3','4','5']:
                      random.seed()
                      print self.cheers[random.randint(0,6)]

  def main(self):
      self.init()
      self.run()

if __name__ == '__main__':
    JobTracker().main()
