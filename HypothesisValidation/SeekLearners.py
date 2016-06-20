'''
Created on Aug 20, 2015

@author: Angus
'''

import os
import mysql.connector

def EdXMatching(path):
    # Mapping between email and global_user_id
    email_user_map = {}
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
        email_user_map[email] = global_user_id
        
        registered_email_set.add(email)  
    
    user_pii_fp.close()    
    # print "The number of enrolled learners is: " + str(len(email_user_map))
    return (email_user_map, registered_email_set)

def GitHubMatching(path, registered_email_set):
    # Mapping between GibHub login name and email
    login_email_map = {}
    
    # Processing previous before_fp101x data  
    files = os.listdir(path)
    
    for name in ["0.5y", "1.0y", "1.5y", "2.0y", "2.5y", "after-fp101"]:    
        for file in files:    
            if name in file:
                
                #print file
                
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
                        login_email_map[login] = email             

    # print "The number of github learners is: " + str(len(login_email_map))
    return login_email_map

def SeekCompleter():    
    print "To seek completed learners..."    
    completer_set = set()
    
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='MOOC')
    cursor = connection.cursor()
    
    sql_query = "SELECT DISTINCT(course_user.course_user_id) FROM course_user, global_user WHERE course_user.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND course_user.certificate_status=\"downloadable\""
    cursor.execute(sql_query)
    results = cursor.fetchall()
        
    for result in results:
        completer_set.add(result[0])
        
    print "The number of completers is: " + str(len(completer_set))
    
    return completer_set

def SeekNonCompleter():    
    print "To seek non-completed learners..."    
    nonCompleter_set = set()
    
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='MOOC')
    cursor = connection.cursor()
    
    sql_query = "SELECT DISTINCT(course_user.course_user_id) FROM course_user, global_user WHERE course_user.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND course_user.certificate_status!=\"downloadable\""
    cursor.execute(sql_query)
    results = cursor.fetchall()
        
    for result in results:
        nonCompleter_set.add(result[0])
    
    print "The number of nonCompleters is: " + str(len(nonCompleter_set))
    
    return nonCompleter_set

def SeekNoviceLearners(path):    
    print "To seek novice learners..."    
    email_user_map, registered_email_set = EdXMatching(path)
    login_email_map = GitHubMatching(path, registered_email_set)
    
    # Processing functional.expertise.onlyAfterFP101x data
    novice_path = path + "functional.expertise.onlyAfterFP101x"
    novice_fp = open(novice_path, "r")
    lines = novice_fp.readlines()

    novice_learner_set = set()
    
    for line in lines:
           
        line = str.lower(line)       
        line = line.replace("\n","")
        
        if login_email_map.has_key(line):            
            email = login_email_map[line]
            if email_user_map.has_key(email):                
                global_user_id = email_user_map[email]
                novice_learner_set.add(str("DelftX/FP101x/3T2014_" + global_user_id))
            
    novice_fp.close()                    

    print "The number of Novice learners is: " + str(len(novice_learner_set))
    
    return novice_learner_set

def SeekExpert(path):
    print "To seek expert learners..."
    email_user_map, registered_email_set = EdXMatching(path)
    login_email_map = GitHubMatching(path, registered_email_set)
    
    expert_set = set()
    
    # Processing beforeFP101x data
    beforeFP101x_path = path + "functional.expertise.beforeFP101x"
    beforeFP101x_fp = open(beforeFP101x_path, "r")
    lines = beforeFP101x_fp.readlines()
    
    cnt = 0
    
    for line in lines:
           
        line = str.lower(line)       
        line = line.replace("\n","")
        
        if login_email_map.has_key(line):            
            email = login_email_map[line]
            if email_user_map.has_key(email):
                global_user_id = email_user_map[email]
                expert_set.add(str("DelftX/FP101x/3T2014_" + global_user_id))
        else:
            cnt += 1                      

    print "The number of Expert learners is: " + str(len(expert_set))
    
    return expert_set

def SeekNonExpert(path):
    print "To seek nonExpert learners..."
    nonExpert_set = set()
    expert_set = SeekExpert(path)
    
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='MOOC')
    cursor = connection.cursor()
    
    sql_query = "SELECT global_user.course_user_id FROM global_user WHERE global_user.course_id=\"DelftX/FP101x/3T2014\""
    cursor.execute(sql_query)
    results = cursor.fetchall()
        
    for result in results:
        if result[0] not in expert_set:
            nonExpert_set.add(result[0])
    
    print "The number of nonExpert is: " + str(len(nonExpert_set))
        
    return nonExpert_set

def SeekTransferedExpertLearners(path):
    print "To seek transfered expert learners....."
    email_user_map, registered_email_set = EdXMatching(path)
    login_email_map = GitHubMatching(path, registered_email_set)
    
    transftered_expert_learner_set = set()
    
    # Processing expert.learner.fractionFuncProg data
    path = path + "expert.learner.fractionFuncProg"
    fp = open(path, "r")
    lines = fp.readlines()
    
    cnt = 0
    
    for line in lines:
           
        line = str.lower(line)       
        line = line.replace("\n","")
        
        array = line.split(" ")        
        login_name = array[0]
        
        if login_email_map.has_key(login_name):            
            email = login_email_map[login_name]
            if email_user_map.has_key(email):
                global_user_id = email_user_map[email]
                
                for i in range(len(array)-7, len(array)):
                # for i in range(1, len(array)-10):
                    if array[i] != "na" and array[i] != "0":
                        transftered_expert_learner_set.add(str("DelftX/FP101x/3T2014_" + global_user_id))
        else:
            cnt += 1                      

    print "The number of non-novice learners is: " + str(len(transftered_expert_learner_set))
    
    return transftered_expert_learner_set

def SeekTransferrer(path):
    print "To seek transferrers..."
    transferrer_set = set()
    
    novice_learner_set = SeekNoviceLearners(path)
    transftered_expert_learner_set = SeekTransferedExpertLearners(path)
    
    for learner in novice_learner_set:
        transferrer_set.add(learner)
    for learner in transftered_expert_learner_set:
        transferrer_set.add(learner)
        
    print "The number of transferrers is: " + str(len(transferrer_set))
    
    return transferrer_set

def SeekNonTransferrer(path):
    print "To seek nonTransferrer..."
    nonTransferrer_set = set()    
    transferrer_set = SeekTransferrer(path)
    
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='MOOC')
    cursor = connection.cursor()
    
    sql_query = "SELECT global_user.course_user_id FROM global_user WHERE global_user.course_id=\"DelftX/FP101x/3T2014\""
    cursor.execute(sql_query)
    results = cursor.fetchall()
        
    for result in results:
        if result[0] not in transferrer_set:
            nonTransferrer_set.add(result[0])
    
    print "The number of nonTransferrers is: " + str(len(nonTransferrer_set))
    
    return nonTransferrer_set

def SeekEngagedLearners(tags):    
    print "To seek engaged learners..."    
    engaged_learner_set = set()
    
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='MOOC')
    cursor = connection.cursor()
    
    if "observation" in tags:
        sql_query = "SELECT DISTINCT(observations.course_user_id) FROM observations, global_user WHERE observations.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\""
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        for result in results:
            engaged_learner_set.add(result[0])
            
    if "submission" in tags:
        sql_query = "SELECT DISTINCT(submissions.course_user_id) FROM submissions, global_user WHERE submissions.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\""
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        for result in results:
            engaged_learner_set.add(result[0])
            
    if "collaboration" in tags:
        sql_query = "SELECT DISTINCT(collaborations.course_user_id) FROM collaborations, global_user WHERE collaborations.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\""
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        for result in results:
            engaged_learner_set.add(result[0])
    
    print "The number of engaged learners is: " + str(len(engaged_learner_set))
    
    return engaged_learner_set

def SeekNonEngagedLearner(tags):
    print "To seek nonEngaged learners..."
    nonEngage_learner_set = set()
    
    engaged_learner_set = SeekEngagedLearners(tags)
    
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='MOOC')
    cursor = connection.cursor()
    
    sql_query = "SELECT global_user.course_user_id FROM global_user WHERE global_user.course_id=\"DelftX/FP101x/3T2014\""
    cursor.execute(sql_query)
    results = cursor.fetchall()
        
    for result in results:
        if result[0] not in engaged_learner_set:
            nonEngage_learner_set.add(result[0])
    
    print "The number of nonEngage learners is: " + str(len(nonEngage_learner_set))
    
    return nonEngage_learner_set
    

def SeekSurveyLearners(path):
    print "To seek survey learners..."   
    survey_learner_set = set()
    
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='MOOC')
    cursor = connection.cursor()

    sql_query = "SELECT survey_response.course_user_id FROM survey_response, global_user WHERE survey_response.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND survey_response.question_id=\"DelftX/FP101x/3T2014_pre_Q8.4\" AND survey_response.answer=\"1\""
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    for result in results:
        course_user_id = result[0]
        survey_learner_set.add(course_user_id)
        
    print "The number of survey learners is: " + str(len(survey_learner_set))
    return survey_learner_set

def SeekHighSelfEfficacyLearners():
    print "To seek high self-efficacy learners..."
    
    efficacy_learner_set = set() 
    
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
    
    
    for learner in high_learners:
        if learner not in low_learners:
            efficacy_learner_set.add(learner)    
        
    print "The number of high self-efficacy learners are: " + str(len(efficacy_learner_set))
    
    return efficacy_learner_set

course_path = "/Volumes/NETAC/EdX/Clear-out/FP101x/"
SeekTransferedExpertLearners(course_path)
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    
    
