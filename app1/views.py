from django.shortcuts import render, redirect
from .models import User, Department, Role, Request, CreatedRequest, WorkflowStep, TemporaryWorkflowStep, ActualWorkflowStep, RegularBillsRequestDetails, PurchaseRequestDetails, LeaveRequestDetails
# Create your views here.
def home(request):
    return render(request, 'homepage.html')
def loadregister(request):
    departments=Department.objects.all().values()
    roles=Role.objects.all().values()
    message='Regsiter to create account'
    return render(request, 'userregister.html',{'depts' : departments, 'roles':roles, 'message':message})
def userregister(request):
    nameofuser=request.POST.get('name')
    uname=request.POST.get('username')
    if User.objects.filter(username=uname).exists():
        departments=Department.objects.all().values()
        roles=Role.objects.all().values()
        message='Username already exists'
        return render(request, 'userregister.html',{'depts' : departments, 'roles':roles, 'message':message})
    upass=request.POST.get('password')
    urole=request.POST.get('role')
    udept_id=int(request.POST.get('departmentId'))
    User.objects.create(name=nameofuser, username=uname, password=upass, role=urole, department_id=udept_id)
    return render(request, 'userlogin.html', {'message':'User registered'})
def userlogin(request):
    uname=request.POST.get('username')
    upass=request.POST.get('password')
    try:
        user=User.objects.get(username=uname)
        if uname==user.username:
            if upass==user.password:
                request.session['username']=user.username
                return redirect('loaddashboard')
            else:
                return render(request, 'userlogin.html', {'message':'Incorrect Password'})
    except Exception as e:
        return render(request, 'userlogin.html',{'message':f'Invalid Username-{e}'})
def logout(request):
    request.session.flush()
    return redirect('userlogin')
def loaddashboard(request):
    uname=request.session.get('username')
    try:
        user=User.objects.get(username=uname)
        if user.role=='Admin':
            pending_requests=CreatedRequest.objects.filter(status='PENDING')
            return render(request, 'admindashboard.html',{'pending_requests':pending_requests})
        else:
            return render(request, 'employeedashboard.html',{'user':user})
    except Exception as e:
        return render(request, 'userlogin.html',{'message':f'Invalid Username-{e}'})
def allemployees(request):
    users=User.objects.all().exclude(role='Admin')
    no_of_employees=len(users)
    return render(request, 'allemployees.html', {'users':users,'no_of_employees':no_of_employees})
def addemployee(request):
    return redirect('loadregister')
def loadeditform(request,user_id):
    user=User.objects.get(id=user_id)
    departments=Department.objects.all().values()
    roles=Role.objects.all().values()
    return render(request, 'editform.html', {'user':user, 'depts':departments, 'roles':roles})
def editemployee(request):
    uid=request.POST.get('user_id')
    nameofuser=request.POST.get('name')
    uname=request.POST.get('username')
    upass=request.POST.get('password')
    urole=request.POST.get('role')
    udept_id=int(request.POST.get('departmentId'))
    user=User.objects.get(id=uid)
    user.name=nameofuser
    user.username=uname
    user.password=upass 
    user.role=urole 
    user.department_id=udept_id
    user.save()
    return redirect('loaddashboard')
def deleteemployee(request,user_id):
    user=User.objects.get(id=user_id)
    user.delete()
    return redirect('loaddashboard')
def createdrequests(request,uid):
    created_requests=CreatedRequest.objects.filter(user_id=uid)
    return render(request,'employeerequests.html',{'user_id':uid, 'created_requests':created_requests})
def createrequestform(request,uid):
    requests=list(Request.objects.all())
    return render(request,'createrequestform.html',{'requests':requests,'user_id':uid})
def createrequest(request):
    uid=request.POST.get('user-id')
    nameofuser=User.objects.get(id=uid).name
    request_type=request.POST.get('request-type')
    rid=Request.objects.get(request_name=request_type).id
    CreatedRequest.objects.create(request_id=rid, request_name=request_type, user_id=uid, user_name=nameofuser)
    created_requestid=CreatedRequest.objects.order_by('-created_at').first().id
    if request_type=='Regular Bills Request':
        bill=request.POST.get('bill-amount')
        RegularBillsRequestDetails.objects.create(created_request_id=created_requestid,bill_amount=bill)
    elif request_type=='Purchase Request':
        amt=request.POST.get('amount')
        PurchaseRequestDetails.objects.create(created_request_id=created_requestid,amount=amt)
    elif request_type=='Leave Request':
        leave_reason=request.POST.get('leave-reason')
        no_of_days=request.POST.get('no-of-days')
        LeaveRequestDetails.objects.create(created_request_id=created_requestid,reason=leave_reason, days=no_of_days)
    return redirect('loaddashboard')
def loadgenerateworkflow(request,cr_id):
    workflowsteps=TemporaryWorkflowStep.objects.filter(created_request_id=cr_id)
    uid=request.POST.get('user-id')
    udept=request.POST.get('user-department')
    if uid:
        if udept:
            users=User.objects.filter(id=uid)
        else:
            users=User.objects.filter(id=uid)
    elif udept:
        department_id=Department.objects.get(dept_name=udept).id
        users=User.objects.filter(department=department_id)
    else:
        users=User.objects.all()
    cr=CreatedRequest.objects.get(id=cr_id)
    request_type=cr.request_name
    if request_type=='Regular Bills Request':
        bill_amt=RegularBillsRequestDetails.objects.get(created_request_id=cr_id).bill_amount
        return render(request,'generateworkflow.html',{'workflowsteps':workflowsteps,'users':users,'cr_id':cr_id,'bill_amount':bill_amt})
    elif request_type=='Purchase Request':
        amt=PurchaseRequestDetails.objects.get(created_request_id=cr_id).amount
        return render(request,'generateworkflow.html',{'workflowsteps':workflowsteps,'users':users,'cr_id':cr_id,'amount':amt})
    elif request_type=='Leave Request':
        r=LeaveRequestDetails.objects.get(created_request_id=cr_id).reason
        d=LeaveRequestDetails.objects.get(created_request_id=cr_id).days
        return render(request,'generateworkflow.html',{'workflowsteps':workflowsteps,'users':users,'cr_id':cr_id,'reason':r,'days':d})
def generateworkflowstep(request,uid,cr_id):
    createdrequest=CreatedRequest.objects.get(id=cr_id)
    employee=User.objects.get(id=uid)
    dept_name=Department.objects.get(id=employee.department_id).dept_name
    most_recent=TemporaryWorkflowStep.objects.order_by('-id').first()
    if not (most_recent and most_recent.approver_id==uid):
        TemporaryWorkflowStep.objects.create(request_id=createdrequest.request_id,request_name=createdrequest.request_name,created_request_id=cr_id,dept_name=dept_name,approver_id=uid,approver_name=employee.name)
    return redirect('loadgenerateworkflow', cr_id=cr_id)
def removefromworkflow(request,tw_id,cr_id):
    TemporaryWorkflowStep.objects.get(id=tw_id).delete()
    return redirect('loadgenerateworkflow',cr_id=cr_id)
def finishmakingflow(request,cr_id):
    workflowsteps=TemporaryWorkflowStep.objects.filter(created_request_id=cr_id)
    step=0
    for i in workflowsteps:
        step+=1
        i.step_no=step
        i.save()
        ActualWorkflowStep.objects.create(step_no=step,request_id=i.request_id,request_name=i.request_name,created_request_id=i.created_request_id,dept_name=i.dept_name,approver_id=i.approver_id,approver_name=i.approver_name)
        WorkflowStep.objects.create(step_no=step,request_id=i.request_id,request_name=i.request_name,created_request_id=i.created_request_id,dept_name=i.dept_name,approver_id=i.approver_id,approver_name=i.approver_name)
    ActualWorkflowStep.objects.filter(created_request_id=cr_id).update(total_steps=step)
    WorkflowStep.objects.filter(created_request_id=cr_id).update(total_steps=step)
    workflowsteps.update(total_steps=step)
    CreatedRequest.objects.filter(id=cr_id).update(workflow_created='Yes')
    TemporaryWorkflowStep.objects.all().delete()
    return redirect('loaddashboard')
def viewworkflow(request,cr_id):
    workflowsteps=WorkflowStep.objects.filter(created_request_id=cr_id)
    return render(request,'viewworkflow.html',{'workflowsteps':workflowsteps})
def workrequestsforemployee(request,uid):
    worker=User.objects.get(id=uid)
    cr_id_list=CreatedRequest.objects.filter(status='PENDING').order_by('id').values_list('id',flat=True)
    workrequests=[]
    for i in cr_id_list:
        first_pending_work=ActualWorkflowStep.objects.filter(created_request_id=i).filter(status='PENDING').order_by('step_no').first()
        if first_pending_work and first_pending_work.approver_id==uid:
            workrequests.append(first_pending_work)

    regular_bills_requests=[]
    purchase_requests=[]
    leave_requests=[]
    for i in workrequests:
        if i.request_name=='Regular Bills Request':
            regular_bills_requests.append(i)
        elif i.request_name=='Purchase Request':
            purchase_requests.append(i)
        elif i.request_name=='Leave Request':
            leave_requests.append(i)
    bill_amounts=[]
    amounts=[]
    reasons=[]
    days=[]

    if regular_bills_requests:
        for i in regular_bills_requests:
            bill_amounts.append(RegularBillsRequestDetails.objects.get(created_request_id=i.created_request_id).bill_amount)
    if purchase_requests:
        for i in purchase_requests:
            amounts.append(PurchaseRequestDetails.objects.get(created_request_id=i.created_request_id).amount)
    if leave_requests:
        for i in leave_requests:
            leave_details=LeaveRequestDetails.objects.get(created_request_id=i.created_request_id)
            reasons.append(leave_details.reason)
            days.append(leave_details.days)
    return render(request, 'workrequestsforemployee.html',{'worker':worker,'regular_bills_requests':regular_bills_requests, 'purchase_requests': purchase_requests, 'leave_requests':leave_requests, 'bill_amounts':bill_amounts, 'amounts':amounts, 'reasons':reasons, 'days':days})




    # workrequests=ActualWorkflowStep.objects.filter(status='PENDING').filter(approver_id=uid)
    # worker=User.objects.get(id=uid)
    # # cr_id_list=workrequests.values_list('created_request_id')

    # regular_bills_requests=workrequests.filter(request_name='Regular Bills Request')
    # purchase_requests=workrequests.filter(request_name='Purchase Request')
    # leave_requests=workrequests.filter(request_name='Leave Request')
    # bill_amounts=[]
    # amounts=[]
    # reasons=[]
    # days=[]

    # if regular_bills_requests:
    #     for i in regular_bills_requests:
    #         bill_amounts.append(RegularBillsRequestDetails.objects.get(created_request_id=i.created_request_id).bill_amount)
    # if purchase_requests:
    #     for i in purchase_requests:
    #         amounts.append(PurchaseRequestDetails.objects.get(created_request_id=i.created_request_id).amount)
    # if leave_requests:
    #     for i in leave_requests:
    #         reasons.append(LeaveRequestDetails.objects.get(created_request_id=i.created_request_id).reason)
    #         days.append(LeaveRequestDetails.objects.get(created_request_id=i.created_request_id).days)
    # return render(request, 'workrequestsforemployee.html',{'worker':worker,'regular_bills_requests':regular_bills_requests, 'purchase_requests': purchase_requests, 'leave_requests':leave_requests, 'bill_amounts':bill_amounts, 'amounts':amounts, 'reasons':reasons, 'days':days})




    # workrequests=ActualWorkflowStep.objects.filter(status='PENDING').filter(approver_id=uid)
    # worker=User.objects.get(id=uid)
    # # cr_id_list=workrequests.values_list('created_request_id')

    # regular_bills_requests=workrequests.filter(request_name='Regular Bills Request')
    # purchase_requests=workrequests.filter(request_name='Purchase Request')
    # leave_requests=workrequests.filter(request_name='Leave Request')
    # regular_bills_requests_details={}
    # purchase_requests_details={}
    # leave_requests_details={}

    # if regular_bills_requests:
    #     for i in regular_bills_requests:
    #         regular_bills_requests_details[i]=RegularBillsRequestDetails.objects.get(created_request_id=i.created_request_id)
    # if purchase_requests:
    #     for i in purchase_requests:
    #         purchase_requests_details[i]=PurchaseRequestDetails.objects.get(created_request_id=i.created_request_id)
    # if leave_requests:
    #     for i in leave_requests:
    #         leave_requests_details[i]=LeaveRequestDetails.objects.get(created_request_id=i.created_request_id)
    # return render(request, 'workrequestsforemployee.html',{'worker':worker,'regular_bills_requests_details':regular_bills_requests_details, 'purchase_requests_details': purchase_requests_details, 'leave_requests_details':leave_requests_details})



    # workrequests=ActualWorkflowStep.objects.filter(status='PENDING').filter(approver_id=uid)
    # worker=User.objects.get(id=uid)
    # # cr_id_list=workrequests.values_list('created_request_id')

    # regular_bills_requests=workrequests.filter(request_name='Regular Bills Request')
    # purchase_requests=workrequests.filter(request_name='Purchase Request')
    # leave_requests=workrequests.filter(request_name='Leave Request')
    # bill_amounts=[]
    # amounts=[]
    # leave_details=[]
    # total_bar = 0
    # total_pr = 0
    # total_lr = 0
    # if regular_bills_requests:
    #     for i in regular_bills_requests:
    #         bill_amounts.append(RegularBillsRequestDetails.objects.get(created_request_id=i.created_request_id))
    #     total_bar=len(bill_amounts)
    # if purchase_requests:
    #     for i in purchase_requests:
    #         amounts.append(PurchaseRequestDetails.objects.get(created_request_id=i.created_request_id))
    #     total_pr=len(amounts)
    # if leave_requests:
    #     for i in leave_requests:
    #         leave_details.append(LeaveRequestDetails.objects.get(created_request_id=i.created_request_id))
    #     total_lr=len(leave_details)
    # return render(request, 'workrequestsforemployee.html',{'worker':worker,'regular_bills_requests':regular_bills_requests, 'total_bar':range(total_bar), 'purchase_requests': purchase_requests, 'total_pr':range(total_pr), 'leave_requests':leave_requests, 'total_lr':range(total_lr), 'bill_amounts':bill_amounts, 'amounts':amounts, 'leave_details':leave_details})



    # workrequests=ActualWorkflowStep.objects.filter(approver_id=uid)
    # # cr_id_list=workrequests.values_list('created_request_id')

    # regular_bills_requests=workrequests.filter(request_name='Regular Bills Request')
    # purchase_requests=workrequests.filter(request_name='Purchase Request')
    # leave_requests=workrequests.filter(request_name='Leave Request')
    # if regular_bills_requests or purchase_requests:
    #     bill_amounts=[]
    #     amounts=[]
    #     if regular_bills_requests:
    #         for i in regular_bills_requests:
    #             bill_amounts.append(RegularBillsRequestDetails.objects.get(created_request_id=i.created_request_id))
    #     else:
    #         for i in purchase_requests:
    #             amounts.append(PurchaseRequestDetails.objects.get(created_request_id=i.created_request_id))
    #     return render(request,'workrequestsforFinance.html',{'workrequests':regular_bills_requests, 'bill_amounts':bill_amounts, 'amounts':amounts})
    # elif leave_requests:
    #     leave_details=[]
    #     for i in leave_requests:
    #         leave_details.append(LeaveRequestDetails.objects.get(created_request_id=i.created_request_id))
    #     return render(request,'workrequestsforemployee.html',{'workrequests':workrequests, 'leave_details':leave_details})


    # workrequests=ActualWorkflowStep.objects.filter(approver_id=uid)
    # cr_id_list=workrequests.values_list('created_request_id')
    # for i in range(len(workrequests)):
    #     wr=workrequests[i]
    #     cr=cr_id_list[i]
    #     if wr.request_name=='Regular Bills Request':
    #         bill_amount=RegularBillsRequestDetails.objects.get(created_request_id=cr).bill_amount
    #         return render(request, 'workrequestsforemployee.html',{'workrequest':wr,'cr_id':cr,'bill_amount':bill_amount})
    #     elif wr.request_name=='Purchase Request':
    #         amount=PurchaseRequestDetails.objects.get(created_request_id=cr).amount
    #         return render(request, 'workrequestsforemployee.html',{'workrequest':wr,'cr_id':cr,'amount':amount})
    #     elif wr.request_name=='Leave Request':
    #         reason=LeaveRequestDetails.objects.get(created_request_id=cr).reason
    #         no_of_days=LeaveRequestDetails.objects.get(created_request_id=cr).days
    #         return render(request, 'workrequestsforemployee.html',{'workrequest':wr,'cr_id':cr,'reason':reason,'no_of_days':no_of_days})    
    
def approve(request,uid,cr_id):
    ActualWorkflowStep.objects.filter(created_request_id=cr_id).filter(approver_id=uid).order_by('step_no').first().delete()
    wfs=WorkflowStep.objects.filter(created_request_id=cr_id).filter(status='PENDING').filter(approver_id=uid).order_by('step_no').first()
    wfs.status='COMPLETED'
    wfs.save()
    if not WorkflowStep.objects.filter(created_request_id=cr_id).filter(status='PENDING').exists():
        CreatedRequest.objects.filter(id=cr_id).update(status='APPROVED')
    return redirect('workrequestsforemployee', uid=uid)