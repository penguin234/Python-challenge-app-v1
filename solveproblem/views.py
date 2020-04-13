from django.shortcuts import render, get_object_or_404
from .models import Problem

# Create your views here.


def home(request):
    problems = Problem.objects
    return render(request, 'solveproblem/home.html', {'problems': problems})


def problem(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    return render(request, 'solveproblem\problem.html', {'problem': problem})


class OutputChecker:
    __outputs = ""
    def write(self, output):
        self.__outputs += output
    
    def Compare(self, outs):
        sout = self.__outputs.strip().split("\n")
        if(len(outs) != len(sout)):
            return False
        for i in range(len(outs)):
            origin = outs[i].strip()
            compare = sout[i].strip()
            if origin != compare:
                return False
        return True
    
    def Clear(self):
        self.__outputs = ""

precode = """
curr_input_index = [-1]
def input(prompt=""):
    curr_input_index[0] += 1
    return test_case_input_list[curr_input_index[0]]

print_original_version = print
def print(*objects, sep=' ', end='\\n', file=test_case_output_collect, flush=False):
    print_original_version(*objects, sep=sep, end=end, file=file, flush=flush)
"""

def submit(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    testcases = problem.TestCase()

    result = {'completed': True}

    source = request.GET['code']
    source = precode + source
    try:
        source = compile(source, '<string>', 'exec')
    except Exception as err:
        result['completed'] = False
        result['description'] = str(err)
        return render(request, 'solveproblem\\result.html', {'result': result})

    check = OutputChecker()
    for case in testcases:
        ins = []
        outs = []
        for line in case['data']:
            if line['type'] == 'in':
                ins.append(line['data'])
            else:
                outs.append(line['data'])
        check.Clear()
        try:
            exec(source, {'test_case_input_list': ins, 'test_case_output_collect': check})
        except Exception as err:
            result['completed'] = False
            result['description'] = str(err)
            break
        if not check.Compare(outs):
            result['completed'] = False
            result['description'] = "Wrong output"
            break
    
    return render(request, 'solveproblem\\result.html', {'result': result})