from django.db import models
from django import forms

# Create your models here.

class Employee(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=6, 
        choices=[('ชาย', 'ชาย'), ('หญิง', 'หญิง')],
        default='ชาย'
    )
    position = models.CharField(max_length=50)
    salary = models.PositiveIntegerField()
    address = models.TextField()
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=30, unique=True)
    birthday = models.DateField()
    religion = models.CharField(
        max_length=20,
        choices=[('พุทธ', 'พุทธ'), ('คริสต์', 'คริสต์'), 
                 ('อิสลาม', 'อิสลาม'), ('อื่นๆ', 'อื่นๆ')],
                 
        default='พุทธ'
	)
    addition_note = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
         return self.firstname


class EmployeeForm(forms.ModelForm):
	class Meta:
		model = Employee
		fields = '__all__'
		labels = {
			'firstname': 'ชื่อ',
			'lastname': 'นามสกุล',
			'gender': 'เพศ',
			'position': 'ตำแหน่งงาน',
			'salary': 'เงินเดือน',
			'address': 'ที่อยู่',
			'email': 'อีเมล',
			'phone': 'โทรศัพท์',
			'birthday': 'วันเกิด',
			'religion': 'ศาสนา',
			'addition_note': 'บันทึกเพิ่มเติม',
		}
		widgets = {
			'gender': forms.RadioSelect(),
			'birthday': forms.DateInput(attrs={'type':'date'}),
			'religion': forms.Select(),
            'address': forms.Textarea(attrs={'rows':'3'}),
            'addition_note': forms.Textarea(attrs={'rows':'3'}),
		}


class Member(models.Model):
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=20)
    security = models.PositiveIntegerField()
    performance = models.PositiveIntegerField()


class MemberForm(forms.ModelForm):
    confirm_pswd = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
    )
    save = forms.BooleanField(required=False)

    class Meta:
        model = Member
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput()
        }
        
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    stock = models.PositiveIntegerField()
    date_add = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} | {self.price} | {self.stock} | {self.date_add}'



class Metricmodel(models.Model):
    logger  = models.PositiveIntegerField()
    vms = models.PositiveIntegerField()

class Metricmodel2(models.Model):
    logger  = models.PositiveIntegerField()
    vms = models.PositiveIntegerField()

'''
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    stock = models.PositiveIntegerField()
    date_add = models.DateField(auto_now_add=True) #ถ้าเป็น True ไม่ปรากฏ input ที่ฟอร์ม (เพราะค่าถูกใส่อัตโนมัติ)
    test = models.TextField(max_length=30, null=True, blank=True)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
           'test': forms.(attrs={'type':'date'})
        }
'''