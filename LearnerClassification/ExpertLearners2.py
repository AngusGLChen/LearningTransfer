'''
Created on Aug 19, 2015

@author: Angus
'''

import os
from sets import Set
import mysql.connector

def InsertExpertMark(path):
    
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
    print "The number of enrolled learners is: " + str(len(email_user_map)) + "\n"
    
    # Mapping between login name and email
    login_email_map = {}
    
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
                        login_email_map[login] = email             

    print "The number of enrolled learners is: " + str(len(login_email_map)) + "\n"

    # Output github_expert_mark sql file
    expert_mark_path = os.path.dirname(os.path.dirname(os.path.dirname(path))) + "/Results/FP101x/" + "github_expert_mark.sql"
    if os.path.isfile(expert_mark_path):
        os.remove(expert_mark_path)
        
    expert_mark_file = open(expert_mark_path, 'wb')
    expert_mark_file.write("\r\n" + "USE FP101x;" + "\r\n")       
    expert_mark_file.write("\r\n" + "ALTER TABLE global_user ADD github_expert_mark BOOLEAN DEFAULT FALSE;" + "\r\n") 
    
    expert_learner_set = Set()
    
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
                
                global_user_id = email_user_map[login_email_map[line]]
            
                write_string = "\r\n" + "UPDATE global_user SET github_expert_mark = TRUE WHERE global_user_id ="
                write_string += "'" + global_user_id + "';\r\n"
                expert_mark_file.write(write_string)
                
                expert_learner_set.add(global_user_id)
        else:
            cnt += 1
            #print line          

    print "The number of Expert learners is: " + str(len(expert_learner_set)) + "\n"
    print "The number of unmatched learners is: " + str(cnt)

    expert_mark_file.close()
    
####################################################
    
course_path = "/Volumes/NETAC/EdX/Clear-out/FP101x/"
InsertExpertMark(course_path)
# ExpertTrendsAnalyzer(course_path)
print "Finished."
