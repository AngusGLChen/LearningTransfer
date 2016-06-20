'''
Created on Aug 25, 2015

@author: Angus
'''

import os
import mysql.connector
from HypothesisValidation.SeekLearners import SeekNoviceLearners, SeekEngagedLearners

def GenerateEngagedNoviceLearners(path):
    
    novice_learner_set = SeekNoviceLearners(path)
    engaged_learner_set = SeekEngagedLearners(["observation", "submission"])
    
    rm_learners = set()
    
    for learner in novice_learner_set:
        if learner not in engaged_learner_set:
            rm_learners.add(learner)
    
    for learner in rm_learners:
        novice_learner_set.remove(learner)
        
    print "The number of engaged novice learners is: " + str(len(novice_learner_set)) 
    
    ##################################################################################
    # To search for the GitHub user name for the engaged novice learners
    
    # Mapping between email and global_user_id
    EdXID_email_map = {}
    registered_email_set = set()
    
    # Processing user_pii.csv file
    user_pii_path = os.path.dirname(os.path.dirname(os.path.dirname(path))) + "/Results/FP101x/" + "user_pii.csv"
    user_pii_fp = open(user_pii_path,"r")
    for line in user_pii_fp:
        line = line.replace("\n", "")
        array = line.split(",")
        global_user_id = array[0]
        email = array[5]        
        email = str.lower(email)        
        
        EdXID_email_map[global_user_id] = email
        
        registered_email_set.add(email)  
    
    user_pii_fp.close()    
    print "The number of enrolled learners is: " + str(len(EdXID_email_map)) + "\n"
    
    # Mapping between login name and email
    email_GitHubID_map = {}
    
    # Processing previous before_fp101x data  
    files = os.listdir(path)
    
    for name in ["0.5y", "1.0y", "1.5y", "2.0y", "2.5y", "after-fp101"]:    
        for file in files:    
            if name in file:
                
                print file
                
                fp = open(path + file,"r")
                fp.readline()
                lines = fp.readlines()
              
                for line in lines:
                
                    line = line.replace("\n","")
                
                    # To select experts
                    line = str.lower(line)
                    array = line.split(",")
                
                    email = array[0]
                    email = str.lower(email)
                    
                    login = array[1]
                    login = str.lower(login)
                    
                    if email in registered_email_set:
                        email_GitHubID_map[email] = login            

    print "The number of enrolled learners is: " + str(len(email_GitHubID_map)) + "\n"
    
    # To query the number of active weeks for engaged novice learners
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='MOOC')
    cursor = connection.cursor()
    
    observation_sql_query = "SELECT observations.course_user_id, resources.relevant_week FROM observations, global_user, resources WHERE observations.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND observations.resource_id=resources.resource_id"
    submission_sql_query = "SELECT submissions.course_user_id, resources.relevant_week FROM submissions, global_user, problems, resources WHERE submissions.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND submissions.problem_id=problems.problem_id AND problems.problem_id=resources.resource_id"
    
    learner_week_map = {}
    sql_array = [observation_sql_query, submission_sql_query]

    for sql_query in sql_array:    
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        for result in results:
            course_user_id = result[0]
            week = result[1]
            
            if learner_week_map.has_key(course_user_id):
                learner_week_map[course_user_id].add(week)
            else:
                learner_week_map[course_user_id] = set()
                learner_week_map[course_user_id].add(week)
    
    # To output the results    
    for learner in novice_learner_set:
        num_weeks = len(learner_week_map[learner])       
        learner = learner.replace("DelftX/FP101x/3T2014_","")
        email = EdXID_email_map[learner]
        GitHubID = email_GitHubID_map[email]
        
        print str(GitHubID) + "," + str(num_weeks)



####################################################
course_path = "/Volumes/NETAC/EdX/Clear-out/FP101x/"
GenerateEngagedNoviceLearners(course_path)
print "Finished."
