/*
 * Author: 57027
 * Date: March 2020
*/

/*
* Creation of all students' instances which
* they are studying Computer Science.
*
* computing: course name, Computer Science.
*/
computing(mary).
computing(pat).
computing(bob).
computing(tony).

/*
 * Data:
 * Indicating all scores of each student.
 * e1: Exam 1, cs1111.
 * e2: Exam 2, cs1112.
 * e3: Exam 3, cs1113.
 * cw: Coursework.
 * prog: Programming.
 * score(name of student,score type,score).
*/
score(mary,e1,60).
score(mary,e2,65).
score(mary,e3,70).
score(mary,cw,75).
score(mary,prog,70).

score(pat,e1,75).
score(pat,e2,80).
score(pat,e3,63).
score(pat,cw,80).
score(pat,prog,25).

score(bob,e1,40).
score(bob,e2,50).
score(bob,e3,80).
score(bob,cw,63).
score(bob,prog,85).

score(tony,e1,20).
score(tony,e2,80).
score(tony,e3,90).
score(tony,cw,57).
score(tony,prog,65).

/*
 * Indicate if a student passes the year.
 * Student: a parameter storing the student's name.
*/
prog_pass(Student) :-
    score(Student,prog,ProgScore),
    ProgScore >= 30.

/*
 * Indicate if a student needs to resit an exam.
 * Student: a parameter storing a student's name.
 * Exam: a parameter storing a symbol representing an exam (e1,e2 or e3)
 * in the KB.
*/
resit(Student,Exam) :-
    score(Student,Exam,ExamScore),
    (Exam =  e1 ; Exam = e2 ; Exam = e3),
    ExamScore < 30.

/*
 * Indicate if a student fails the year.
 * Student: a parameter storing a student's name.
*/
fail(Student) :-
    findall(E,resit(Student,E),Res),
    (length(Res,2) ; length(Res,3)). % failing at least 2 exams resulting in failing the entire year

/*
 * Indicate if a student passes the year.
 * Student: a parameter storing a student's name.
*/
pass(Student) :-
    prog_pass(Student),
    score(Student,e1,Exam1),
    score(Student,e2,Exam2),
    score(Student,e3,Exam3),
    \+fail(Student),
    Sum is Exam1 + Exam2 + Exam3,
    ExamAvg is Sum/3,
    score(Student,cw,CwScore),
    (
        CwScore < 50 -> ExamAvg >= 50 ;
        ExamAvg >= 40
    ).
