from django.db import models

# Create your models here.


class Problem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    inputs = models.TextField()

    def __str__(self):
        return self.title

    def TestCase(self):
        result = []
        data = self.inputs.split('\n')

        curr = []
        curr_type = ""
        for line in data:
            if line[0] == 's':
                if len(curr) != 0:
                    result.append({'type': curr_type, 'data': curr})
                curr = []
                curr_type = line[4:]
            elif line[0] == 'i':
                curr.append({'type': 'in', 'data': line[3:]})
            elif line[0] == 'o':
                curr.append({'type': 'out', 'data': line[4:]})
        if len(curr) != 0:
            result.append({'type': curr_type, 'data': curr})

        return result

    def TestCasePublic(self):
        result = self.TestCase()
        result = filter(lambda case: case['type'][:3]=="pub", result)
        return result