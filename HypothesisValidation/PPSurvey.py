'''
Created on Aug 26, 2015

@author: Angus
'''

from HypothesisValidation.SeekLearners import SeekCompleter,\
    SeekNonTransferrer, SeekNonExpert, SeekSurveyLearners,  SeekExpert,\
    SeekHighSelfEfficacyLearners, SeekTransferrer, SeekNonCompleter,\
    SeekEngagedLearners, SeekNonEngagedLearner
import mysql.connector

def GroupA(path, mark):    
    # Group A: Novie & Completer & No transfer
    nonExpert_set = SeekNonExpert(path)
    print "\n"
    
    if mark=="completed":
        completer_set = SeekCompleter()
    if mark=="engaged":
        completer_set = SeekEngagedLearners(["observation", "submission"])
    print "\n"
    
    nonTransferrer_set = SeekNonTransferrer(path)
    print "\n"
    
    survey_learner_set = SeekSurveyLearners(path)
    print "\n"

    overlap_set = set()    
    final_overlap_set = set()

    for learner in completer_set:
        if learner in nonExpert_set and learner in nonTransferrer_set:
            overlap_set.add(learner)    
    print "The overlap is: " + str(len(overlap_set))    
    
    for learner in overlap_set:
        if learner in survey_learner_set:
            final_overlap_set.add(learner)
    
    print "After checking the survey learners, the overlap is: " + str(len(final_overlap_set))
    return final_overlap_set
    
def GroupB(path, mark):
    # Group B: Expert & Completer & No transfer
    expert_set = SeekExpert(path)
    print "\n"
    
    if mark=="completed":
        completer_set = SeekCompleter()
    if mark=="engaged":
        completer_set = SeekEngagedLearners(["observation", "submission"])
    print "\n"
    
    nonTransferrer_set = SeekNonTransferrer(path)
    print "\n"
    
    survey_learner_set = SeekSurveyLearners(path)
    print "\n"

    overlap_set = set()    
    final_overlap_set = set()

    for learner in completer_set:
        if learner in expert_set and learner in nonTransferrer_set:
            overlap_set.add(learner)    
    print "The overlap is: " + str(len(overlap_set))    
    
    for learner in overlap_set:
        if learner in survey_learner_set:
            final_overlap_set.add(learner)
    
    print "After checking the survey learners, the overlap is: " + str(len(final_overlap_set))
    return final_overlap_set

def GroupC(path, mark):
    # Group C: Novice & Completer & With transfer
    nonExpert_set = SeekNonExpert(path)
    print "\n"
    
    if mark=="completed":
        completer_set = SeekCompleter()
    if mark=="engaged":
        completer_set = SeekEngagedLearners(["observation", "submission"])
    print "\n"
    
    transferrer_set = SeekTransferrer(path)
    print "\n"
    
    survey_learner_set = SeekSurveyLearners(path)
    print "\n"

    overlap_set = set()    
    final_overlap_set = set()

    for learner in completer_set:
        if learner in nonExpert_set and learner in transferrer_set:
            overlap_set.add(learner)    
    print "The overlap is: " + str(len(overlap_set))    
    
    for learner in overlap_set:
        if learner in survey_learner_set:
            final_overlap_set.add(learner)
    
    print "After checking the survey learners, the overlap is: " + str(len(final_overlap_set))
    return final_overlap_set

def GroupD(path, mark):
    # Group D: Novice & nonCompleter/nonEngaged & With transfer
    nonExpert_set = SeekNonExpert(path)
    print "\n"
    
    if mark=="completed":
        nonCompleter_set = SeekNonCompleter()
    if mark=="engaged":
        nonCompleter_set = SeekNonEngagedLearner(["observation", "submission"])
    print "\n"
    
    transferrer_set = SeekTransferrer(path)
    print "\n"
    
    survey_learner_set = SeekSurveyLearners(path)
    print "\n"

    overlap_set = set()    
    final_overlap_set = set()

    for learner in nonCompleter_set:
        if learner in nonExpert_set and learner in transferrer_set:
            overlap_set.add(learner)    
    print "The overlap is: " + str(len(overlap_set))    
    
    for learner in overlap_set:
        if learner in survey_learner_set:
            final_overlap_set.add(learner)
    
    print "After checking the survey learners, the overlap is: " + str(len(final_overlap_set))
    return final_overlap_set

def GroupE(path, mark):
    # Group E: Expert & Completer & With transfer
    expert_set = SeekExpert(path)
    print "\n"
    
    if mark=="completed":
        completer_set = SeekCompleter()
    if mark=="engaged":
        completer_set = SeekEngagedLearners(["observation", "submission"])
    print "\n"
    
    transferrer_set = SeekTransferrer(path)
    print "\n"
    
    survey_learner_set = SeekSurveyLearners(path)
    print "\n"

    overlap_set = set()    
    final_overlap_set = set()

    for learner in completer_set:
        if learner in expert_set and learner in transferrer_set:
            overlap_set.add(learner)    
    print "The overlap is: " + str(len(overlap_set))    
    
    for learner in overlap_set:
        if learner in survey_learner_set:
            final_overlap_set.add(learner)
    
    print "After checking the survey learners, the overlap is: " + str(len(final_overlap_set))
    return final_overlap_set
         
def GroupF(path, mark):
    # Group F: Expert & nonCompleter & With transfer
    expert_set = SeekExpert(path)
    print "\n"
    
    if mark=="completed":
        nonCompleter_set = SeekNonCompleter()
    if mark=="engaged":
        nonCompleter_set = SeekNonEngagedLearner(["observation", "submission"])
    print "\n"
    
    transferrer_set = SeekTransferrer(path)
    print "\n"
    
    survey_learner_set = SeekSurveyLearners(path)
    print "\n"

    overlap_set = set()    
    final_overlap_set = set()

    for learner in nonCompleter_set:
        if learner in expert_set and learner in transferrer_set:
            overlap_set.add(learner)    
    print "The overlap is: " + str(len(overlap_set))    
    
    for learner in overlap_set:
        if learner in survey_learner_set:
            final_overlap_set.add(learner)
    
    print "After checking the survey learners, the overlap is: " + str(len(final_overlap_set))
    return final_overlap_set

def GroupEfficacy(path):
    # Group Efficacy: High self-efficacy & No transfer
    efficacy_learner_set = SeekHighSelfEfficacyLearners()
    nonTransferrer_set = SeekNonTransferrer(path)
    print "\n"
    
    survey_learner_set = SeekSurveyLearners(path)
    print "\n"

    overlap_set = set()    
    final_overlap_set = set()

    for learner in efficacy_learner_set:
        if learner in nonTransferrer_set:
            overlap_set.add(learner)    
    print "The overlap is: " + str(len(overlap_set))    
    
    for learner in overlap_set:
        if learner in survey_learner_set:
            final_overlap_set.add(learner)
    
    print "After checking the survey learners, the overlap is: " + str(len(final_overlap_set))
    return final_overlap_set

def ComputeOverlap(group1, group2):
    cnt = 0
    for learner in group1:
        if learner in group2:
            cnt += 1
    print "The overlap is: " + str(cnt)

def ComputeAllLearners(group_sets, all_learners):
    for group_set in group_sets:
        for group in group_set:
            for learner in group:
                all_learners.add(learner)
    print "The number of all learners is: " + str(len(all_learners))
    
def ToSelectLearners(learners, num):    
    while len(learners) != num:
        learners.pop()   

def ToSeekEmail(learners):
    connection = mysql.connector.connect(user='root', password='admin', host='127.0.0.1', database='MOOC')
    cursor = connection.cursor()
    
    email_set = set()
    
    for learner in learners:     
        sql_query = "SELECT user_pii.email FROM user_pii, global_user WHERE user_pii.global_user_id=global_user.global_user_id AND global_user.course_user_id=\"" + str(learner) + "\""
        cursor.execute(sql_query)
        results = cursor.fetchall()
        for result in results:
            email_set.add(result[0])
    
    return email_set

def ToPrintEmail(path, emails):
    fp = open(path, "w")
    for email in emails:
        fp.write(email + ";\n")
    print "\n"

def ToSeekSentLearners(path, emails):    
    fp = open(path, "r")
    for line in fp:
        line = line.replace("\n", "")
        emails.remove(line)
    

   
####################################################
course_path = "/Volumes/NETAC/EdX/Clear-out/FP101x/"

'''
# To check overlap
#group_set1 = [GroupA(course_path, "completed"), GroupB(course_path, "completed")]
#group_set2 = [GroupC(course_path, "completed"), GroupD(course_path, "completed"), GroupE(course_path, "completed"), GroupF(course_path, "completed")]

group_set1 = [GroupA(course_path, "engaged"), GroupB(course_path, "engaged")]
group_set2 = [GroupC(course_path, "engaged"), GroupD(course_path, "engaged"), GroupE(course_path, "engaged"), GroupF(course_path, "engaged")]

all_learners = set()

print "\n\n\n"
print "-----------------------------"
for group_set in [group_set1, group_set2]:
    for i in range(0, len(group_set)):
        for j in range(i+1, len(group_set)):
            if i != j:
                print str(i) + "\t" + str(j)
                group1 = group_set[i]
                group2 = group_set[j]    
                ComputeOverlap(group1, group2)

ComputeAllLearners([group_set1, group_set2], all_learners)
'''
'''
# For group A
group_A = GroupA(course_path, "completed")
ToSelectLearners(group_A, 50)
email_set_A = ToSeekEmail(group_A)
ToPrintEmail(email_set_A)
'''
'''
# For group B
group_B = GroupB(course_path, "completed")
ToSelectLearners(group_B, 10)
email_set_B = ToSeekEmail(group_B)
ToPrintEmail(email_set_B)
'''
'''
# For group C
group_C = GroupC(course_path, "completed")
ToSelectLearners(group_C, 10)
email_set_C = ToSeekEmail(group_C)
ToPrintEmail(email_set_C)
'''
'''
# For group D
group_D = GroupD(course_path, "completed")

group_D_duplicate = GroupD(course_path, "engaged")
group_D = group_D.difference(group_D_duplicate)

ToSelectLearners(group_D, 10)
email_set_D = ToSeekEmail(group_D)
ToPrintEmail(email_set_D)
'''
'''
# For group E
group_E = GroupE(course_path, "completed")
ToSelectLearners(group_E, 10)
email_set_E = ToSeekEmail(group_E)
ToPrintEmail(email_set_E)
'''
'''
# For group F
group_F = GroupF(course_path, "completed")

group_F_duplicate = GroupF(course_path, "engaged")
group_F = group_F.difference(group_F_duplicate)

ToSelectLearners(group_F, 10)
email_set_F = ToSeekEmail(group_F)
ToPrintEmail(email_set_F)

##################################################

# 1. For group A (completed learners) - Remaining
group_A = GroupA(course_path, "completed")
email_set_A = ToSeekEmail(group_A)
print "---------------------------------------------"
print "The size of learners is: " + str(len(email_set_A))
ToSeekSentLearners(course_path + "post++/group_a", email_set_A)
print "The size of learners is: " + str(len(email_set_A))
ToPrintEmail(course_path + "post++/group_a(remaining completed learners).txt", email_set_A)

# 1. For group A (engaged learners)
group_A = GroupA(course_path, "engaged")
group_A_filter = GroupA(course_path, "completed")
print "---------------------------------------------"
print "The size of learners is: " + str(len(group_A))
for learner in group_A_filter:
    group_A.remove(learner)
print "The size of learners is: " + str(len(group_A))
email_set_A = ToSeekEmail(group_A)
ToPrintEmail(course_path + "post++/group_a(engaged learners) - NEW.txt", email_set_A)

# 2. For group B (completed learners) - Remaining
group_B = GroupB(course_path, "completed")
email_set_B = ToSeekEmail(group_B)
print "---------------------------------------------"
print "The size of learners is: " + str(len(email_set_B))
ToSeekSentLearners(course_path + "post++/group_b", email_set_B)
print "The size of learners is: " + str(len(email_set_B))
ToPrintEmail(course_path + "post++/group_b(remaining completed learners).txt", email_set_B)

# 2. For group B (engaged learners)
group_B = GroupB(course_path, "engaged")
group_B_filter = GroupB(course_path, "completed")
print "---------------------------------------------"
print "The size of learners is: " + str(len(group_B))
for learner in group_B_filter:
    group_B.remove(learner)
print "The size of learners is: " + str(len(group_B))
email_set_B = ToSeekEmail(group_B)
ToPrintEmail(course_path + "post++/group_b(engaged learners) - NEW.txt", email_set_B)

# 3. For group C (completed learners) - Remaining
group_C = GroupC(course_path, "completed")
email_set_C = ToSeekEmail(group_C)
print "---------------------------------------------"
print "The size of learners is: " + str(len(email_set_C))
ToSeekSentLearners(course_path + "post++/group_c", email_set_C)
print "The size of learners is: " + str(len(email_set_C))
ToPrintEmail(course_path + "post++/group_c(remaining completed learners).txt", email_set_C)

# 4. For group D (non-completed learners) - Remaining
group_D = GroupD(course_path, "completed")
group_D_filter = GroupD(course_path, "engaged")
group_D = group_D.difference(group_D_filter)

print "The size of learners is: " + str(len(group_D))

email_set_D = ToSeekEmail(group_D)
print "---------------------------------------------"
print "The size of learners is: " + str(len(email_set_D))
ToSeekSentLearners(course_path + "post++/group_d", email_set_D)
print "The size of learners is: " + str(len(email_set_D))

ToPrintEmail(course_path + "post++/group_d(remaining non-completed but engaged learners) - NEW.txt", email_set_D)

# 4(1) For group D (non-engaged learners)
group_D = GroupD(course_path, "engaged")
email_set_D = ToSeekEmail(group_D)
print "---------------------------------------------"
print "The size of learners is: " + str(len(email_set_D))
ToPrintEmail(course_path + "post++/group_d(non-engaged learners) - NEW.txt", email_set_D)

# 5. For group E (completed learners) - Remaining
group_E = GroupE(course_path, "completed")
email_set_E = ToSeekEmail(group_E)
print "---------------------------------------------"
print "The size of learners is: " + str(len(email_set_E))
ToSeekSentLearners(course_path + "post++/group_e", email_set_E)
print "The size of learners is: " + str(len(email_set_E))
ToPrintEmail(course_path + "post++/group_e(remaining completed learners).txt", email_set_E)

# 6. For group F (non-completed learners) - Remaining
group_F = GroupF(course_path, "completed")
group_F_filter = GroupF(course_path, "engaged")
group_F = group_F.difference(group_F_filter)

print "The size of learners is: " + str(len(group_F))

email_set_F = ToSeekEmail(group_F)
print "---------------------------------------------"
print "The size of learners is: " + str(len(email_set_F))
ToSeekSentLearners(course_path + "post++/group_f", email_set_F)
print "The size of learners is: " + str(len(email_set_F))

ToPrintEmail(course_path + "post++/group_f(remaining non-completed but engaged learners) - NEW.txt", email_set_F)
'''

# 6(1) For group F (non-engaged learners)
group_F = GroupF(course_path, "engaged")
email_set_F = ToSeekEmail(group_F)
print "---------------------------------------------"
print "The size of learners is: " + str(len(email_set_F))
ToPrintEmail(course_path + "post++/group_f(non-engaged learners) - NEW.txt", email_set_F)




print "Finished."































