init -100 python:
    
    import math
    
    class mat(object):
        
        def __init__(self, data):
            
            self.rows = len(data)
            self.cols = len(data[0])
            self.data = data
            
            for x in range(self.rows):
                if (isinstance(data[x], list) == False) or (len(data[x]) != self.cols):
                    raise exception("matrix class can only be initialised with lists of matching length")
        
        # Equality operators
        
        def __eq__(self, other):
            
            if (isinstance(other, mat) == False):
                return False
            
            if (self == None or other == None):
                if (self == None and other == None):
                    return True
                else:
                    return False
                
            
            if (self.rows != other.rows) or (self.cols != other.cols):
                return False
            for y in range(self.rows):
                for x in range(self.cols):
                    if self.data[y][x] != other.data[y][x]:
                        return False
            return True
            
        def __ne__(self, other):
            return self.__eq__(other) == False
            
        # Arithmetic Operators
        
        def __add__(self, other):
            
            if (self.rows != other.rows) or (self.cols != other.cols):
                raise exception("matrix addition can only be performed on matrices of similar order")
                
            # prep output
            output = [[0 for col in range(self.cols)] for row in range(self.rows)]
            
            for y in range(self.rows):
                for x in range(self.cols):
                    output[y].append(self.data[y][x] + other.data[y][x])
                    
            return mat(output)
            
        def __sub__(self, other):

            if (self.rows != other.rows) or (self.cols != other.cols):
                raise exception("matrix subtraction can only be performed on matrices of similar order")
                
            # prep output
            output = [[0 for col in range(self.cols)] for row in range(self.rows)]
            
            for y in range(self.rows):
                for x in range(self.cols):
                    output[y].append(self.data[y][x] - other.data[y][x])
                    
            return mat(output)
            
        def __mul__(self, other):
            
            # prep output
            output = [[0 for col in range(other.cols)] for row in range(self.rows)]
            
            for y in range(self.rows):
                for x in range(other.cols):
                    for i in range(self.cols):
                        output[y][x] += self.data[y][i] * other.data[i][x]
                        
            return mat(output)
            
        # TODO: write overloads for all the operators which make no sense on a matrix and throw exceptions.
        
        # Easy Access
        def __getitem__(self, key):
            return self.data[key]
        
        def __str__(self):
            return str(self.data)
            
        def __repr__(self):
            return repr(self.data)
        
        # Utility statics
        @staticmethod
        def identity(order):
            
            # prep output
            output = [[0 for col in range(order)] for row in range(order)]
            
            for x in range(order):
                output[x][x] = 1
                
            return mat(output)

        # Static methods for 2D matrices
        @staticmethod
        def smat(x, y):
            
            return mat([[x], [y], [1]])

        @staticmethod
        def sidentity():
            
            return mat.identity(3)

        @staticmethod
        def stranslate(x, y):
            
            output = mat.sidentity()
            
            output.data[0][2] = x
            output.data[1][2] = y
            
            return output
            
        @staticmethod
        def srotate(deg):
            
            rads = (-1 * float(deg))/180.0 * math.pi
            
            output = mat([[math.cos(rads), -1 * math.sin(rads), 0],[math.sin(rads), math.cos(rads), 0], [0,0,1]])
            
            return output
            
        @staticmethod
        def srotatearound(x, y, deg):
            
            toorigin = mat.stranslate(-1 * x, -1 * y)
            rot = mat.srotate(deg)
            fromorigin = mat.stranslate(x, y)
            
            return fromorigin * (rot * toorigin)
            
        @staticmethod
        def sscale(x, y):
            
            return mat([[x, 0, 0],[0, y, 0],[0, 0, 1]])
            
        @staticmethod
        def sxskew(degree):
            
            return mat([[1, 0, 0], [degree, 1, 0], [0, 0, 1]])
            
        @staticmethod
        def syskew(degree):
            
            return mat([[1, degree, 0], [0, 1, 0], [0, 0, 1]])
            
        @staticmethod
        def sinvert(input):
            
            a = input[0][0]
            b = input[0][1]
            c = input[0][2]

            d = input[1][0]
            e = input[1][1]
            f = input[1][2]

            g = input[2][0]
            h = input[2][1]
            i = input[2][2]

            det = (a*e*i) + (b*f*g) + (c*d*h) - (c*e*g) - (b*d*i) - (a*f*h)
            x = 1.0/det

            A = (e*i) - (f*h)
            B = (f*g) - (d*i)
            C = (d*h) - (e*g)
            D = (c*h) - (b*i)
            E = (a*i) - (c*g)
            F = (g*b) - (a*h)
            G = (b*f) - (c*e)
            H = (c*d) - (a*f)
            I = (a*e) - (b*d)
            
            A = x*A
            B = x*B
            C = x*C
            D = x*D
            E = x*E
            F = x*F
            G = x*G
            H = x*H
            I = x*I
            
            return mat([[A,D,G],[B,E,H],[C,F,I]])
            

