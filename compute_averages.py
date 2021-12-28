#!/usr/bin/python3

""""
GRADE COMPUTER

Run like this:
./compute_averages.py   grades.csv

The grades.csv is downloadable from blackboard.

See CUTOFFS below. This script takes the grades from the semester and turns them into 
a letter as per NJCU guidelines:

https://www.njcu.edu/directories/offices-centers/registrar/grading-system

( file was there as of DEC-28-2021 )


Grading logic is as follows:
1. Add all homework grades.
2. Assume you planned to drop NUM_GRADES_TO_DROP at the end of semester
3. Take extra credit grades and add them to the homework subtotal.
4. Plan to drop an extra # of grades equal to the # of Extra credits.
5. From the list of homework and extra credit, drop NUM_GRADES_TO_DROP + N_EXTRA_CREDIT
6. Multiply by HW_WEIGHT. This is the homework subtotal.
7. Average the exams. However many there are - maybe you gave midterm, maybe not.
8. Multiply exam avg by EXAM_WEIGHT. This is the exam subtotal.
9. Add homework and exam subtotals. This is final score.
10. Convert number into letter. 


This code prints stuff out along the way throughout the computation for inspection.

Then enter grades in gothicnet and go on vacation!

NOTE:
 * for eAsE oF HaNDLinG column names, we convert column names to .lower() before parsing the data.
 * You might have some empty data in the csv. The NaN values will ruin the computation. They are replaced by 0 in the code. 
   Read ahead to see where.
"""


import pandas as pd
import sys


# EDIT THESE VARIABLES
NUM_GRADES_TO_DROP = 2 # how many homework grades should we forgive?
HW_WEIGHT = 0.8        # percent weight for hw
EXAM_WEIGHT = 0.2      # percent weight for exam
HW_COLUMN_NAME_REGEX = "homework|assignment|extra"  # what did you name the homeworks in blackboard? Use this regex to extract them
EXTRA_CREDIT_COL_NAME_REGEX = "extra"               # what did you name extra credits in blackboard? Use this regex to extract them
EXAM_COL_NAME_REGEX = "exam"                        # what did you name exams in blackboard?
# DO NOT EDIT BELOW UNLESS YOURE SURE


A_CUTOFF =       3.9 * 25 # NJCU Says you get an A for a 4.0 but I have some students with 3.95 who were very good. I think they get A.
A_MINUS_CUTOFF = 3.7 * 25
B_PLUS_CUTOFF =  3.3 * 25
B_CUTOFF =       3.0 * 25
B_MINUS_CUTOFF = 2.7 * 25
C_PLUS_CUTOFF =  2.3 * 25
C_CUTOFF =       2.0 * 25
C_MINUS_CUTOFF = 1.7 * 25
D_CUTOFF =       1.0 * 25
F_CUTOFF =       0


def number_to_letter(grade_as_number):
    """
    This is my understanding of the grading guidelines at NJCU. 
    Modify as you see fit.
    """
    if(grade_as_number >= A_CUTOFF):
        return "A"
    elif (grade_as_number >= A_MINUS_CUTOFF):
        return "A-"
    elif (grade_as_number >= B_PLUS_CUTOFF):
        return "B+"
    elif (grade_as_number >= B_CUTOFF):
        return "B"
    elif (grade_as_number >= B_MINUS_CUTOFF):
        return "B-"
    elif (grade_as_number >= C_PLUS_CUTOFF):
        return "C+"
    elif (grade_as_number >= C_CUTOFF):
        return "C"
    elif (grade_as_number >= C_MINUS_CUTOFF):
        return "C-"
    elif (grade_as_number >= D_CUTOFF):
        return "D"
    else:
        return "F"

grades = pd.read_csv(sys.argv[1])
print("#" * 80)
print("this should be the full data frame:")
grades.columns = grades.columns.str.lower() # make col names lower case for ease of handling.
grades = grades.fillna(0) # did you forget to enter a 0 for an assignment a student didnt complete? It will be a NaN in the CSV - lets make it a 0
print(grades)
print("#" * 80)

print("#" * 80)
print("this should be all homework grades:")
homework = grades.filter(regex=(HW_COLUMN_NAME_REGEX))
print(homework)
print(homework.columns)
print("#" * 80)

print("#" * 80)
extra = grades.filter(regex=(EXTRA_CREDIT_COL_NAME_REGEX))
N_EXTRA_CREDIT = extra.columns.size
print("Detected this many extra credits: " + str(N_EXTRA_CREDIT))
print("#" * 80)


print("#" * 80)
print("sorting homework grades...")
values_to_sort = homework.values
values_to_sort.sort(axis=1)
values_to_sort = values_to_sort[:,::-1]
sorted_homework = pd.DataFrame(values_to_sort)
print(sorted_homework)
print("#" * 80)

print("#" * 80)
print("dropping low grades...")
filtered_homeworks = sorted_homework.iloc[:,:-1*(NUM_GRADES_TO_DROP + N_EXTRA_CREDIT)]
print(filtered_homeworks)
print("#" * 80)


print("#" * 80)
print("homework averages:")
hw_average = filtered_homeworks.mean(axis=1)
print(hw_average)
print("#" * 80)

print("#" * 80)
print("homework values after 0.70 weighting:")
hw_points = hw_average.apply(lambda x: x*HW_WEIGHT)
print(hw_points)
print("#" * 80)

print("#" * 80)
print("these are your exams")
exams = grades.filter(regex=EXAM_COL_NAME_REGEX)
print(exams)
print("#" * 80)

print("#" * 80)
print("exam averages:")
exam_avg = exams.mean(axis=1)
print(exam_avg)
print("#" * 80)

print("#" * 80)
print("exam values after 0.3 weighting:")
exam_points = exam_avg.apply(lambda x: x* EXAM_WEIGHT)
print(exam_points)
print("#" * 80)

print("#" * 80)
print("Generating final scores...")
final_number = hw_points + exam_points
print(final_number)
print("#" * 80)

print("#" * 80)
print("Converting to letter...")
letter = final_number.apply(lambda x: number_to_letter(x))
print(letter)
print("#" * 80)



print("#" * 80)
print("Final scores:")
final = pd.concat([grades["last name"], letter, final_number, hw_points, exam_points], axis=1, keys=["last name", "letter", "final number", "hw", "exam"])
print(final)
print(type(final))
print("#" * 80)
