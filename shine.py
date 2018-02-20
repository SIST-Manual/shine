import math
#return sin(x), where x is measured in degree
def sin(x):
    return math.sin(x / 180 * math.pi)

#return cos(x), where x is measured in degree 
def cos(x):
    return math.cos(x / 180 * math.pi)
#class of  pictures
class picture(object):
    def __init__(self):
        self.points = []
        self.filled = False
        self.linear = True
    def  __str__(self):
        result = str(self.points[0][0]) + ' ' + str(self.points[0][1]) + ' moveto'
        list = self.points[1:]
        for i in list:
            result += '\n' + str(i[0]) + ' ' + str(i[1]) + ' ' + 'lineto'
        if not self.linear:
            result += '\n'
            for i in self.sector:
                result += str(i) + ' '
            result = result[:-1]
            result += '\n' + str(self.points[0][0]) + ' ' + str(self.points[0][1]) + ' ' + 'lineto'
        if self.filled:
            return result + '\nfill'
        return result + '\nstroke'
#pictures
def line(X0, Y0, X1, Y1):
    result = picture()
    result.points.append((X0, Y0))
    result.points.append((X1, Y1))
    return result

def rect(X, Y, W, H):
    result = picture()
    result.points.append((X, Y))
    result.points.append((X + W, Y))
    result.points.append((X + W ,Y + H))
    result.points.append((X, Y + H))
    result.points.append((X, Y))
    return result

def ngon(X, Y, R, N):
    result = picture()
    t = nearest(N)
    result.points.append((X + R, Y))
    for i in range(t):
        a = (i + 1) / t * 180 *2
        result.points.append((X + R * cos(a), Y + R * sin(a)))
    return result

def sector(X, Y, R, B, E):
    result = picture()
    result.linear = False
    result.points.append((X, Y))
    result.points.append((X + R * cos(B), Y + R * sin(B)))
    result.sector = [X, Y, R, B % 360, E % 360, 'arc']
    return result

def tri(X, Y, R):
    return ngon(X, Y, R, 3)

def square(X, Y, R):
    return ngon(X, Y, R, 4)

def penta(X, Y, R):
    return ngon(X, Y, R, 5)

def hexa(X, Y, R):
    return ngon(X, Y, R, 6)

def filledrect(X, Y, W, H):
    result = rect(X, Y, W, H)
    result.filled = True
    return result

def filledngon(X, Y, R, N):
    result = ngon(X, Y, R, N)
    result.filled = True
    return result

def filledsector(X, Y, R, B, E):
    result = sector(X, Y, R, B, E)
    result.filled = True
    return result

def filledtri(X, Y, R):
    return filledngon(X, Y, R, 3)

def filledsquare(X, Y, R):
    return filledngon(X, Y, R, 4)

def filledpenta(X, Y, R):
    return filledngon(X, Y, R, 5)

def filledhexa(X, Y, R):
    return filledngon(X, Y, R, 6)
#return the nearest integer of x
def nearest(x):
    if x - int(x) < 0.5:
        return int(x)
    return int(x) + 1
#transformation
def translate(P, X, Y):
    result = picture()
    result.filled = P.filled
    result.linear = P.linear
    result.points = []
    for point in P.points:
        x0 = point[0]
        y0 = point[1]
        result.points.append((x0 + X, y0 + Y))
    #which means sector/filledsector
    if not P.linear:
        x1 = P.sector[0] + X
        y1 = P.sector[1] + Y
        result.sector = [x1 , y1] + P.sector[2:]
    return result

def rotate(P, X):
    result = picture()
    result.filled = P.filled
    result.linear = P.linear
    result.points = []
    def degree(point):
        x, y = point
        r = (x ** 2 + y ** 2) ** 0.5
        if r == 0:
            result = 90
        else:
            result = math.degrees(math.asin(y / r))
            if x < 0:
                result = 180 - result
        return result
    def r(point):
        x, y = point
        return (x ** 2 + y ** 2) ** 0.5
    for point in P.points:
        a = degree(point)
        result.points.append((r(point) * cos(a + X), r(point) * sin(a + X)))
    #which means sector/filledsector
    if not P.linear:
        result.sector = []
        a = P.sector[:]
        p1, p2 = P.points
        a1, a2 = degree(p1), degree(p2)
        r1, r2 = r(p1), r(p2)
        p1 = (r1 * cos(a1 + X), r1 * sin(a1 + X))
        p2 = (r2 * cos(a2 + X), r2 * sin(a2 + X))
        B = degree((p2[0] - p1[0], p2[1] - p1[1]))
        E = B + (a[4] - a[3])
        result.sector = [p1[0], p1[1], r((p2[0] - p1[0], p2[1] - p1[1])), B % 360, E % 360, 'arc']
    return result

def scale(P, S):
    result = picture()
    result.filled = P.filled
    result.linear = P.linear
    result.points = []
    for point in P.points:
        x, y = point
        result.points.append((x * S, y * S))
    #which means sector/filledsector
    if not P.linear:
        X, Y, R = P.sector[:3]
        result.sector = [X * S, Y * S, R * S] + P.sector[3:]
    return result
#drawing parameters
def color(R, G, B):
    return str(R) + ' ' + str(G) + ' ' + str(B) + ' setrgbcolor'

def linewidth(W):
    return  str(W) + ' setlinewidth'
#string processing
def fixAssignment(s):
    def validAssignment(s):
        return '=' in s and removeSpace(s[s.find('=') + 1:]) != '' and s.count('(') == s.count(')') and s[-1] == ' '
    if not validAssignment(s):
        return s
    if s.count('(') != 0:
        return s
    a = s.find('=')
    return  s[:a] + '= (' + s[a + 1:] + ')'

def valid(s):
    if s == '':
        return False
    return (s.count('(') == s.count(')') and s[-1] == ')' and removeSpace(s)[0] != '{' and s.split()[0] != 'for')  or (s.count('{') == s.count('}')  and  s[-1] == '}' and s.count('(') == s.count(')'))

def removeSpace(s):
    try:
        i = 0
        while s[i] == ' ' :
            i += 1
        return s[i:]
    except:
        return ''

def fixValid(s):
    #insert missed '('    or   ')' 
    def fixUnary(s):
        tokens = s.split()
        for i in range(len(tokens)):
            if  (tokens[i] == 'sin' or tokens[i] == 'cos') and (tokens[i + 1] not in list('+-*/),(')):
                tokens[i] = tokens[i] + ' ( '
                tokens[i + 1] = tokens[i + 1] + ' ) '
            else:
                pass
            result = ''
        for token in tokens:
            result += ' ' + token + ' '
        return result
    #fix name in commands
    def fixName(s):
        def suspect(s):
            #+,
            if s in list('.1234567890();,:+-*/=  '):
                return False
            return not(s[0] in list('.1234567890();,:+-*/=  '))
        start = s.find('(')
        executed = s[start + 1:]
        tokens = executed.split()
        for i in range(len(tokens)):
            if not(suspect(tokens[i])):
                continue
            elif tokens[i + 1] == '(':
                continue
            #now it is sure that tokens[i] is a name of a variable, rather than of a function
            else:
                tokens[i] = 'variables[\'' + tokens[i] + '\']'
        result = s[:start + 1]
        for token in tokens:
            result += ' ' +  token + ' '
        return result
    result = fixUnary(s)
    result = fixName(result)
    return result
#execute the input
def carryOut(command):
    global count
    count += 1
    if count >= 2500000:
        exit(0)
    #for
    if command.split()[0] == 'for':
        existed = False
        V = command.split()[1]
        if V in variables:
            a = variables[V]
            existed = True
        expressions = ''
        for i in command.split()[3:]:
            if i == '{':
                break
            expressions += ' ' + i + ' '
        G = command[command.find('{'):]
        expression1 = expressions.split('..')[0]
        expression2 = expressions.split('..')[1]
        L = nearest(eval(fixValid(expression1)))
        H = nearest(eval(fixValid(expression2)))
        value = L
        while value <= H:
            variables[V] = value
            carryOut(G)
            value += 1
        #restore V's previous value
        if existed:
            variables[V] = a
        else:
            variables.pop(V)
    #group
    elif '{' in command:
        a = command.find('{')
        b = command.find('}') + 1
        executed = command[a + 1:b - 1]
        commands = executed.split(';')
        for  i in commands:
            carryOut(command[:a] + i + command[b:])
    #assignment
    elif '=' in command:
        command = command[:command.find('=') + 1] + fixValid(command[command.find('=') + 1:])
        #remove 'let'
        command = removeSpace(command)[3:]
        L = command.split('=')
        name = L[0].replace(' ', '')
        value = eval(L[1])
        variables[name] = value
    else:
        command = fixValid(command)
        print(eval(command))
#main
print('%!PS-Adobe-3.0 EPSF-3.0')
print('%%BoundingBox: 0 0 1239 1752')
try:
    count = 0
    s = ''
    while 1:
        try:
            s += ' ' + str(input()) + ' '
        except EOFError:
            break
    command = ''
    s1 = ''
    variables = {}
    for i in s:
        s1 += i
        command = fixAssignment(s1)
        if valid(command):
            #command without group and for
            try:
                carryOut(command)
            except:
                pass
            finally:
                command = ''
                s1 = ''
        if count >= 250000:
            break
except:
    pass
