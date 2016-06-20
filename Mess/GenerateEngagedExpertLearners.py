'''
Created on Aug 27, 2015

@author: Angus
'''

import os
from HypothesisValidation.SeekLearners import SeekExpert, SeekEngagedLearners

def GenerateEngagedExpertLearners(path):
    
    expert_learner_set = SeekExpert(path)
    engaged_learner_set = SeekEngagedLearners(["observation", "submission"])
    
    rm_learners = set()
    
    for learner in expert_learner_set:
        if learner not in engaged_learner_set:
            rm_learners.add(learner)
    
    for learner in rm_learners:
        expert_learner_set.remove(learner)
        
    print "The number of engaged expert learners is: " + str(len(expert_learner_set)) 
    
    ##################################################################################
    # To search for the GitHub user name for the engaged expert learners
    
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
    
    for learner in expert_learner_set:
        learner = learner.replace("DelftX/FP101x/3T2014_","")
        email = EdXID_email_map[learner]
        GitHubID = email_GitHubID_map[email]
        
        print GitHubID



####################################################
course_path = "/Volumes/NETAC/EdX/Clear-out/FP101x/"
GenerateEngagedExpertLearners(course_path)
print "Finished."