from django.shortcuts import render
from django.http import HttpResponse,HttpRequest,HttpResponseRedirect
from lab1.forms import RegisterForm
from django.urls import reverse
from django.contrib.auth import login

import random
import numpy as np

random.seed(10)
LoggerN = 10
domuM = 6
security = [5,5,4,1,6,5]
perf = [5,5,4,1,6,2]
test = print("Number of Loggers:"+ str(LoggerN))
max_unoccupied = 0
N_max = None
x_max = None

metricrow = []
loggerSum = []


# Function Metric
def create_metric_square(LoggerN, domuM):
    metric_square = []
    for i in range(domuM):
        row = [0] * LoggerN
        random_index = random.randint(0, LoggerN - 1)
        row[random_index] = 1
        metric_square.append(row)

    domU_sum = [0] * LoggerN
    for i in range(LoggerN):
        for j in range(domuM):
            domU_sum[i] += metric_square[j][i]
            if domU_sum[i] > 1:
              domU_sum[i] = 1
            elif domU_sum[i] < 1:  
              domU_sum[i] = 0
   
        total_logger = sum(domU_sum)

    return metric_square, domU_sum, total_logger

def constraint_check(C, P, x):
    X = np.array(x)
    N = X.sum(axis=0)

    for i, c_i in enumerate(C):
        j = np.where(X[i] == 1)
        # if c_i == 0 and N[j][0] != 1:
        #     #print("Sec:", i, N[j][0])
        #     return False, N

        # if c_i == 1 and N[j][0] <= 1:
        #     #print("Perf:", i, N[j][0])
        #     return False, N
        if C[i] < N[j][0] or P[i] > N[j][0]:
            return False, N

    return True, N

def objective(N):
    return N[np.where(N==0)].shape[0]

def penalty(C, P, x):
    X = np.array(x)
    N = X.sum(axis=0)
    cost = 0
    for i, c_i in enumerate(C):
        j = np.where(X[i] == 1)
        if C[i] < N[j][0]:
            cost += 2 * (C[i] - N[j][0])

        if P[i] > N[j][0]:
            cost += 1 * (N[j][0] - P[i])

    return cost, N


    # print("Number of free Logger: "+ str(obj_max))
    # print("Pernalty Values: "+ str(cost_max))
    # print("Total of free Logger: "+ str(max_unoccupied))
    
    #print(N_max, obj_max, cost_max, max_unoccupied)

if False:
    for row in x_max:
        print(row)
        print("Constrained ==================================")
else:
    max_unoccupied = 0
    N_max = None
    x_max = None
    obj_max = 0
    cost_max = 0
    for i in range(1000):
        x, domU_sum, total_logger = create_metric_square(LoggerN, domuM)
        cost, N = penalty(security, perf, x)
        obj_val = objective(N) + cost

        if obj_val > max_unoccupied:    
            max_unoccupied = obj_val
            x_max = x
            N_max = N
            num_ofRow = len(x_max)
            obj_max = objective(N)
            cost_max = cost
          # Add column headers
            header_row = ["    "] + ["L" + str(i+1) for i in range(len(N_max))]
            # x_max.insert(0, header_row)
  
          # Add row headers
            # for i in range(num_ofRow):
            #     x_max[i+1] = ["VM" + str(i+1)] + x_max[i+1]

            # Add column headers
            header_row_N = ["L" + str(i+1) for i in range(len(N_max))] 
            
            new_N_max = np.vstack((header_row_N,N_max))
            

        # print("Best Model ==>")
        # print(' '.join(str(e) for e in header_row))
    i = 1
    for row in x_max:
        print(f"VM{i} {row}")
        metricrow.append(row)
        i += 1


    loggerSum.append(new_N_max[1])     
# ##########################################################################
# # Web Page
def index(request):
    # all_product = Product.objects.all()
    # filter_product = Product.objects.filter()
    return render(request, 'index.html')

def home(request):
    return render(request, 'index.html')

def metric(request):
  
    return render(request, 'metric.html',\
                  {"LoggerN":LoggerN,\
                   "domuM":domuM,\
                   "security":security,\
                   "perf":perf,\
                   "metricmodel":metricrow,\
                   "header_row_N":header_row_N,\
                   'obj_max':obj_max,\
                   'loggerSum':loggerSum\
                   })\


def adminModel(request):
    return render(request, 'adminModel.html')

def register(request:HttpRequest):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return HttpResponseRedirect(reverse('index'))
    else :
        form = RegisterForm()
    context = {"form": form}
    return render(request,'register.html',context)




