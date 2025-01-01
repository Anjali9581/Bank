from django.shortcuts import render , HttpResponse ,redirect
from .forms import Bankform
from .models import Bank
from django.core.mail import send_mail
from django.conf import settings
import random
from decimal import Decimal
from django.db.models import Q


from django.contrib.sessions.models import Session

# Create your views here.
def index(req):
    return render(req,'index.html')




def acc_creation(request):
    form = Bankform()
    # print(form)
    if request.method == "POST":
        form = Bankform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            print("success")
        return redirect('acc_creation')
    context = {
        'form':form
    }
    return render(request,'acc_creation.html',context)

otp_storage={}
def otp(request):
    val = False
    banks = Bank.objects.all()
    bank_numbers = [bank.bank_number for bank in banks]
    print(bank_numbers) 
    if 'otp_send' in request.POST:
        if request.method=='POST':
          acc = request.POST.get('number')
          try:
            banks = Bank.objects.get(bank_number=acc)
            email = banks.email
            print(acc)

            otp = random.randint(1000, 9999)
            request.session['otp'] = otp
          except Exception as e:
              return render(request,'otp.html',{'error':'Account number do not match'})
        try:
            send_mail(
                "Thanks for Registration",   # Subject
                f"Your OTP is {otp}",       # Body
                settings.EMAIL_HOST_USER,  
                [email],  
                fail_silently=False,
            )
            # Store OTP using the email as the key
            otp_storage[email] = otp  
            print(otp)
            print(otp_storage)
            # return HttpResponse("Thank you! Email sent successfully!")
            val = True
            print("hello")
        except Exception as e:
            return HttpResponse(f"Error sending email: {e}")

    elif  "verify" in request.POST:
            print("otp_send")
            email = request.POST.get('email')
            acc = request.POST.get('number')
            entered_otp = ''.join([request.POST.get(f'otp_{i}') for i in range(4)])  # Combine individual OTP inputs
            
            # Check if email and OTP were provided
            if not acc or  email or not entered_otp :
                return render(request, 'otp.html', {'error': "Account  or OTP not provided."})

            # Retrieve stored OTP using the provided email
            stored_otp = request.session.get('otp')
            stored_email = request.session.get('email')

            print(stored_otp)
            print(stored_email)
            
            # Debugging: Print stored and entered OTPs
            print(f"Stored OTP: {stored_otp}, Entered OTP: {entered_otp}")

            if stored_otp and str(stored_otp) == entered_otp:
                del request.session['otp']  # Remove OTP after successful verification
                return redirect('pin')
            else:
                return render(request, 'otp.html', {'error': "Invalid OTP. Please try again."})
                
            
    context ={
        'bank_numbers': bank_numbers,
        'val':val
    }   
    return render(request, 'otp.html',context)

def pin(request):
    if request.method=='POST':
        number=request.POST['account']
        pin=request.POST['pin']
        pin1=request.POST['pin1']
        try:
            account=Bank.objects.get(bank_number=number)
            if pin==pin1:
                account.Pin_No=pin
                account.save()
                return render(request,'pin_gen.html',{'message':'Pin Generated Successfully!😊😊😊😊..'})
            else:
                print('PIN does not match')
            return render(request,'pin_gen.html',{'error':'PIN do not match'})
        except Bank.DoesNotExist:
            print('Account not Found')
            return render(request,'pin_gen.html',{'error':'Account number do not match'})
        
    return render(request,'pin_gen.html')
    

def deposit(request):
    if request.method=='POST':
        account_number=request.POST['account']
        amount=request.POST['amount']
        pin=request.POST['pin']
        print(account_number)
        print(amount)
        print(pin)
        
        try:
           account=Bank.objects.get(Pin_No=pin)
        except:
            return render(request,'deposit.html',{'error':'Please Enter the valid pin'})
        try:
            account=Bank.objects.get(bank_number=account_number,Pin_No=pin)
            print(account)
            amount = int(amount)
            if amount >= 1:
                account.Balance=account.Balance+amount
                account.save()
                print(f'Amount {amount} deposited Successfully')
                return render(request,'deposit.html',{'message':f'Amount {amount} /- Deposit Successfully!..😊😊'})
            else:
                print('ENTER VALID AMOUNT')
                return render(request,'deposit.html',{'error':'Enter Valid Amount'})
        except Bank.DoesNotExist:
            print('Account Not Found')
            return render(request,'deposit.html',{'error':'Enter Valid Amount number '})
    return render(request,'deposit.html')
def withdraw(request):
    if request.method=='POST':
        account_number=request.POST['account']
        amount=request.POST['amount']
        pin=request.POST['pin']
        # try:
        #    account=Bank.objects.get(Pin_No=pin)
        # except:
        #     return render(request,'withdraw.html',{'error':'Please Enter the valid pin'})
        try:
            account=Bank.objects.get(bank_number=account_number)
            try:
              account=Bank.objects.get(Pin_No=pin)
            except:
                return render(request,'withdraw.html',{'error':'Please Enter the valid pin'})
            amount = int(amount)
            if amount<=account.Balance and amount >= 1:
                account.Balance=account.Balance - amount
                account.save()
                print('Amount withdrwal Successfully')
                return render(request,'withdraw.html',{'message':f'Amount {amount}/- withdrwal Successfully !😊😊..'})
            else:
                print('Insuffincent Balance')
                return render(request,'withdraw.html',{'error':'Insuffincent Balanace'})
        except Bank.DoesNotExist:
            print('Account Not Found')
            return render(request,'withdraw.html',{'error':'Account Not Found'})
       
    return render(request,'withdraw.html')


def transfer(request):
    if request.method == 'POST':
        account_number1 = request.POST['account1']
        account_number2 = request.POST['account2']
        amount=request.POST['amount']
        pin = request.POST['pin']
        print(account_number1)
        print(account_number2)
        # Convert amount to Decimal
        try:
            amount = request.POST['amount']
        except:
            return render(request, 'transfer.html', {'error': 'Please Enter a Valid Amount'})
        try:
            # Attempt to convert amount to Decimal
            amount = Decimal(amount)
            if amount <= 0:
                return render(request, 'transfer.html', {'error': 'Enter an Amount Greater Than 0'})
        except :
            return render(request, 'transfer.html', {'error': 'Please Enter a Valid Amount'})
        # Check if the amount is greater than 0
        amount = int(amount)
        if amount <= 0:
            return render(request, 'transfer.html', {'error': 'Enter an Amount Greater Than 0'})

        # Verify the sender's account
        try:
            sender_account = Bank.objects.get(bank_number=account_number1)
            print(sender_account)
            # Ensure the sender has sufficient balance
            if sender_account.Balance < Decimal(amount):
                 return render(request, 'transfer.html', {'error': 'Insufficient Balance'})
            try:
                receiver_account = Bank.objects.get(bank_number=account_number2)
                print(receiver_account)
                
                # Perform the transfer
                # sender_account.Balance -= Decimal(amount)
                # receiver_account.Balance += Decimal(amount)

                try :
                    Bank.objects.get(bank_number=account_number1)
                    try:
                        account=Bank.objects.get(Pin_No=pin)
                    except:
                            return render(request,'transfer.html',{'error':'Please Enter the valid pin'})
                    
                   
                    sender_account.Balance -= Decimal(amount)
                    receiver_account.Balance += Decimal(amount)
 
                # Save updated balances
                    sender_account.save()
                    receiver_account.save()

                    return render(request, 'transfer.html', {'message': f'Amount {amount}/- Transferred Successfully!..😊😊😊'})
                except:
                    return render(request,'transfer.html', {'error': 'Insufficient pin'})
                
            except Bank.DoesNotExist:
                return render(request, 'transfer.html', {'error': 'Receiver Account Not Found'})
        # else:
            # return render(request, 'transfer.html', {'error': 'Insufficient Balance'})
        except Bank.DoesNotExist:
            return render(request, 'transfer.html', {'error': 'Sender Account Not Found'})

    return render(request, 'transfer.html')
def details(request):
    data=Bank.objects.all()
    if request.method=='POST':
        search=request.POST.get('search')
        print('search')
        data=Bank.objects.filter(Q(Name__icontains=search)|Q(Mobile_no__icontains=search))
    context={
        'data':data
    }
    return render(request,'bankdetails.html',context)