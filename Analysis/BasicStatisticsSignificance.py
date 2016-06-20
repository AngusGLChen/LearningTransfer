'''
Created on Sep 18, 2015

@author: Angus
'''

import mysql.connector
import scipy
from scipy.stats import mannwhitneyu

def ToComputeAverage(array):    
    sum = 0    
    for element in array:
        sum += float(element)
    sum /= float(len(array))
    print "The average value is:" + str(round(sum,2))

def GitHubTest(cursor):
    
    # To retrieve the list of the GitHub learner
    learner_set = set()
    non_learner_set = set()
    
    sql_query = "SELECT global_user_id FROM global_user WHERE global_user.course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=TRUE"
    non_sql_query = "SELECT global_user_id FROM global_user WHERE global_user.course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=FALSE"
        
    cursor.execute(sql_query)
    results = cursor.fetchall()
    for result in results:
        learner_set.add(result[0])
    
    cursor.execute(non_sql_query)
    results = cursor.fetchall()
    for result in results:
        non_learner_set.add(result[0])
    
    print "The number of GH vs. Non-GH learners is: " + str(len(learner_set)) + "\t" + str(len(non_learner_set))
    
    # To query and perform the significant analysis
    array = []
    non_array = []
    
    sql_query = "SELECT SUM(observations.duration) FROM observations, global_user WHERE observations.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=TRUE GROUP BY observations.course_user_id"
    non_sql_query = "SELECT SUM(observations.duration) FROM observations, global_user WHERE observations.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=FALSE GROUP BY observations.course_user_id"
    '''
    sql_query = "SELECT COUNT(submissions.submission_id) FROM submissions, global_user WHERE submissions.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=TRUE GROUP BY submissions.course_user_id"
    non_sql_query = "SELECT COUNT(submissions.submission_id) FROM submissions, global_user WHERE submissions.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=FALSE GROUP BY submissions.course_user_id"
    
    sql_query = "SELECT COUNT(assessments.assessment_id) FROM assessments, global_user WHERE assessments.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND assessments.grade!=0 AND global_user.github_mark=TRUE GROUP BY assessments.course_user_id"
    non_sql_query = "SELECT COUNT(assessments.assessment_id) FROM assessments, global_user WHERE assessments.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND assessments.grade!=0 AND global_user.github_mark=FALSE GROUP BY assessments.course_user_id"
    
    sql_query = "SELECT COUNT(assessments.assessment_id)/T1.Num_attempts FROM assessments, (SELECT assessments.course_user_id, COUNT(assessments.assessment_id) AS Num_attempts FROM assessments, global_user WHERE assessments.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=TRUE GROUP BY assessments.course_user_id) AS T1 WHERE assessments.course_user_id=T1.course_user_id AND assessments.grade!=0 GROUP BY assessments.course_user_id"
    non_sql_query = "SELECT COUNT(assessments.assessment_id)/T1.Num_attempts FROM assessments, (SELECT assessments.course_user_id, COUNT(assessments.assessment_id) AS Num_attempts FROM assessments, global_user WHERE assessments.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=FALSE GROUP BY assessments.course_user_id) AS T1 WHERE assessments.course_user_id=T1.course_user_id AND assessments.grade!=0 GROUP BY assessments.course_user_id"
    
    sql_query = "SELECT COUNT(collaborations.collaboration_id) FROM collaborations, global_user WHERE collaborations.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=TRUE GROUP BY collaborations.course_user_id"
    non_sql_query = "SELECT COUNT(collaborations.collaboration_id) FROM collaborations, global_user WHERE collaborations.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=FALSE GROUP BY collaborations.course_user_id"
    '''   
    cursor.execute(sql_query)
    results = cursor.fetchall()
    for result in results:
        array.append(result[0])
    
    cursor.execute(non_sql_query)
    results = cursor.fetchall()
    for result in results:
        non_array.append(result[0])
    
    print "The number of records: " + str(len(array)) + "\t" + str(len(non_array))   
    
    while len(array) != len(learner_set):
        array.append(0)
    while len(non_array) != len(non_learner_set):
        non_array.append(0)
        
    ToComputeAverage(array)
    ToComputeAverage(non_array)
    
    print scipy.stats.mannwhitneyu(array,non_array)
    
def ExpertTest(cursor):
    
    # To retrieve the list of the Dedicated BE/Non-BE learner
    learner_set = set()
    non_learner_set = set()
    
    sql_query = "SELECT global_user_id FROM global_user WHERE global_user.course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=TRUE AND global_user.github_expert_mark=TRUE"
    non_sql_query = "SELECT global_user_id FROM global_user WHERE global_user.course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=TRUE AND global_user.github_expert_mark=FALSE"
    
    cursor.execute(sql_query)
    results = cursor.fetchall()
    for result in results:
        learner_set.add(result[0])
    
    cursor.execute(non_sql_query)
    results = cursor.fetchall()
    for result in results:
        non_learner_set.add(result[0])
    
    print "The number of Dedicated BE vs. Non-BE learners is: " + str(len(learner_set)) + "\t" + str(len(non_learner_set))
    
    # To query and perform the significant analysis
    array = []
    non_array = []
    
    sql_query = "SELECT SUM(observations.duration) FROM observations, global_user WHERE observations.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=TRUE AND global_user.github_expert_mark=TRUE GROUP BY observations.course_user_id"
    non_sql_query = "SELECT SUM(observations.duration) FROM observations, global_user WHERE observations.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=TRUE AND global_user.github_expert_mark=FALSE GROUP BY observations.course_user_id"
    '''
    sql_query = "SELECT COUNT(submissions.submission_id) FROM submissions, global_user WHERE submissions.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=TRUE AND global_user.github_expert_mark=TRUE GROUP BY submissions.course_user_id"
    non_sql_query = "SELECT COUNT(submissions.submission_id) FROM submissions, global_user WHERE submissions.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=TRUE AND global_user.github_expert_mark=FALSE GROUP BY submissions.course_user_id"
    
    sql_query = "SELECT COUNT(assessments.assessment_id) FROM assessments, global_user WHERE assessments.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND assessments.grade!=0 AND global_user.github_mark=TRUE AND global_user.github_expert_mark=TRUE GROUP BY assessments.course_user_id"
    non_sql_query = "SELECT COUNT(assessments.assessment_id) FROM assessments, global_user WHERE assessments.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND assessments.grade!=0 AND global_user.github_mark=TRUE AND global_user.github_expert_mark=FALSE GROUP BY assessments.course_user_id"
    
    sql_query = "SELECT COUNT(assessments.assessment_id)/T1.Num_attempts FROM assessments, (SELECT assessments.course_user_id, COUNT(assessments.assessment_id) AS Num_attempts FROM assessments, global_user WHERE assessments.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=TRUE AND global_user.github_expert_mark=TRUE GROUP BY assessments.course_user_id) AS T1 WHERE assessments.course_user_id=T1.course_user_id AND assessments.grade!=0 GROUP BY assessments.course_user_id"
    non_sql_query = "SELECT COUNT(assessments.assessment_id)/T1.Num_attempts FROM assessments, (SELECT assessments.course_user_id, COUNT(assessments.assessment_id) AS Num_attempts FROM assessments, global_user WHERE assessments.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=TRUE AND global_user.github_expert_mark=FALSE GROUP BY assessments.course_user_id) AS T1 WHERE assessments.course_user_id=T1.course_user_id AND assessments.grade!=0 GROUP BY assessments.course_user_id"
    
    sql_query = "SELECT COUNT(collaborations.collaboration_id) FROM collaborations, global_user WHERE collaborations.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=TRUE AND global_user.github_expert_mark=TRUE GROUP BY collaborations.course_user_id"
    non_sql_query = "SELECT COUNT(collaborations.collaboration_id) FROM collaborations, global_user WHERE collaborations.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND global_user.github_mark=TRUE AND global_user.github_expert_mark=FALSE GROUP BY collaborations.course_user_id"
    '''
    cursor.execute(sql_query)
    results = cursor.fetchall()
    for result in results:
        array.append(result[0])
    
    cursor.execute(non_sql_query)
    results = cursor.fetchall()
    for result in results:
        non_array.append(result[0])
    
    print "The number of records: " + str(len(array)) + "\t" + str(len(non_array))   
    
    while len(array) != len(learner_set):
        array.append(0)
    while len(non_array) != len(non_learner_set):
        non_array.append(0)
    
    ToComputeAverage(array)
    ToComputeAverage(non_array)
    
    print scipy.stats.mannwhitneyu(array,non_array)

def BasicStatisticsSignificance():
    
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='FP101x')
    cursor = connection.cursor()
    
    #####################################
    # For GH learners vs. Non-GH learners
    GitHubTest(cursor)
    
    #####################################
    # For Expert learners vs. Non-Expert learners
    ExpertTest(cursor)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


####################################################    
BasicStatisticsSignificance()
print "Finished."

