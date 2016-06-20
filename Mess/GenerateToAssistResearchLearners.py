'''
Created on Aug 23, 2015

@author: Angus
'''

import os
import mysql.connector
from HypothesisValidation.SeekLearners import SeekNoviceLearners

def GenerateToAssistResearchLearners(path):
    
    id_email_map = {}
    
    # Processing user_pii.csv file
    user_pii_path = os.path.dirname(os.path.dirname(os.path.dirname(path))) + "/Results/FP101x/" + "user_pii.csv"
    user_pii_fp = open(user_pii_path,"r")
    for line in user_pii_fp:
        line = line.replace("\n", "")
        array = line.split(",")
        global_user_id = array[0]
        email = array[5]        
        email = str.lower(email)        
        id_email_map[global_user_id] = email
    user_pii_fp.close()    
    print "The number of enrolled learners is: " + str(len(id_email_map))

    # Processing auth_user data   
    files = os.listdir(path)
    email_name_map = {}
    for file in files:               
        if "auth_user-" in file:
            fp = open(path + file, "r")
            fp.readline()
            lines = fp.readlines()
                        
            for line in lines:
                record = line.split("\t")
                email_name_map[str.lower(record[4])] = record[1]

    
    novice_learner_set = SeekNoviceLearners(path)
    
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='MOOC')
    cursor = connection.cursor()

    sql_query = "SELECT survey_response.course_user_id FROM survey_response, global_user WHERE survey_response.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND survey_response.question_id=\"DelftX/FP101x/3T2014_pre_Q8.4\" AND survey_response.answer=\"1\""
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    output_path = os.path.dirname(os.path.dirname(os.path.dirname(path))) + "/Results/FP101x/" + "To_assist_research_learner_list.txt" 
    output_file = open(output_path, 'wb')
    
    num_overlap = 0
    
    for result in results:
        course_user_id = result[0]
        global_user_id = course_user_id[course_user_id.find("_") + 1:len(course_user_id)]
        user_name = email_name_map[id_email_map[global_user_id]]
        output_file.write(user_name + "\n")
        
        if course_user_id in novice_learner_set:
            num_overlap += 1
        
    output_file.close()
    
    print "The number of overlap learners is: " + str(num_overlap)
    

####################################################
course_path = "/Volumes/NETAC/EdX/Clear-out/FP101x/"
GenerateToAssistResearchLearners(course_path)
print "Finished."
    
    
