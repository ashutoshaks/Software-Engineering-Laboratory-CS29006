class Vector:
        
    def __init__(self, *args): 
        # if arg is an int (dimension)
        if isinstance(args[0], int): 
            self._coords = [0] * args[0]
        # if arg is an iterable type
        else:
            self._coords = [x for x in args[0]]

    def __len__(self):
        # return the dimension of the vector
        return len(self._coords)

    def __getitem__(self, j):
        # return the jth coordinate of the vector
        if(len(self) < j):
            print("ERROR! {}th coordinate does not exist for this vector".format(j))
            return
        return self._coords[j]

    def __setitem__(self, j, val):
        # set the jth coordinate of vector to val
        if(len(self) < j):
            print("ERROR! {}th coordinate does not exist for this vector".format(j))
            return
        self._coords[j] = val

    def __add__(self, other):
        # u + v
        if(len(self) != len(other)):
            print("ERROR! Trying to add two vectors of diferent dimensions")
            return
        sum_vector = [(self[i] + other[i]) for i in range(len(self))]
        return Vector(sum_vector)
            
    def __eq__(self, other):
        # return True if vector has same coordinates as other
        if(len(self) != len(other)):
            print("ERROR! Trying to compare two vectors of diferent dimensions")
            return
        return (self._coords == other._coords)
    
    def __ne__(self, other):
        # return True if vector differs from other
        if(len(self) != len(other)):
            print("ERROR! Trying to compare two vectors of diferent dimensions")
            return
        return (self._coords != other._coords)
    
    def __str__(self):
        # return the string representation of a vector within <>
        return "<{}>".format(", ".join(map(str, self._coords)))

    def __sub__(self, other):
        # Soln for Qs. 2
        if(len(self) != len(other)):
            print("ERROR! Trying to subtract two vectors of diferent dimensions")
            return
        diff_vector = [(self[i] - other[i]) for i in range(len(self))]
        return Vector(diff_vector)

    def __neg__(self):
        # Soln for Qs. 3
        neg_vector = [-(self[i]) for i in range(len(self))]
        return Vector(neg_vector)
    
    def __rmul__(self, value):
        return (self * value)
    
    def __mul__(self, other):
        # Soln for Qs. 4, 5 and 6
        if(isinstance(other, Vector)):
            if(len(self) != len(other)):
                print("ERROR! Trying to take dot product of two vectors of diferent dimensions")
                return
            dot_product = sum([(self[i] * other[i]) for i in range(len(self))])
            return dot_product
        else:
            prod_vector = [(self[i] * other) for i in range(len(self))]
            return Vector(prod_vector)
    
def main():

    # Add suitable print statements to display the results
    # of the different question segments

    v1 = Vector([1, 2, 3, 4])
    v2 = Vector([5, 7, 9, 11])
    v3 = Vector(5)

    print("Vector v1 : ", end = "")
    print(v1)
    print("Vector v2 : ", end = "")
    print(v2)
    print("Vector v3 : ", end = "")
    print(v3)
    print()

    print("Dimension of Vector v1 : {}".format(len(v1)))
    print("Dimension of Vector v2 : {}".format(len(v2)))
    print("Dimension of Vector v3 : {}".format(len(v3)))
    print()

    print("Get v3[1]")
    print(v3[1])
    print()

    print("Set v3[1] = 10")
    v3[1] = 10
    print(v3)
    print()

    print("Adding vectors v1 and v2")
    print(v1 + v2)
    print()

    print("Checking if vectors v1 and v2 are equal")
    print(v1 == v2)
    print()

    print("Checking if vectors v1 and v2 are unequal")
    print(v1 != v2)
    print()

    print("Subtracting vectors v1 and v2")
    print(v1 - v2)
    print()

    print("New vector after negating vector v1")
    print(-v1)
    print()

    print("Trying to perform v1 * 3")
    print(v1 * 3)
    print()

    print("Trying to perform 3 * v1")
    print(3 * v1)
    print()

    print("Trying to perform v1 * v2")
    print(v1 * v2)
    print()

if __name__ == '__main__':
    main()