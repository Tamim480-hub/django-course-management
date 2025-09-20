from django.db import models
from django.core.exceptions import ValidationError

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    enrollment_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.department})"

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    hire_date = models.DateField()

    def __str__(self):
        return self.name

    def course_count(self):
        return self.course_set.count()
    course_count.short_description = "Number of Courses"

class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=200)
    credits = models.IntegerField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course_code} - {self.title}"

    def enrolled_students_count(self):
        return self.enrollment_set.count()
    enrolled_students_count.short_description = "Enrolled Students"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField()
    grade = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'course')  # prevent duplicates

    def __str__(self):
        return f"{self.student.name} → {self.course.course_code}"

    def clean(self):

        if Enrollment.objects.filter(student=self.student, course=self.course).exists():
            raise ValidationError("This student is already enrolled in this course.")
