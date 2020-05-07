from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone;

from django.template import loader
from django.db.models import Sum
from .models import Book,Book_AUTHORS,AUTHORS,BOOK_LOANS,BORROWER,FINES


def index(request):
    template = loader.get_template('lib/index.html')
    return HttpResponse(template.render(None, request))

def searchbook(request):
    template = loader.get_template('lib/searchbook.html')
    return HttpResponse(template.render(None,request))


def searchbookresult(request):
    template=loader.get_template('lib/searchbookresult.html')
    mytext=request.POST['text']

    content = {}

    Booklist1 = Book.objects.filter(title__icontains=mytext);
    Booklist2=Book.objects.filter(ISBN__icontains=mytext);
    Authorlist=AUTHORS.objects.filter(Name__icontains=mytext);
    #
    Book_AUTHORSList=Book_AUTHORS.objects.filter(Authors_id_id__in=[q.id for q in Authorlist]);
    Booklist3=Book.objects.filter(id__in=[r.ISBN_id for r in Book_AUTHORSList]);
    #

    Booklist=Booklist1|Booklist2|Booklist3;
    content['books']=Booklist;
    content['authors'] = getAuthors(content['books']);
    content['isAvail']=isAvail(content['books'])
    content['total']=zip(content['books'],content['authors'],content['isAvail']);
    return HttpResponse(template.render(content,request))


def getAuthors(book):
    authors = [];
    for b in book:
        temp1 = Book_AUTHORS.objects.filter(ISBN_id=b.id);
        temp2 = ''
        for t in range(len(temp1)):
            temp3 = AUTHORS.objects.get(id=temp1[t].Authors_id_id)
            if t != 0:
                temp2+=' , '
            temp2 = temp2+temp3.Name;

        authors.append(temp2)

    return authors;


def isAvail(book):
    isAvail=[];
    for b in book:
        if BOOK_LOANS.objects.filter(ISBN_id=b.id).filter(Date_in=None).exists():
            isAvail.append(False);
        else:
            isAvail.append(True)
    return  isAvail;



def checkout(request,book_id):
    book = Book.objects.filter(id=book_id)[0];
    context={'book':book};
    template = loader.get_template('lib/checkout.html')
    return HttpResponse(template.render(context,request))

def checkoutresult(request,book_id):
    card_id = request.POST['card_id']
    isBorrowed=BOOK_LOANS.objects.filter(ISBN_id=book_id).filter(Date_in=None).exists();
    if isBorrowed:
        messages.add_message(request, messages.ERROR, "You can't borrower the book because book is not available")
        return redirect('/')
    else:
        hasBorrower = BORROWER.objects.filter(id=card_id).exists()
        if hasBorrower and len(BOOK_LOANS.objects.filter(Card_id_id=card_id).filter(Date_in=None))<=2:
            BOOK_LOANS.objects.create(Card_id_id=card_id,ISBN_id=book_id,Date_out=timezone.now(),Due_date=timezone.now() + timezone.timedelta(days=14),Date_in=None)
            borrower=BORROWER.objects.filter(id=card_id)[0];
            book=Book.objects.filter(id=book_id)[0];
            context={'borrower':borrower,'book':book}
            template = loader.get_template('lib/checkoutresult.html')
            return HttpResponse(template.render(context,request))
        elif hasBorrower:
            messages.add_message(request, messages.INFO, "You can't borrower the book because you already borrow 3 books")
            return redirect('/')
        else:
            messages.add_message(request, messages.INFO, "You can't borrower the book because you are not yet a borrower")
            return redirect('/')

def checkin(request):
    template = loader.get_template('lib/checkin.html')
    return HttpResponse(template.render(None,request))
def checkinresult(request):
    text = request.POST['text']
    option=request.POST['inlineRadioOptions']

    content = {};
    if(option=="BOOKS.book_id"):
        book_loan=BOOK_LOANS.objects.filter(ISBN_id=text,Date_in=None)
    elif(option == "BORROWER.card_no"):
            book_loan = BOOK_LOANS.objects.filter(Card_id_id=text,Date_in=None)
    elif (option == "BORROWER name"):
        borrowers=BORROWER.objects.filter(Bname__icontains=text);
        book_loan=[];
        for b in borrowers:
            book_loansub=BOOK_LOANS.objects.filter(Card_id_id=b.id,Date_in=None)
            for q in book_loansub:
                book_loan.append(q);
    template = loader.get_template('lib/checkinresult.html')
    content['book_loan'] = book_loan;
    return HttpResponse(template.render(content, request))


def checkinfinish(request):
    book_idCheck = request.POST.getlist('book_id')
    if book_idCheck:
        for b in book_idCheck:
            BOOK_LOANS.objects.filter(ISBN=b).update(Date_in=timezone.now())
        messages.add_message(request, messages.INFO, "Check in succeed!");
        return redirect('/')
    else:
        return HttpResponse("You didn't select at all");


def createborrower(request):
    template = loader.get_template('lib/createborrower.html')
    return HttpResponse(template.render(None, request));

def newborrower(request):
    ssn = request.POST['ssn']
    name=request.POST['name']
    address=request.POST['address']
    phone=request.POST['phone']
    if ssn and name and address:
        if BORROWER.objects.filter(ssn=ssn).exists():
            return HttpResponse("Your SSN has been used, try another one ");
        else:
            if BORROWER.objects.filter(ssn=ssn).exists():
                return HttpResponse("SSN has already taken");
            else:
                BORROWER.objects.create(ssn=ssn, Bname=name, Address=address,Phone=phone)
                return HttpResponse("Create new Borrower");
    else:
        return HttpResponse("You haven't enter all fields");

def updatefine(request):
    book_loan=BOOK_LOANS.objects.all();
    for b in book_loan:
        fine=FINES.objects.filter(Loan_id_id=b.id).exists();
        if not fine:
            if (not b.Date_in and timezone.now() > b.Due_date):
                FINES.objects.create(Fine_amt=0.25 * ((timezone.now() - b.Due_date).days + 1), Paid=False,
                                     Loan_id_id=b.id);
            if ((b.Date_in and b.Date_in > b.Due_date)):
                FINES.objects.create(Fine_amt=0.25 * ((b.Date_in - b.Due_date).days + 1), Paid=False, Loan_id_id=b.id);
        else:
            if not FINES.objects.get(Loan_id_id=b.id).Paid:
                FINES.objects.filter(Loan_id_id=b.id).update(Fine_amt=0.25 * ((timezone.now() - b.Due_date).days + 1))
    return HttpResponse("Update fine finish");

def showfine(request):
    fine = FINES.objects.filter(Paid=False);
    book_loan=[]
    for f in fine:
        bl=BOOK_LOANS.objects.get(id=f.Loan_id_id);
        book_loan.append(bl)
    total = zip(fine, book_loan);
    template = loader.get_template('lib/showfine.html')
    finebycardid=FINES.objects.values('Loan_id__Card_id').filter(Paid=False).annotate(Sum('Fine_amt'));
    book_loans=[];
    card_id=[];
    amount=[];

    for f2 in finebycardid:
        bl = BOOK_LOANS.objects.filter(Card_id=f2['Loan_id__Card_id']).first();
        book_loans.append(bl);
        card_id.append(f2['Loan_id__Card_id']);
        amount.append(f2['Fine_amt__sum']);

    total2 = zip (book_loans,card_id,amount);
    context={'total':total,'total2':total2}
    return HttpResponse(template.render(context, request));



def makepaymentbyloanid(request,loan_id):
    book_loan=BOOK_LOANS.objects.get(id=loan_id);
    if book_loan.Date_in:
        fine=FINES.objects.get(Loan_id_id=book_loan.id)
        fine.Paid=True;
        fine.save();
        return HttpResponse("Succeed in making payment");
    else:
        return HttpResponse("Can't pay because not yet return the book");
    # return HttpResponse(template.render(None, request));

def makepaymentbycardid(request,card_id):
    book_loan = BOOK_LOANS.objects.filter(Card_id=card_id);
    if canpay(book_loan):
        for bl in book_loan:
            fine = FINES.objects.filter(Loan_id_id=bl.id).filter(Paid=False);
            if fine:
                for f in fine:
                        f.Paid=True;
                        f.save();
        return HttpResponse("We pay it off");
    else:
        return HttpResponse("Can't pay because not yet return all your  fined (all the expire book)books");

def canpay(book_loan):
    for bl in book_loan:
        if not bl.Date_in and timezone.now()>bl.Due_date:
            return False;
    return True;