from django import forms
from .models import Transactions

class TransactionForm(forms.ModelForm):
    class Meta:
        model= Transactions
        fields= ['amount', 'transaction_type']
    
    def __init__(self, *args, **kwargs):
        self.user_account= kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled= True
        self.fields['transaction_type'].widget= forms.HiddenInput()

    def save(self, commit=True):
        self.instance.account= self.user_account
        self.instance.balance_after_transaction= self.user_account.balance
        return super().save()
    
class Deposit(TransactionForm):
  # def clean_fieldName(self)
    def clean_amount(self): # built-in method
        min_deposit= 100
        amount= self.cleaned_data.get('amount')
        if amount<min_deposit:
            raise forms.ValidationError(
                f'You need to deposite at least {min_deposit} BDT'
            )
        return amount
    
class Withdraw(TransactionForm):
    def clean_amount(self):
        account= self.user_account
        balance= account.balance
        min_withdraw= 500
        max_withdraw= 20000
        amount= self.cleaned_data.get('amount')
        if amount<min_withdraw:
            raise forms.ValidationError(
                f'You need to withdraw at least {min_withdraw} BDT'
            )
        elif amount>max_withdraw:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw} BDT'
            )
        elif amount>balance:
            raise forms.ValidationError(
                f'You have {balance} BDT in your account. '
                'You can\'t withdraw more than your account balance'
            )
        return amount
    
class LoanRequest(TransactionForm):
    def clean_amount(self):
        amount= self.cleaned_data.get('amount')
        return amount
