'''
Created on Aug 20, 2015

@author: Angus
'''

import mysql.connector
from HypothesisValidation.SeekLearners import SeekNoviceLearners, SeekEngagedLearners

def H2(path):
    
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
    
    extrinsic_learners = set()
    intrinsic_learners = set()
    
    ########################################
    # Process survey question data
    
    # Question 5
    sql_query = "SELECT survey_response.course_user_id, survey_response.answer FROM survey_response, global_user WHERE survey_response.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND survey_response.question_id=\"DelftX/FP101x/3T2014_pre_Q2.4_1\""
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    for result in results:
        course_user_id = result[0]
        answer = result[1]
        
        if answer in ["60","61"]:        
            intrinsic_learners.add(course_user_id)     
        
    print "The number of intrinsic & extrinsic learners are: " + str(len(intrinsic_learners)) + "\t" + str(len(extrinsic_learners))
    
    # Question 7
    sql_query = "SELECT survey_response.course_user_id, survey_response.answer FROM survey_response, global_user WHERE survey_response.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND survey_response.question_id=\"DelftX/FP101x/3T2014_pre_Q3.1\""
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    for result in results:
        course_user_id = result[0]
        answer = result[1]
        
        if answer in ["6"]:        
            intrinsic_learners.add(course_user_id)
        if answer in ["1", "2"]:            
            extrinsic_learners.add(course_user_id)      
        
    print "The number of intrinsic & extrinsic learners are: " + str(len(intrinsic_learners)) + "\t" + str(len(extrinsic_learners))
    
    # Question 11
    sql_query = "SELECT survey_response.course_user_id, survey_response.answer FROM survey_response, global_user WHERE survey_response.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND survey_response.question_id=\"DelftX/FP101x/3T2014_pre_Q3.5\""
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    for result in results:
        course_user_id = result[0]
        answer = result[1]
                
        if answer in ["5", "7", "8"]:
            intrinsic_learners.add(course_user_id)
            
    print "The number of intrinsic & extrinsic learners are: " + str(len(intrinsic_learners)) + "\t" + str(len(extrinsic_learners))
    
    # Question 5
    sql_query = "SELECT survey_response.course_user_id, survey_response.answer FROM survey_response, global_user WHERE survey_response.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND survey_response.question_id=\"DelftX/FP101x/3T2014_pre_Q2.4_2\""
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    for result in results:
        course_user_id = result[0]
        answer = result[1]
        
        if answer in ["60","61"]:        
            extrinsic_learners.add(course_user_id)     
        
    print "The number of intrinsic & extrinsic learners are: " + str(len(intrinsic_learners)) + "\t" + str(len(extrinsic_learners))
    
    # Question 8
    sql_query = "SELECT survey_response.course_user_id, survey_response.answer FROM survey_response, global_user WHERE survey_response.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND survey_response.question_id=\"DelftX/FP101x/3T2014_pre_Q3.2\""
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    for result in results:
        course_user_id = result[0]
        answer = result[1]
                
        if answer in ["4", "5"]:
            extrinsic_learners.add(course_user_id)
            
    print "The number of intrinsic & extrinsic learners are: " + str(len(intrinsic_learners)) + "\t" + str(len(extrinsic_learners))
    
    # Question 10
    sql_query = "SELECT survey_response.course_user_id, survey_response.answer FROM survey_response, global_user WHERE survey_response.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND survey_response.question_id=\"DelftX/FP101x/3T2014_pre_Q3.4\""
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    for result in results:
        course_user_id = result[0]
        answer = result[1]
                
        if answer in ["5"]:
            extrinsic_learners.add(course_user_id)
            
    print "The number of intrinsic & extrinsic learners are: " + str(len(intrinsic_learners)) + "\t" + str(len(extrinsic_learners))
    
    # Question 12
    sql_query = "SELECT survey_response.course_user_id, survey_response.answer FROM survey_response, global_user WHERE survey_response.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND survey_response.question_id=\"DelftX/FP101x/3T2014_pre_Q3.6_8\""
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    for result in results:
        course_user_id = result[0]
        answer = result[1]
                
        if answer in ["4","5"]:
            extrinsic_learners.add(course_user_id)
            
    print "The number of intrinsic & extrinsic learners are: " + str(len(intrinsic_learners)) + "\t" + str(len(extrinsic_learners))
    
    # Post-survey Question 6
    sql_query = "SELECT survey_response.course_user_id, survey_response.answer FROM survey_response, global_user WHERE survey_response.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND survey_response.question_id=\"DelftX/FP101x/3T2014_post_Q4.1_13\""
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    for result in results:
        course_user_id = result[0]
        answer = result[1]
                
        if answer in ["4","5"]:
            extrinsic_learners.add(course_user_id)
            
    print "The number of intrinsic & extrinsic learners are: " + str(len(intrinsic_learners)) + "\t" + str(len(extrinsic_learners))

    print "------------------------------------------------------"
    print "After filtering contradicted learners..."
    
    commonLearners = set()
    for learner in extrinsic_learners:
        if learner in intrinsic_learners:
            commonLearners.add(learner)
    
    for learner in commonLearners:
        extrinsic_learners.remove(learner)
        intrinsic_learners.remove(learner)
        
    print "The number of intrinsic & extrinsic learners are: " + str(len(intrinsic_learners)) + "\t" + str(len(extrinsic_learners))
    
    print "------------------------------------------------------"
    num_intrinsic = 0
    num_extrinsic = 0
    num_unassigned = 0  
    
    for learner in novice_learner_set:
        if learner in intrinsic_learners:
            num_intrinsic += 1
        
        if learner in extrinsic_learners:
            num_extrinsic += 1
        
        if learner not in intrinsic_learners and learner not in extrinsic_learners:
            num_unassigned += 1
    
    print "The number of intrinsic NOVICE learners are: " + str(num_intrinsic)
    print "The number of extrinsic NOVICE learners are: " + str(num_extrinsic)
    print "The number of unassigned NOVICE learners are: " + str(num_unassigned) + "\n"
                
    
    
    









 
####################################################
course_path = "/Volumes/NETAC/EdX/Clear-out/FP101x/"
H2(course_path)
print "Finished."

















