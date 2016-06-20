'''
Created on Jul 28, 2015

@author: Angus
'''

import os
from sets import Set

def InsertGitHubMark(path):
    
    email_user_map = {}
    
    # Processing user_pii.csv file
    user_pii_path = os.path.dirname(os.path.dirname(os.path.dirname(path))) + "/Results/FP101x/" + "user_pii.csv"
    user_pii_fp = open(user_pii_path,"r")
    for line in user_pii_fp:
        line = line.replace("\r\n", "")
        array = line.split(",")
        global_user_id = array[0]
        email = array[5]        
        email = str.lower(email)        
        email_user_map[email] = global_user_id        
    
    user_pii_fp.close()    
    print "The number of enrolled learners is: " + str(len(email_user_map))

    # Output github_mark sql file
    github_mark_path = os.path.dirname(os.path.dirname(os.path.dirname(path))) + "/Results/FP101x/" + "github_mark.sql"
    if os.path.isfile(github_mark_path):
        os.remove(github_mark_path)
        
    github_mark_file = open(github_mark_path, 'wb')
    github_mark_file.write("\r\n" + "USE FP101x;" + "\r\n")    
    github_mark_file.write("\r\n" + "ALTER TABLE global_user ADD github_mark BOOLEAN DEFAULT FALSE;" + "\r\n") 
    
    # Processing GitHub email file    
    email_set = Set()
    num_github_learners = 0   
    
    if not os.path.isdir(path):
        return False    
    files = os.listdir(path)
    
    num_ineffective_email = 0
    
    # Processing github_email data
    for file in files:      
        if "emails-github-and-fp101x" in file:      
                
            fp = open(path + file,"r")   
            for line in fp:
                
                line = line.replace("\r\n","")
                line = str.lower(line)
                
                if line not in email_set:                    
                    email_set.add(line)
                
                    if email_user_map.has_key(line):                    
                        num_github_learners += 1                
                        global_user_id = email_user_map[line]
                                    
                        write_string = "\r\n" + "UPDATE global_user SET github_mark = TRUE WHERE global_user_id ="
                        write_string += "'" + global_user_id + "';\r\n"
                        github_mark_file.write(write_string)
                    else:
                        num_ineffective_email += 1
                        

    github_mark_file.close()
    
    print "The number of emails contained in the GitHub email file is: " + str(len(email_set))
    print "The number of github learners is: " + str(num_github_learners)    
    print "The number of ineffective emails is: " + str(num_ineffective_email)
    
    

course_path = "/Volumes/NETAC/EdX/Clear-out/FP101x/"
InsertGitHubMark(course_path)
print "Finished."



