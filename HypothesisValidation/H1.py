'''
Created on Aug 20, 2015

@author: Angus
'''

import mysql.connector

from HypothesisValidation.SeekLearners import SeekNoviceLearners, SeekTransferedExpertLearners
    
def H1(path):    
    
    novice_learner_set = SeekNoviceLearners(path)
    # transftered_expert_learner_set = SeekTransferedExpertLearners(path)
    
    completed_learner_set = set()
    
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='MOOC')
    cursor = connection.cursor()
    
    sql_query = "SELECT course_user.course_user_id FROM course_user, global_user WHERE course_user.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=TRUE AND certificate_status=\"downloadable\""
    cursor.execute(sql_query)
    for element in cursor:
        completed_learner_set.add(element[0])
    
    print "---------------------------------------------------------"
    print "The number of completed learners is: " + str(len(completed_learner_set)) + "\n"

    cnt = 0
    for learner in novice_learner_set:
        if learner in completed_learner_set:
            cnt += 1
            # print learner

    print "The number of completed learners among novice learners is: " + str(cnt) + "\n"
    
    '''    
    cnt = 0
    for learner in transftered_expert_learner_set:
            if learner in completed_learner_set:
                cnt += 1

    print "The number of completed learners among non-novice learners is: " + str(cnt) + "\n"
    '''
    
    
    
####################################################    
course_path = "/Volumes/NETAC/EdX/Clear-out/FP101x/"
H1(course_path)
print "Finished."














    
    