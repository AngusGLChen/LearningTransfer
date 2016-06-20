'''
Created on Aug 22, 2015

@author: Angus
'''

import mysql.connector
from HypothesisValidation.SeekLearners import SeekNoviceLearners, SeekEngagedLearners

def H3(path):
    
    novice_learner_set = SeekNoviceLearners(path)
    active_learner_set = SeekEngagedLearners(["observation", "submission"])
    
    rm_learners = set()
    
    for learner in novice_learner_set:
        if learner not in active_learner_set:
            rm_learners.add(learner)
    
    for learner in rm_learners:
        novice_learner_set.remove(learner)    
    
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='MOOC')
    cursor = connection.cursor()
    
    high_learners = set()
    low_learners = set()
    
    ########################################
    # Process survey question data

    # Post-survey Question 22
    question_ids = ["Q7.3_10", "Q7.3_11", "Q7.3_12"]
    
    for id in question_ids:
        
        sql_query = "SELECT survey_response.course_user_id, survey_response.answer FROM survey_response, global_user WHERE survey_response.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND survey_response.question_id=\"DelftX/FP101x/3T2014_post_" + id + "\""
        cursor.execute(sql_query)
        results = cursor.fetchall()
    
        for result in results:
            course_user_id = result[0]
            answer = result[1]
        
            if answer in ["1","2"]:
                low_learners.add(course_user_id)
            
            if answer in ["4","5"]:
                high_learners.add(course_user_id)
            
        print "The number of low & high learners are: " + str(len(low_learners)) + "\t" + str(len(high_learners))

    print "------------------------------------------------------"
    print "After filtering contradicted learners..."
    
    commonLearners = set()
    for learner in high_learners:
        if learner in low_learners:
            commonLearners.add(learner)
    
    for learner in commonLearners:
        high_learners.remove(learner)
        low_learners.remove(learner)
        
    print "The number of low & high learners are: " + str(len(low_learners)) + "\t" + str(len(high_learners))
    
    print "------------------------------------------------------"
    num_low = 0
    num_high = 0
    num_unassigned = 0  
    
    for learner in novice_learner_set:
        if learner in low_learners:
            num_low += 1
        
        if learner in high_learners:
            num_high += 1
        
        if learner not in low_learners and learner not in high_learners:
            num_unassigned += 1
    
    print "The number of low NOVICE learners are: " + str(num_low)
    print "The number of high NOVICE learners are: " + str(num_high)
    print "The number of unassigned NOVICE learners are: " + str(num_unassigned) + "\n"
                
    
    
    









 
####################################################
course_path = "/Volumes/NETAC/EdX/Clear-out/FP101x/"
H3(course_path)
print "Finished."

