'''
Created on Aug 23, 2015

@author: Angus
'''

import mysql.connector
from HypothesisValidation.SeekLearners import SeekNoviceLearners, SeekEngagedLearners

import matplotlib.pyplot as plt
import numpy as np

def SessionsDistribution():
    
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='MOOC')
    cursor = connection.cursor()
    
    sql_query = "SELECT COUNT(*) FROM sessions, global_user WHERE sessions.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" GROUP BY sessions.course_user_id"
    
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    result_map = {}
    
    num_learners = len(results)
    num_low = 0
    num_high = 0
    
    for result in results:
        if result[0] in result_map.keys():
            result_map[result[0]] += 1
        else:
            result_map[result[0]] = 1
        
        if result[0] < 10:
            num_low += 1
        else:
            num_high += 1
    
    sorted_result_map = sorted(result_map.items(), key=lambda d:d[0])
    
    plot_x = []
    plot_y = []
    
    for result in sorted_result_map:
        plot_x.append(result[0])
        plot_y.append(result[1])
        
    print "Percentage of Low is: " + str(round(float(num_low)/num_learners, 4))
    print "Percentage of High is: " + str(round(float(num_high)/num_learners, 4)) + "\n"
    
    plt.plot(plot_x,plot_y, linestyle='--')
    plt.show()
        
def H6(path):
    
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='MOOC')
    cursor = connection.cursor()
    
    learner_timeOnSite = {}
    learner_session = {}
    
    learner_group = {}
    for i in range(10):
        learner_group[i] = [] 
        for j in range(2):
            learner_group[i].append([])
    
    # Applying knowledge version
    timeOnSite_query = "SELECT sessions.course_user_id, sessions.duration/3600 FROM sessions, global_user WHERE sessions.course_user_id=global_user.course_user_id AND global_user.github_mark=TRUE AND global_user.course_id=\"DelftX/FP101x/3T2014\""

    cursor.execute(timeOnSite_query)
    query_results = cursor.fetchall()    
    for result in query_results:
        course_user_id = result[0]        
        duration = result[1]
        
        if learner_timeOnSite.has_key(course_user_id):
            learner_timeOnSite[course_user_id] = learner_timeOnSite[course_user_id] + duration
        else:
            learner_timeOnSite[course_user_id] = duration
        
        if learner_session.has_key(course_user_id):
            learner_session[course_user_id] = learner_session[course_user_id] + 1
        else:
            learner_session[course_user_id] = 1
            
    num_learners = len(learner_timeOnSite)        
    print "The number of session learners is: " + str(num_learners) + "\t" 
        
    # To group learners according to their time spent on site
    sorted_learner_timeOnSite = sorted(learner_timeOnSite.items(), key=lambda d:d[1])
    
    timeOnSite_groups = {}
    step = num_learners / 10 + 1
   
    for i in range(0, num_learners):
        index = i / step        
        if timeOnSite_groups.has_key(index):
            timeOnSite_groups[index].append(sorted_learner_timeOnSite[i][0])            
        else:
            timeOnSite_groups[index] = [sorted_learner_timeOnSite[i][0]]
    
    # To group learners according to their session number
    for i in range(0, len(timeOnSite_groups)):
        
        # To sort
        timeOnSite_groups[i].sort()
        
        # To group
        sub_step = len(timeOnSite_groups[i]) / 2 + 1
        for j in range(0, len(timeOnSite_groups[i])):
            index = j / sub_step            
            learner_group[i][index].append(timeOnSite_groups[i][j])
            
    ############################################       
    novice_learner_set = SeekNoviceLearners(path)
    active_learner_set = SeekEngagedLearners(["observation", "submission"])
    
    rm_learners = set()
    
    for learner in novice_learner_set:
        if learner not in active_learner_set:
            rm_learners.add(learner)
    
    for learner in rm_learners:
        novice_learner_set.remove(learner)
    
    num_assigned = 0
    
    for i in range(len(learner_group)):
        num_low = 0
        num_high = 0
        avg_timeOnSite_low = 0
        avg_timeOnSite_high = 0
        for j in range(len(learner_group[i])):
            for learner in learner_group[i][j]:
                if learner in novice_learner_set:
                    if j == 0:
                        num_low += 1
                    if j == 1:
                        num_high += 1
                    
                    num_assigned += 1
                if j == 0:
                    avg_timeOnSite_low += learner_timeOnSite[learner]
                if j == 1:
                    avg_timeOnSite_high += learner_timeOnSite[learner]
            
            if j == 0:
                avg_timeOnSite_low /= len(learner_group[i][j])
            if j == 1:
                avg_timeOnSite_high /= len(learner_group[i][j])
                
        print " For\t" + str(i) + "\t:\t" + str(num_low) + "\t" + str(num_high) + "\t" + str(round(avg_timeOnSite_low, 3)) + "\t" + str(round(avg_timeOnSite_high,3))

    print "\nThe number of assigned NOVICE learners are: " + str(num_assigned) + "\n"
                
    
    
    









 
####################################################
course_path = "/Volumes/NETAC/EdX/Clear-out/FP101x/"
#SessionsDistribution()
H6(course_path)
print "Finished."