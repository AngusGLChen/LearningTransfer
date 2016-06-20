'''
Created on Aug 20, 2015

@author: Angus
'''

import mysql.connector
import scipy
from scipy.stats import mannwhitneyu

def SignificantTest():
    
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='MOOC')
    cursor = connection.cursor()
    
    array = []
    non_array = []
    
    ###################################################
    # GitHub vs. Non-GitHub
    # Average time spent on watching video
    sql_query = "SELECT SUM(duration) FROM observations JOIN global_user ON observations.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND github_mark=TRUE GROUP BY observations.course_user_id"
    non_sql_query = "SELECT SUM(duration) FROM observations JOIN global_user ON observations.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND github_mark=FALSE GROUP BY observations.course_user_id"

    # Average number of questions learners attempted to solve
    sql_query = "SELECT COUNT(DISTINCT(problem_id)) FROM submissions, global_user WHERE submissions.course_user_id = global_user.course_user_id AND global_user.course_id =  \"DelftX/FP101x/3T2014\" AND global_user.github_mark=TRUE GROUP BY submissions.course_user_id"
    non_sql_query = "SELECT COUNT(DISTINCT(problem_id)) FROM submissions, global_user WHERE submissions.course_user_id = global_user.course_user_id AND global_user.course_id =  \"DelftX/FP101x/3T2014\" AND global_user.github_mark=FALSE GROUP BY submissions.course_user_id"
    
    # Average number of problems answered correctly
    sql_query = "SELECT COUNT(assessment_id) FROM assessments, global_user WHERE assessments.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND grade!=0 AND github_mark=TRUE GROUP BY assessments.course_user_id"
    non_sql_query = "SELECT COUNT(assessment_id) FROM assessments, global_user WHERE assessments.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND grade!=0 AND github_mark=FALSE GROUP BY assessments.course_user_id"
    
    # Average accuracy of answers
    sql_query = "SELECT COUNT(assessments.assessment_id)/num_correct FROM assessments, global_user, (SELECT assessments.course_user_id, COUNT(assessments.course_user_id) as num_correct FROM assessments JOIN global_user ON assessments.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND github_mark=TRUE GROUP BY assessments.course_user_id) as attempts WHERE assessments.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND github_mark=TRUE AND grade!= 0 AND assessments.course_user_id=attempts.course_user_id GROUP BY assessments.course_user_id"
    non_sql_query = "SELECT COUNT(assessments.assessment_id)/num_correct FROM assessments, global_user, (SELECT assessments.course_user_id, COUNT(assessments.course_user_id) as num_correct FROM assessments JOIN global_user ON assessments.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND github_mark=FALSE GROUP BY assessments.course_user_id) as attempts WHERE assessments.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND github_mark=FALSE AND grade!= 0 AND assessments.course_user_id=attempts.course_user_id GROUP BY assessments.course_user_id"
    
    ###################################################
    # Expert vs. Non-Expert
    
    # Expert - Average time spent on watching video
    sql_query = "SELECT SUM(duration) FROM observations JOIN global_user ON observations.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND github_mark=TRUE AND github_expert_mark=TRUE GROUP BY observations.course_user_id"
    non_sql_query = "SELECT SUM(duration) FROM observations JOIN global_user ON observations.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND github_mark=TRUE AND github_expert_mark=FALSE GROUP BY observations.course_user_id"
   
    # Expert - Average number of questions learners attempted to solve
    sql_query ="SELECT COUNT(problem_id) FROM submissions JOIN global_user ON submissions.course_user_id = global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND github_mark=TRUE AND github_expert_mark=TRUE GROUP BY submissions.course_user_id"
    non_sql_query = "SELECT COUNT(problem_id) FROM submissions JOIN global_user ON submissions.course_user_id = global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND github_mark=TRUE AND github_expert_mark=FALSE GROUP BY submissions.course_user_id"
    
    # Expert - Average number of problems answered correctly
    sql_query = "SELECT COUNT(assessment_id) FROM assessments JOIN global_user ON assessments.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND grade!=0 AND github_mark=TRUE AND github_expert_mark=TRUE GROUP BY assessments.course_user_id"
    non_sql_query = "SELECT COUNT(assessment_id) FROM assessments JOIN global_user ON assessments.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND grade!=0 AND github_mark=TRUE AND github_expert_mark=FALSE GROUP BY assessments.course_user_id"
    
    # Expert - Average accuracy of answers
    sql_query = "SELECT COUNT(assessments.assessment_id)/num_correct FROM assessments, global_user, (SELECT assessments.course_user_id, COUNT(assessments.course_user_id) as num_correct FROM assessments JOIN global_user ON assessments.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND github_mark=TRUE AND github_expert_mark=TRUE GROUP BY assessments.course_user_id) as attempts WHERE assessments.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND github_mark=TRUE AND github_expert_mark=TRUE AND grade!= 0 AND assessments.course_user_id=attempts.course_user_id GROUP BY assessments.course_user_id"    
    non_sql_query = "SELECT COUNT(assessments.assessment_id)/num_correct FROM assessments, global_user, (SELECT assessments.course_user_id, COUNT(assessments.course_user_id) as num_correct FROM assessments JOIN global_user ON assessments.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND github_mark=TRUE AND github_expert_mark=FALSE GROUP BY assessments.course_user_id) as attempts WHERE assessments.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND github_mark=TRUE AND github_expert_mark=FALSE AND grade!= 0 AND assessments.course_user_id=attempts.course_user_id GROUP BY assessments.course_user_id"
   
    cursor.execute(sql_query)
    for element in cursor:
        array.append(element[0])
     
    cursor.execute(non_sql_query) 
    for element in cursor:
        non_array.append(element[0])
        
    print scipy.stats.mannwhitneyu(array,non_array)


###################################################
SignificantTest()
