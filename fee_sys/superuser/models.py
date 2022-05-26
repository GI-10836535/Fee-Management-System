from django.db import models
from django.forms import ModelForm
from django import forms

# Create your models here.

class FeeType(models.Model):
    id = models.AutoField(primary_key=True)
    fee_type = models.CharField(max_length= 50)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.fee_type





class FeeItems(models.Model):
    id = models.AutoField(primary_key=True)
    fee_type = models.ForeignKey(FeeType, on_delete= models.CASCADE)
    fee_items = models.CharField(max_length = 100)
    date_created = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return f'{self.fee_type}- {self.fee_items}'


class FeeDescription(models.Model):
    id = models.AutoField(primary_key=True)
    fee_description = models.CharField(max_length= 100)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.fee_description



class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length= 100)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.currency



class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    branch = models.CharField(max_length= 100)
    member_category = models.CharField(max_length= 100)
    group = models.CharField(max_length= 100)
    subgroup = models.CharField(max_length= 100)
    fee_type = models.ForeignKey(FeeType, on_delete= models.CASCADE)
    fee_description = models.ForeignKey(FeeDescription, on_delete= models.CASCADE)
    fee_items = models.ForeignKey(FeeItems, on_delete= models.CASCADE)
    items_amount = models.CharField(max_length= 100)
    total_amount = models.IntegerField(default=0)
 

    def __str__(self):
        return f'{self.branch}, {self.member_category}, {self.group}, {self.subgroup}, {self.fee_type}, {self.fee_description},'




# class InvoiceType(models.Model):
#     id = models.AutoField(primary_key=True)
#     branch = models.CharField(max_length= 100)
#     member_category = models.CharField(max_length= 100)
#     group = models.CharField(max_length= 100)
#     subgroup = models.CharField(max_length= 100)
#     fee_type = models.ForeignKey(FeeType, on_delete= models.CASCADE)
#     fee_description = models.ForeignKey(FeeDescription, on_delete= models.CASCADE)
 

#     def __str__(self):
#         return f'{self.branch}, {self.member_category}, {self.group}, {self.subgroup}, {self.fee_type}, {self.fee_description},'


# class InvoiceItems(models.Model):
#     id = models.AutoField(primary_key=True)
#     fee_items = models.ForeignKey(FeeItems, on_delete= models.CASCADE)
#     items = models.CharField(max_length= 100, default="Home")
#     items_amount = models.IntegerField(default=0)
#     total_amount = models.IntegerField(default=0)

#     def __str__(self):
#         return f"{self.total_amount}"




# class Invoice(models.Model):
#     id = models.AutoField(primary_key=True)
#     branch = models.ForeignKey(InvoiceType, on_delete= models.CASCADE)
#     member_category = models.ForeignKey(InvoiceType, on_delete= models.CASCADE)
#     group = models.ForeignKey(InvoiceType, on_delete= models.CASCADE)
#     subgroup = models.ForeignKey(InvoiceType, on_delete= models.CASCADE)
#     fee_type = models.ForeignKey(InvoiceType, on_delete= models.CASCADE)
#     fee_description = models.ForeignKey(InvoiceType, on_delete= models.CASCADE)
#     fee_items = models.ForeignKey(InvoiceItems, on_delete= models.CASCADE)
#     items = models.ForeignKey(InvoiceItems, on_delete= models.CASCADE)
#     items_amount = models.ForeignKey(InvoiceItems, on_delete= models.CASCADE)
#     total_amount = models.ForeignKey(InvoiceItems, on_delete= models.CASCADE)

#     def __str__(self):
#         return f'{self.branch}, {self.member_category}, {self.group}, {self.subgroup}, {self.fee_type}, {self.fee_description},'








class SelectedValue(models.Model):
    id = models.AutoField(primary_key=True)
    selected_value = models.IntegerField(null=True, default=0)

    def __str__(self):
        return f"{self.selected_value}"






# class CreateInvoiceForm(ModelForm):

#      class Meta:
#         model = Invoice
#         fields = ['branch','member_category','group','subgroup','fee_type','fee_description','items_amount']

#         widgets = {
#             # from API
#         'branch': forms.ChoiceField(),
#         'member_category': forms.ChoiceField(),
#         'group': forms.ChoiceField(),
#         'subgroup': forms.ChoiceField(),

#         'fee_type': forms.ChoiceField(choices = FeeType.objects.all(),  label="", initial='Choose fee type/category', widget=forms.Select(), required=True),
#         'fee_description': forms.ChoiceField(),
#         'items_amount': forms.TextInput(attrs={'placeholder': 'Enter amount...'}),
#             }  










# logo and signature upload

class SetInvoiceDetails(models.Model):
    id = models.AutoField(primary_key=True)
    signers_name = models.CharField(max_length= 500)
    signature = models.ImageField(blank=True, null=True, upload_to='signature-uploads/', default='')
    logo = models.ImageField(blank=True, null=True, upload_to='logo-uploads/', default='')
    contact = models.CharField(max_length= 500)
    email = models.EmailField(max_length= 500)


    def __str__(self):
        return f'{self.signers_name}, {self.contact}'






class AssignPaymentDuration(models.Model):
    id = models.AutoField(primary_key=True)
    branch = models.CharField(max_length= 100)
    member_category = models.CharField(max_length= 100)
    group = models.CharField(max_length= 100)
    subgroup = models.CharField(max_length= 100)
    member = models.CharField(max_length= 100, default= None)
    fee_type = models.ForeignKey(FeeType, on_delete= models.CASCADE)
    total_invoice = models.IntegerField(blank=True)
    install_days = models.IntegerField(blank=True, default=0)
    install_amount = models.IntegerField()
    set_date =  models.DateField(blank=True)
    start_date =  models.DateField(blank=True)
    end_date =  models.DateField(blank=True)
    account_status = models.CharField(max_length= 100)

    def __str__(self):
        return f'{self.branch}, {self.member_category}, {self.group}, {self.subgroup}, {self.total_invoice}'
      