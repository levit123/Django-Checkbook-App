from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm


# Create your views here.
def home(request):
    # displays a drop down of account names for the user to choose from
    form = TransactionForm(data=request.POST or None)

    # determines the correct balance sheet to redirect the user to upon submitting form
    if request.method == 'POST':
        pk = request.POST['account']
        return balance(request, pk)

    content = {'form': form}
    return render(request, 'checkbook/index.html', content)


def create_account(request):
    form = AccountForm(data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('index')

    # pulls info filled out in the form and saves it to a variable named "content"
    content = {'form': form}

    return render(request, 'checkbook/CreateNewAccount.html', content)


def balance(request, pk):
    # attempts to pull info from the database; if unable, display an error 404 page in the browser
    account = get_object_or_404(Account, pk=pk)

    # gets a list of transactions from the info pulled above
    transactions = Transaction.Transactions.filter(account=pk)
    current_total = account.initial_deposit
    table_contents = {}

    # iterates through the list of transactions
    for transaction in transactions:
        # if the current transaction the loop is on is a Deposit...
        if transaction.type == 'Deposit':
            current_total += transaction.amount
            table_contents.update({transaction: current_total})
        # otherwise...
        else:
            current_total -= transaction.amount
            table_contents.update({transaction: current_total})

    content = {'account': account, 'table_contents': table_contents, 'balance': current_total}
    return render(request, 'checkbook/BalanceSheet.html', content)

def transaction(request):
    form = TransactionForm(data=request.POST or None)

    # when user adds a new transaction, they are redirected to the balance sheet
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            pk = request.POST['account']
            form.save()
            return balance(request, pk)

    # pulls info filled out in the form and saves it to a variable named "content"
    content = {'form': form}

    return render(request, 'checkbook/AddTransaction.html', content)