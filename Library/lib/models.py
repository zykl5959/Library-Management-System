from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=200)
    ISBN=models.CharField(max_length=10)

class AUTHORS(models.Model):
    Name=models.CharField(max_length=100)


class Book_AUTHORS(models.Model):
    Authors_id=models.ForeignKey(AUTHORS,on_delete=models.CASCADE)
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)

class BORROWER(models.Model):
    ssn=models.CharField(max_length=15)
    Bname=models.CharField(max_length=100)
    Address=models.CharField(max_length=100)
    Phone=models.CharField(max_length=100)

class BOOK_LOANS(models.Model):
    ISBN=models.ForeignKey(Book,on_delete=models.CASCADE)
    Card_id=models.ForeignKey(BORROWER,on_delete=models.CASCADE)
    Date_out=models.DateTimeField(max_length=20)
    Due_date=models.DateTimeField(max_length=20)
    Date_in=models.DateTimeField(max_length=20)

class FINES(models.Model):
    Loan_id=models.ForeignKey(BOOK_LOANS,on_delete=models.CASCADE)
    Fine_amt=models.DecimalField(max_digits=5,decimal_places=2)
    Paid=models.BooleanField(max_length=10)
