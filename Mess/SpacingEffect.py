'''
Created on Jul 29, 2015

@author: Angus
'''

import mysql.connector
import time,datetime

import matplotlib.pyplot as plt
import numpy as np

import os
from sets import Set

def ValidateSpacingEffect():
    
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='MOOC')
    cursor = connection.cursor()
    
    ################################################################################
    # To plot timeOnSite
    '''
    timeOnSite_plot_query = "SELECT sessions.course_user_id, SUM(sessions.duration)/3600 FROM sessions, (SELECT DISTINCT(assessments.course_user_id) FROM assessments, global_user WHERE assessments.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND assessments.grade != 0) AS T1 WHERE sessions.course_user_id=T1.course_user_id GROUP BY sessions.course_user_id"
    # timeOnSite_plot_query = "SELECT sessions.course_user_id, SUM(sessions.duration)/3600 FROM sessions, (SELECT course_user.course_user_id FROM course_user, global_user WHERE course_user.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND course_user.final_grade > 0) AS T1 WHERE sessions.course_user_id=T1.course_user_id GROUP BY sessions.course_user_id"
    cursor.execute(timeOnSite_plot_query)
    query_results = cursor.fetchall()    
    
    plot_x = []
    plot_y = []
    
    result_map = {}    
    
    for result in query_results:
        
        
        #if result[1] < 0.1:
        #    value = round(result[1], 2)
        #else:
        #    if result[1] < 1:
        #        value = round(result[1], 1)
        #    else:
        #        if result[1] < 2:
        #            value = round(result[1], 1)
        #        else:
        #           value = round(result[1], 0)
        
        
        if result[1] < 1:
            value = round(result[1], 1)
        else:
            value = round(result[1], 0)
        
        if result_map.has_key(value):
            result_map[value] += 1
        else:
            result_map[value] = 1
            
    sorted_result_map = sorted(result_map.items(), key=lambda d:d[0])        

    for result in  sorted_result_map:
        plot_x.append(result[0])
        plot_y.append(result[1])


         
    plt.plot(plot_x,plot_y)
    plt.xscale("log")
    plt.show()
    
    '''
    ################################################################################
    # To plot sessionCount
    '''
    sessionCount_plot_query = "SELECT T2.Num, COUNT(T2.course_user_id) FROM (SELECT sessions.course_user_id, COUNT(sessions.session_id) AS Num FROM sessions, (SELECT DISTINCT(assessments.course_user_id) FROM assessments, global_user WHERE assessments.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND assessments.grade != 0) AS T1 WHERE sessions.course_user_id=T1.course_user_id GROUP BY sessions.course_user_id) AS T2 GROUP BY T2.Num"
    # sessionCount_plot_query = "SELECT T2.Num, COUNT(T2.course_user_id) FROM (SELECT sessions.course_user_id, COUNT(sessions.session_id) AS Num FROM sessions, (SELECT course_user.course_user_id FROM course_user, global_user WHERE course_user.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND course_user.final_grade > 0)  AS T1 WHERE sessions.course_user_id=T1.course_user_id GROUP BY sessions.course_user_id) AS T2 GROUP BY T2.Num"
    
    cursor.execute(sessionCount_plot_query)
    query_results = cursor.fetchall()
    
    result_map = {}
    
    for result in query_results:

        if result[0] <= 10:
            value = result[0]
        else:
            if result[0] <= 100:
                value = result[0] / 10 * 10
            else:
                value = result[0] / 50 * 50
        
        # value = result[0]
        
        if result_map.has_key(value):
            result_map[value] = result_map[value] + result[1]
        else:
            result_map[value] = result[1]
    
    sorted_result_map = sorted(result_map.items(), key=lambda d:d[0]) 
    
    plot_x = []
    plot_y = []
    
    for result in sorted_result_map:
        plot_x.append(result[0])
        plot_y.append(result[1])
        
        # print str(result[0]) + "\t" + str(result[1])
        
    plt.plot(plot_x,plot_y)
    plt.xscale("log")
    plt.show()
    '''
    ################################################################################
    # To plot timeOnSite-completionRate effect
    '''
    learner_timeOnSite = {}
    learner_certification = {}
    
    # To query the amount of time learners spent on the whole course    
    timeOnSite_query = "SELECT sessions.course_user_id, SUM(sessions.duration)/3600 FROM sessions, (SELECT DISTINCT(assessments.course_user_id) FROM assessments, global_user WHERE assessments.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND assessments.grade != 0) AS T WHERE sessions.course_user_id=T.course_user_id GROUP BY sessions.course_user_id"
    
    cursor.execute(timeOnSite_query)
    query_results = cursor.fetchall()    
    
    for result in query_results:
        course_user_id = result[0]
        duration = result[1]
        
        learner_timeOnSite[course_user_id] = duration
    
    num_learners = len(learner_timeOnSite)
    
    # To gather the certification status of learners
    certification_query = "SELECT course_user.course_user_id, course_user.certificate_status FROM course_user, global_user WHERE course_user.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" "
    cursor.execute(certification_query)
    query_results = cursor.fetchall()    
    for result in query_results:
        course_user_id = result[0]
        certification_status = result[1]
        learner_certification[course_user_id] = certification_status    
     
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
            
    plot_x = []
    plot_y = []
            
    for i in range(len(timeOnSite_groups)):
        avg_time = computeAvgTimeOnSite(timeOnSite_groups[i], learner_timeOnSite)
        completionRate = computeCompletionRate(timeOnSite_groups[i], learner_certification)
        
        plot_x.append(avg_time)
        plot_y.append(completionRate)
    
    plt.plot(plot_x,plot_y, linestyle='--',marker='o')
    plt.xscale("log")
    plt.show()       
    '''
    ################################################################################
    # To plot spacing effect
    learner_certification = {}
    learner_timeOnSite = {}
    learner_session = {}    
    
    learner_group = {}
    for i in range(10):
        learner_group[i] = [] 
        for j in range(3):
            learner_group[i].append([])    
    
    # To gather the certification status of learners
    certification_query = "SELECT course_user.course_user_id, course_user.certificate_status FROM course_user, global_user WHERE course_user.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" "
    cursor.execute(certification_query)
    query_results = cursor.fetchall()    
    for result in query_results:
        course_user_id = result[0]
        certification_status = result[1]
        learner_certification[course_user_id] = certification_status
    
    # To query the amount of time learners spent on the whole course    
    # Paper version
    # timeOnSite_query = "SELECT sessions.course_user_id, sessions.duration/3600 FROM sessions, (SELECT DISTINCT(assessments.course_user_id) FROM assessments, global_user WHERE assessments.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND assessments.grade != 0) AS T WHERE sessions.course_user_id=T.course_user_id"
    # timeOnSite_query = "SELECT sessions.course_user_id, sessions.duration/3600 FROM sessions, (SELECT course_user.course_user_id FROM course_user, global_user WHERE course_user.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND course_user.final_grade != 0) AS T WHERE sessions.course_user_id=T.course_user_id"
    
    # Applying knowledge version
    timeOnSite_query = "SELECT sessions.course_user_id, sessions.duration/3600 FROM sessions, global_user WHERE sessions.course_user_id=global_user.course_user_id AND global_user.github_mark=TRUE AND global_user.course_id=\"DelftX/FP101x/3T2014\" "

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
    print "The number of learners is: " + str(num_learners)  
        
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
        
        #for element in sorted_learner_timeOnSite:
        #    print str(element[0]) + "\t" + str(element[1])
        
        # To group
        sub_step = len(timeOnSite_groups[i]) / 3 + 1
        for j in range(0, len(timeOnSite_groups[i])):
            index = j / sub_step            
            learner_group[i][index].append(timeOnSite_groups[i][j])
            
    ########################################
    path = "/Volumes/NETAC/EdX/Clear-out/FP101x/"
    transfer_learners = locateTransferLearners(path)      
    ########################################
            
    for i in range(0, len(learner_group[0])):
        
        plot_x = []
        plot_y = []
        
        for j in range(0, len(learner_group)):
            
            avg_timeOnSite = computeAvgTimeOnSite(learner_group[j][i], learner_timeOnSite)
            plot_x.append(avg_timeOnSite)
           
            # completionRate = computeCompletionRate(learner_group[j][i], learner_certification)
            # plot_y.append(completionRate)
            # print str(avg_timeOnSite) + "\t" + str(completionRate)
            
            applyRate = computeApplyRate(learner_group[j][i], transfer_learners)
            plot_y.append(applyRate)
            print str(avg_timeOnSite) + "\t" + str(applyRate)        
                   
        
        if i == 0:
            low = plt.plot(plot_x, plot_y, color='r', marker='o', label='Low')
        
        if i == 1:
            plt.plot(plot_x, plot_y, color='g', marker='o', label='Mid')
        
        if i == 2:     
            plt.plot(plot_x, plot_y, color='b', linestyle='--', marker='o', label='High')
            
    
    plt.legend(loc='upper left')   
    plt.xscale("log")
    plt.show()        
        
def computeAvgTimeOnSite(learners, learner_timeOnSite):
    avgTimeOnSite = 0    
    for learner in learners:        
        avgTimeOnSite += learner_timeOnSite[learner]
    
    avgTimeOnSite = float(avgTimeOnSite) / len(learners)  
    return avgTimeOnSite

def computeAvgSession(learners, learner_session):
    avgSession = 0
    for learner in learners:
        avgSession += learner_session[learner]
        
    avgSession = float(avgSession) / len(learners)
    return avgSession

def computeCompletionRate(learners, learner_certification):
    num_pass = 0
    for learner in learners:
        if learner_certification[learner] == "downloadable":
            num_pass += 1
    return float(num_pass) / len(learners)

def locateTransferLearners(path):
    
    email_user_map = {}
    
    # Processing user_pii.csv file
    user_pii_path = os.path.dirname(os.path.dirname(os.path.dirname(path))) + "/Results/FP101x/" + "user_pii.csv"
    user_pii_fp = open(user_pii_path,"r")
    for line in user_pii_fp:
        line = line.replace("\n", "")
        array = line.split(",")
        global_user_id = array[0]
        email = array[5]
        
        email = str.lower(email)
        
        email_user_map[email] = global_user_id        
    
    user_pii_fp.close()
    
    transfer_learners = set()
    if not os.path.isdir(path):
        return False    
    files = os.listdir(path)
    
    # Processing after_fp101 data    
    for file in files:       
       
        if "after-fp101.csv" in file:
            
            print file
                
            fp = open(path + file,"r")
            nameLine = fp.readline()
            names = nameLine.split(",")
            
            lines = fp.readlines()
              
            for line in lines:
                
                line = line.replace("\n","")
                
                # To select experts
                line = str.lower(line)
                array = line.split(",")
                
                email = array[0]
                    
                if email_user_map.has_key(email):
                    if array[18] != "0" or array[19] != "0" or array[23] != "0":
                        transfer_learners.add("DelftX/FP101x/3T2014_" + email_user_map[email])

        
    return transfer_learners

def computeApplyRate(learners, transfer_learners):
    num_apply = 0
    for learner in learners:
        if learner in transfer_learners:
            num_apply += 1
    return float(num_apply) / len(learners)
    
                        
                        
    

####################################################
ValidateSpacingEffect()
print "Finished."

