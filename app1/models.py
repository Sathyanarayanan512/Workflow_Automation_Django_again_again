from django.db import models

# Create your models here.
class Department(models.Model):
    dept_name=models.CharField(max_length=50)

class Role(models.Model):
    role_name=models.CharField(max_length=50)

class User(models.Model):
    name=models.CharField(max_length=30)
    username=models.CharField(max_length=50, unique=True, null=False)
    password=models.CharField(max_length=50, null=False)
    role=models.CharField(max_length=50)
    department=models.ForeignKey(Department, on_delete=models.PROTECT)





class Request(models.Model):
    request_name=models.CharField(max_length=50)

class CreatedRequest(models.Model):
    request=models.ForeignKey(Request, on_delete=models.PROTECT)
    request_name=models.CharField(max_length=50)
    user_id=models.IntegerField(null=False)
    user_name=models.CharField(max_length=30)
    created_at=models.DateTimeField(auto_now_add=True)
    workflow_created=models.CharField(max_length=10, default='No')
    status=models.CharField(max_length=20,default='PENDING')

class RegularBillsRequestDetails(models.Model):
    created_request=models.ForeignKey(CreatedRequest, on_delete=models.PROTECT)
    bill_amount=models.DecimalField(max_digits=10,decimal_places=2)

class PurchaseRequestDetails(models.Model):
    created_request=models.ForeignKey(CreatedRequest, on_delete=models.PROTECT)
    amount=models.DecimalField(max_digits=10,decimal_places=2) 

class LeaveRequestDetails(models.Model):
    created_request=models.ForeignKey(CreatedRequest, on_delete=models.PROTECT)
    reason=models.CharField(max_length=40)
    days=models.IntegerField()

class WorkflowStep(models.Model):
    step_no=models.IntegerField(null=True)
    total_steps=models.IntegerField(null=True)
    request=models.ForeignKey(Request, on_delete=models.PROTECT)
    request_name=models.CharField(max_length=50,null=False)
    created_request=models.ForeignKey(CreatedRequest, on_delete=models.PROTECT)
    dept_name=models.CharField(max_length=50)
    approver_id=models.IntegerField()
    approver_name=models.CharField(max_length=30)
    status=models.CharField(max_length=20,default='PENDING')

class TemporaryWorkflowStep(models.Model):
    step_no=models.IntegerField(null=True)
    total_steps=models.IntegerField(null=True)
    request=models.ForeignKey(Request, on_delete=models.PROTECT)
    request_name=models.CharField(max_length=50,null=False)
    created_request=models.ForeignKey(CreatedRequest, on_delete=models.PROTECT)
    dept_name=models.CharField(max_length=50)
    approver_id=models.IntegerField()
    approver_name=models.CharField(max_length=30)
    status=models.CharField(max_length=20,default='PENDING')




class ActualWorkflowStep(models.Model):
    step_no=models.IntegerField(null=True)
    total_steps=models.IntegerField(null=True)
    request=models.ForeignKey(Request, on_delete=models.PROTECT)
    request_name=models.CharField(max_length=50,null=False)
    created_request=models.ForeignKey(CreatedRequest, on_delete=models.PROTECT)
    dept_name=models.CharField(max_length=50)
    approver_id=models.IntegerField()
    approver_name=models.CharField(max_length=30)
    status=models.CharField(max_length=20,default='PENDING')






# class ITDepartment(models.Model):
#     user=models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)
#     role=models.CharField(max_length=50)
# class FinanceDepartment(models.Model):
#     user=models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)
#     role=models.CharField(max_length=50)
# class SalesDepartment(models.Model):
#     user=models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)
#     role=models.CharField(max_length=50)



# class WorkflowStepLog(models.Model):
#     step_no=models.IntegerField()
#     total_steps=models.IntegerField()
#     request=models.ForeignKey(Request, on_delete=models.PROTECT)
#     request_name=models.CharField(max_length=50,null=False)
#     created_request=models.ForeignKey(CreatedRequest, on_delete=models.PROTECT)
#     dept_name=models.CharField(max_length=50)
#     approver_id=models.IntegerField()
#     approver_name=models.CharField(max_length=30)
#     status=models.CharField(max_length=20,default='PENDING')