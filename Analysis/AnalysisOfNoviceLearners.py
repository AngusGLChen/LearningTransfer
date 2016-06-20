'''
Created on Aug 24, 2015

@author: Angus
'''

import mysql.connector
from HypothesisValidation.SeekLearners import SeekNoviceLearners, SeekActiveLearners, SeekCompletedLearners

import matplotlib.pyplot as plt
import numpy as np

def AnalysisOfLearners(learners, tag):
    
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='MOOC')
    cursor = connection.cursor()
    
    # 1. Average time spent on watching video
    sql_query = "SELECT observations.course_user_id, SUM(duration)/60 FROM observations, global_user WHERE observations.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" GROUP BY observations.course_user_id"
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    avgTime = 0
    cnt = 0
        
    for result in results:
        course_user_id = result[0]
        time = result[1]
        
        if course_user_id in learners:
            cnt += 1
            avgTime += time
    
    avgTime /= float(cnt)
    print "The average time spent on watching video is: " + str(round(avgTime,2))
    
    # 2. Average number of questions learners attempted to solve
    sql_query = "SELECT submissions.course_user_id, COUNT(submissions.problem_id) FROM submissions, global_user WHERE submissions.course_user_id = global_user.course_user_id AND global_user.course_id = \"DelftX/FP101x/3T2014\" GROUP BY submissions.course_user_id"
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    avgAttemptedQuestion = 0
    cnt = 0
        
    for result in results:
        course_user_id = result[0]
        num_question = result[1]
        
        if course_user_id in learners:
            cnt += 1
            avgAttemptedQuestion += num_question
    
    avgAttemptedQuestion /= float(cnt)
    print "The average number of questions attempted to solve is: " + str(round(avgAttemptedQuestion,2))
    
    # 3. Average number of problems answered correctly
    sql_query = "SELECT assessments.course_user_id, COUNT(*) AS correct_answer FROM assessments, global_user WHERE assessments.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND grade!=0 GROUP BY assessments.course_user_id"
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    avgCorrectedQuestion = 0
    cnt = 0
        
    for result in results:
        course_user_id = result[0]
        num_question = result[1]
        
        if course_user_id in learners:
            cnt += 1
            avgCorrectedQuestion += num_question
    
    avgCorrectedQuestion /= float(cnt)
    print "The average number of questions answered correctly is: " + str(round(avgCorrectedQuestion,2))
    
    # 4. Average accuracy of answers
    sql_query = "SELECT assessments.course_user_id, COUNT(*)/num_correct FROM assessments, global_user, (SELECT assessments.course_user_id, COUNT(*) as num_correct FROM assessments, global_user WHERE assessments.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" GROUP BY assessments.course_user_id) as attempts WHERE assessments.course_user_id=global_user.course_user_id AND course_id=\"DelftX/FP101x/3T2014\" AND grade!= 0 AND assessments.course_user_id=attempts.course_user_id GROUP BY assessments.course_user_id"
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    avgAccuracy = 0
    cnt = 0
        
    for result in results:
        course_user_id = result[0]
        accuracy = result[1]
        
        if course_user_id in learners:
            cnt += 1
            avgAccuracy += accuracy
   
    avgAccuracy = float(avgAccuracy) / cnt
    print "The average accuracy of questions is: " + str(round(avgAccuracy*100,2))
    
    # 5. Active weeks
    observation_sql_query = "SELECT observations.course_user_id, resources.relevant_week FROM observations, global_user, resources WHERE observations.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND observations.resource_id=resources.resource_id"
    submission_sql_query = "SELECT submissions.course_user_id, resources.relevant_week FROM submissions, global_user, problems, resources WHERE submissions.course_user_id=global_user.course_user_id AND global_user.course_id=\"DelftX/FP101x/3T2014\" AND submissions.problem_id=problems.problem_id AND problems.problem_id=resources.resource_id"
    
    learner_week_map = {}
    sql_array = [observation_sql_query, submission_sql_query]

    for sql_query in sql_array:    
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        for result in results:
            course_user_id = result[0]
            week = result[1]
            
            if learner_week_map.has_key(course_user_id):
                learner_week_map[course_user_id].add(week)
            else:
                learner_week_map[course_user_id] = set()
                learner_week_map[course_user_id].add(week)
                
    num_weeks = 8
    plot_x = []
    plot_y = []    

    for i in range(num_weeks):
        week = i + 1
        plot_x.append(week)
        plot_y.append(0)
        
    for learner in learners:
        if learner in learner_week_map.keys():
            for week in learner_week_map[learner]:
                plot_y[week-1] += 1
            
    for i in range(len(plot_y)):
        plot_y[i] = plot_y[i] / float(len(learners))
    
    if tag =="active_novice_learners":
        plt.plot(plot_x, plot_y, color='r', marker='o', label='all')
    if tag =="completed_active_novice_learners":
        plt.plot(plot_x, plot_y, color='g', marker='o', label='completed')
    if tag =="non-completed_active_novice_learners":
        plt.plot(plot_x, plot_y, color='b', marker='o', label='non-completed')   
    
    
    print "------------------------------------------------------------"
        
    

def AnalysisOfNoviceLearners(path):
    
    novice_learner_set = SeekNoviceLearners(path)
    
    active_tags = ["observation","submission"]
    active_learner_set = SeekActiveLearners(active_tags)
    
    completed_learners = SeekCompletedLearners()
    
    # Different groups of learners to be analyzed
    active_novice_learners = set()
    complted_active_novice_learners = set()
    nonCompleted_active_novice_learners = set()

    for learner in novice_learner_set:
        
        if learner in active_learner_set:
            active_novice_learners.add(learner)
            
            if learner in completed_learners:
                complted_active_novice_learners.add(learner)
            else:
                nonCompleted_active_novice_learners.add(learner)
    
    print "The number of overlap learners is: " + str(len(active_novice_learners))
    print "The number of completed overlap learners is: " + str(len(complted_active_novice_learners))
    print "The number of NON_completed overlap learners is: " + str(len(nonCompleted_active_novice_learners))
    print "-----------------------------------------------------------------\n"
    
    print "Active novice learners..."
    AnalysisOfLearners(active_novice_learners, "active_novice_learners")
    print "Active completed novice learners..."
    AnalysisOfLearners(complted_active_novice_learners, "completed_active_novice_learners")
    print "Active nonCompleted novice learners..."
    AnalysisOfLearners(nonCompleted_active_novice_learners, "non-completed_active_novice_learners")
    
    plt.legend(loc='lower left')   
    plt.show()
    
    
    
    
    

    
    















####################################################
course_path = "/Volumes/NETAC/EdX/Clear-out/FP101x/"
AnalysisOfNoviceLearners(course_path)
print "Finished."