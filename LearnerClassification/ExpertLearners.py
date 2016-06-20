'''
Created on Jul 28, 2015

@author: Angus
'''

import os
from sets import Set

def InsertExpertMark(path):
    
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
    print "The number of enrolled learners is: " + str(len(email_user_map)) + "\n"

    # Output github_expert_mark sql file
    expert_mark_path = os.path.dirname(os.path.dirname(os.path.dirname(path))) + "/Results/FP101x/" + "github_expert_mark.sql"
    if os.path.isfile(expert_mark_path):
        os.remove(expert_mark_path)
        
    expert_mark_file = open(expert_mark_path, 'wb')
    expert_mark_file.write("\r\n" + "USE FP101x;" + "\r\n")       
    expert_mark_file.write("\r\n" + "ALTER TABLE global_user ADD github_expert_mark BOOLEAN DEFAULT FALSE;" + "\r\n") 
    
    github_email_set = Set()
    
    if not os.path.isdir(path):
        return False    
    files = os.listdir(path)
    
    # max = 0
    # min = 0
    
    expert_learner_set = Set()
    
    # Processing before_fp101 data   
    for year_name in ["0.5y", "1.0y", "1.5y", "2.0y", "2.5y"]:    
        for file in files:           
            if year_name in file:            
                                
                fp = open(path + file,"r")
                nameLine = fp.readline()
                names = nameLine.split(",")
                # print names[18] + "\t" + names[19] + "\t" + names[23]
            
                lines = fp.readlines()
              
                for line in lines:
                
                    line = line.replace("\n","")
                
                    # To select experts
                    line = str.lower(line)
                    array = line.split(",")
                
                    email = array[0]                    
                    
                    '''
                    if value > max:
                        max = value
                    
                    if min == 0 and value != 0:
                        min = value
                    
                    if min != 0 and value < min and value != 0:
                        min = value
                    '''
                    
                    if email_user_map.has_key(email):
                        github_email_set.add(email)
                    
                    if email_user_map.has_key(email) and (array[18] != "0" or array[19] != "0" or array[23] != "0"):
                        if email not in expert_learner_set:                            
                            expert_learner_set.add(email)                
                            global_user_id = email_user_map[email]
                                    
                            write_string = "\r\n" + "UPDATE global_user SET github_expert_mark = TRUE WHERE global_user_id ="
                            write_string += "'" + global_user_id + "';\r\n"
                            expert_mark_file.write(write_string)                

    print "The number of Expert learners is: " + str(len(expert_learner_set))
    print "The number of GitHub learners is: " + str(len(github_email_set)) + "\n"

    expert_mark_file.close()
    
    # print max
    # print min

def ExpertTrendsAnalyzer(path):
    
    email_user_map = {}
    
    # Processing user_pii.csv file
    user_pii_path = os.path.dirname(os.path.dirname(os.path.dirname(path))) + "/Results/FP101x/""user_pii.csv"
    user_pii_fp = open(user_pii_path,"r")
    for line in user_pii_fp:
        line = line.replace("\n", "")
        array = line.split(",")
        global_user_id = array[0]
        email = array[5]        
        email = str.lower(email)        
        email_user_map[email] = global_user_id        
    
    user_pii_fp.close()
    
    print "The number of enrolled learners is: " + str(len(email_user_map)) + "\n"

    # To analyze the data    
    if not os.path.isdir(path):
        return False    
    files = os.listdir(path)
    
    expert_learner_set = Set()
    non_expert_learner_set = Set()    
        
    before_ratio_map = {}
    
    all_Geo_email_set = set()
    effective_Geo_email_set = set()
    non_effective_Geo_email_set = set()   
    
    # Processing before_fp101 data
    for year_name in ["0.5y", "1.0y", "1.5y", "2.0y", "2.5y"]:
    
        for file in files:    
            if year_name in file:
                
                fp = open(path + file,"r")
                nameLine = fp.readline()
                names = nameLine.split(",")
                # print names[18] + "\t" + names[19] + "\t" + names[23]
            
                lines = fp.readlines()
              
                for line in lines:
                
                    line = line.replace("\n","")
                
                    # To select experts
                    line = str.lower(line)
                    array = line.split(",")
                
                    email = array[0]
                    email = str.lower(email)
                    
                    all_Geo_email_set.add(email)
                    
                    if email_user_map.has_key(email):
                        
                        effective_Geo_email_set.add(email)
                        
                        if array[18] != "0" or array[19] != "0" or array[23] != "0":
                            expert_learner_set.add(email)
                            
                            if email in non_expert_learner_set:
                                non_expert_learner_set.remove(email)
                            
                        else:
                            
                            if email not in expert_learner_set:                      
                                non_expert_learner_set.add(email)
                        
                        num_fp_lines = 0
                        num_non_fp_lines = 0
                        
                        for i in range(2,24):
                            if i in [18, 19, 23]:
                                num_fp_lines += float(array[i])
                            else:
                                num_non_fp_lines += float(array[i])
                            
                        if email in before_ratio_map:
                            before_ratio_map[email] = {"fp":before_ratio_map[email]["fp"] + num_fp_lines, "non_fp": before_ratio_map[email]["non_fp"] + num_fp_lines} 
                        else:
                            before_ratio_map[email] = {"fp":num_fp_lines, "non_fp":num_non_fp_lines}
                    
                    else:
                        if email not in non_effective_Geo_email_set:
                            # print email
                            non_effective_Geo_email_set.add(email)
                      
    print "The number of expert learners is: " + str(len(expert_learner_set))
    print "The number of non-expert learners is: " + str(len(non_expert_learner_set)) + "\n"

    print "All of Geo's emails is: " + str(len(all_Geo_email_set))
    print "Effective Geo's emails is: " + str(len(effective_Geo_email_set)) + "\n"
        
    after_fp = Set()
    after_new_fp = Set()
    after_old_fp = Set()
    
    new_ratio = 0
    
    before_old_rator = 0
    after_old_ratio = 0 
    
    # after_non_effective_github_set = set()   
    
    # Processing after_fp101 data
    for file in files:
        if "after" in file:
                            
            fp = open(path + file,"r")
            nameLine = fp.readline()
            names = nameLine.split(",")
            # print names[18] + "\t" + names[19] + "\t" + names[23]
            
            lines = fp.readlines()
              
            for line in lines:
                
                line = line.replace("\n","")
                
                # To select experts
                line = str.lower(line)
                array = line.split(",")
                
                email = array[0]
                    
                if email_user_map.has_key(email):
                    if array[18] != "0" or array[19] != "0" or array[23] != "0":
                        after_fp.add(email)
                        
                        if email in expert_learner_set:
                            after_old_fp.add(email)
                            
                            num_fp_lines = 0
                            num_non_fp_lines = 0
                            for i in range(2,24):
                                if i in [18, 19, 23]:
                                    num_fp_lines += float(array[i])
                                else:
                                    num_non_fp_lines += float(array[i])
                            
                            after_old_ratio += num_fp_lines/(num_fp_lines+num_non_fp_lines)
                            before_old_rator += before_ratio_map[email]["fp"] / (before_ratio_map[email]["fp"] + before_ratio_map[email]["non_fp"])
                            
                        else:
                            after_new_fp.add(email)
                            
                            num_fp_lines = 0
                            num_non_fp_lines = 0
                            for i in range(2,24):
                                if i in [18, 19, 23]:
                                    num_fp_lines += float(array[i])
                                else:
                                    num_non_fp_lines += float(array[i])
                        
                            new_ratio += num_fp_lines/(num_fp_lines+num_non_fp_lines)
                '''
                else:
                    if email in after_non_effective_github_set:
                        print email
                    else:
                        after_non_effective_github_set.add(email)
                '''
              
    print "After: all fp learners: " + str(len(after_fp))
    print "After: old fp learners: " + str(len(after_old_fp))
    print "After: new  fp learners: " + str(len(after_new_fp))
    print "FP percentage is: " + str(new_ratio/len(after_new_fp)) + "\n"
    
    print "Old FP programmers before percentage: " + str(before_old_rator/len(after_old_fp))
    print "Old FP programmers after percentage: " + str(after_old_ratio/len(after_old_fp)) + "\n"
    
    
####################################################
    
course_path = "/Volumes/NETAC/EdX/Clear-out/FP101x/"
InsertExpertMark(course_path)
# ExpertTrendsAnalyzer(course_path)
print "Finished."



