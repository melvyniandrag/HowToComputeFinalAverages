#!/usr/bin/python3

import pandas as pd
import sys

NUM_GRADES_TO_DROP = 2
HW_WEIGHT = 0.7
EXAM_WEIGHT = 0.3

A_CUTOFF =       4.0 * 25
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
grades.columns = grades.columns.str.lower()
grades = grades.fillna(0)
print(grades)
print("#" * 80)

print("#" * 80)
print("this should be all homework grades:")
homework = grades.filter(regex=("homework|assignment|extra"))
print(homework)
print(homework.columns)
print("#" * 80)

print("#" * 80)
extra = grades.filter(regex=("extra"))
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
exams = grades.filter(regex="exam")
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
