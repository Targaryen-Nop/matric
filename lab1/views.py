from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from lab1.forms import RegisterForm
from django.urls import reverse
from django.contrib.auth import login
from Database.models import Member
import random
import numpy as np

random.seed(10)


def input(request):
    security=[]
    perf=[]
    if request.method == 'POST':
        user = request.POST.get('login')
        password = request.POST.get('password')
        sec = request.POST.get('sec')
        per = request.POST.get('per')
        Member.objects.create(login=user, password=password, security=sec, performance=per)
        security = list(Member.objects.values_list('security', flat=True))
        perf = list(Member.objects.values_list('performance', flat=True))
        data = {'security': security, 'perf': perf}
        print(type(security))
        print(type(perf))
        return render(request, "input.html", data,)
    return render(request, "input.html")
    


def read(request):
    security = Member.objects.all()
    perf = Member.objects.values_list('performance', flat=True)
    data = {'security': security, 'perf': perf}
    print(type(security))
    print(type(perf))
    return render(request, "input.html", data)


LoggerN = 10
security = [1, 1, 0, 5, 5, 5, 4, 3]
perf = [1, 1, 0, 4, 3, 3, 2, 3]
domuM = len(perf)
test = print("Number of Loggers:" + str(LoggerN))
max_unoccupied = 0
N_max = None
x_max = None
obj_max = 0
cost_max = 0
c_cost_max = 0

metricrow = []
loggerSum = []
loggerSum2 = []

metricrow_old = []
metricrow_new = []


# Function Metric

def create_metric_square2(LoggerN, domuM, x_old):
    swap_prob = 20  # ระบุเปอร์เซ็นในการที่จะทำการสลับที่ของ VM
    metric_square = []
    for i in range(domuM):
        if random.randrange(100) < swap_prob or np.sum(x_old[i]) > 1:
            row = [0] * LoggerN
            random_index = random.randint(0, LoggerN - 1)
            row[random_index] = 1
            metric_square.append(row)
        else:
            metric_square.append(x_old[i].tolist())

    return metric_square


def penalty2(C, P, x):
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


def penalty_swap(x_old, x):
    x = np.array(x)
    # vm ทั้งหมด ลบ ด้วย VM ที่ไม่ถูกสลับที่ 0.5 คือค่าลงโทษสำหรับการสลับที่2
    # return 0.5 * (x.shape[0]  - np.sum(np.multiply(x_old,x)))
    return 0.5 * (np.sum(np.multiply(x_old, x)) - x.shape[0])


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
    return N[np.where(N == 0)].shape[0]


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


x_old = np.loadtxt("logger.out", dtype=int)
for i in range(x_old.shape[0], len(security)):
    x_old = np.vstack([x_old, [1]*LoggerN])

for i in range(x_old.shape[0]-1, -1, -1):
    if perf[i] == 0:
        x_old = np.delete(x_old, (i), axis=0)
        del security[i]
        del perf[i]

print(x_old)
print("Security Level of VMs New: " + str(security))
print("Performance Level of VMs New: " + str(perf))
domuM = len(perf)
if x_max != None:
    for row in x_max:
        print(row)

    print("Constrained ==================================")
    print(N_max, max_unoccupied)
else:
    max_unoccupied = 0
    N_max = None
    x_max = None
    obj_max = 0
    cost_max = 0
    for i in range(1000):
        x2 = create_metric_square2(LoggerN, domuM, x_old)
        cost2, N2 = penalty2(security, perf, x2)
        c_cost = penalty_swap(x_old, x2)
        x, domU_sum, total_logger = create_metric_square(LoggerN, domuM)
        cost, N = penalty(security, perf, x)
        obj_val = objective(N) + cost

        obj_val2 = objective(N2) + cost2 + c_cost

        if obj_val2 > max_unoccupied:
            max_unoccupied2 = obj_val2
            x_max2 = x2
            N_max2 = N2
            num_ofRow2 = len(x_max2)
            obj_max2 = objective(N2)
            cost_max2 = cost2
            c_cost_max2 = c_cost
            header_row_N2 = ["L" + str(i+1) for i in range(len(N_max2))]
            new_N_max2 = np.vstack((header_row_N2, N_max2))

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

          # Add row headers;
            # for i in range(num_ofRow):
            #     x_max[i+1] = ["VM" + str(i+1)] + x_max[i+1]

            # Add column headers
            header_row_N = ["L" + str(i+1) for i in range(len(N_max))]

            new_N_max = np.vstack((header_row_N, N_max))

    print("Best Model ==>")
    print(' '.join(str(e) for e in header_row))
    i = 1
    for row in x_max:
        print(f"VM{i} {row}")
        metricrow.append(row)
        i += 1
    loggerSum.append(new_N_max[1])

    metricrow_old.append(x_old)
    loggerSum2.append(new_N_max2[1])
    for row in x_max2:
        print(f"VM{i} {row}")
        metricrow_new.append(row)
        i += 1

# print("Number of VMs in Logger: "+str(new_N_max[1]))
# print("Number of free Logger: " + str(obj_max))
# print("Total of free Logger: " + str(max_unoccupied))
# print("Penalty Values: " + str(cost_max))s


x_max2 = np.array(x_max2)
# print(obj_max, cost_max, c_cost_max)
# print("Number of VMs in Logger: "+str(N_max))
print("Number of free Logger: " + str(obj_max2))
print("Penalty Values: " + str(cost_max2))
print("Penalty Swap: "+str(c_cost_max2))
print("Total of free Logger: " + str(max_unoccupied2))
# print(metricrow_new)
print("Old Solution ==>")
print(x_old)
print("New Solution ==>")
print(x_max2)

# ##########################################################################


def index(request):
    # all_product = Product.objects.all()
    # filter_product = Product.objects.filter()
    return render(request, 'index.html')


def home(request):
    return render(request, 'index.html')


def metric(request):

    return render(request, 'metric.html',
                  {"LoggerN": LoggerN,
                   "domuM": domuM,
                   "security": security,
                   "perf": perf,
                   "metricmodel": metricrow,
                   "header_row_N": header_row_N,
                   'obj_max': obj_max,
                   'loggerSum': loggerSum,
                   'penalty': cost_max,
                   'total': max_unoccupied
                   })


def metric2(request):
    return render(request, 'metric2.html',
                  {"LoggerN": LoggerN,
                   "domuM": domuM,
                   "security": security,
                   "perf": perf,
                   "metricmodel_new": metricrow_new,
                   "metricmodel_old": metricrow_old,
                   "header_row_N": header_row_N,
                   'obj_max': obj_max2,
                   'loggerSum': loggerSum2,
                   'penalty': cost_max2,
                   'penaltySwap': c_cost_max2,
                   'total': max_unoccupied2
                   })


def adminModel(request):
    return render(request, 'adminModel.html')


def register(request: HttpRequest):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegisterForm()
    context = {"form": form}
    return render(request, 'register.html', context)
