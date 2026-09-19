# from django.contrib import admin

# # Register your models here.
from django.contrib import admin
from .models import (
    User,
    Department,
    Role,
    Request,
    CreatedRequest,
    WorkflowStep,
    TemporaryWorkflowStep,
    ActualWorkflowStep,
    RegularBillsRequestDetails,
    PurchaseRequestDetails,
    LeaveRequestDetails,
)

admin.site.register(User)
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(Request)
admin.site.register(CreatedRequest)
admin.site.register(WorkflowStep)
admin.site.register(TemporaryWorkflowStep)
admin.site.register(ActualWorkflowStep)
admin.site.register(RegularBillsRequestDetails)
admin.site.register(PurchaseRequestDetails)
admin.site.register(LeaveRequestDetails)