import unittest

def add(x, y):
    return x + y

def subtract(x,y):
    return x - y 

def divide(x,y):
    return x / y

def multiply(x,y):
    return x * y

class TestCalculator(unittest.TestCase):
    def test_add_positive_numbers(self):
        result = add(2, 3)
        self.assertEqual(result, 5)
    
    def test_minus_positive_numbers(self):
        result = subtract(3, 2)
        self.assertEqual(result, 1)

    def test_division_positive_numbers(self):
        result = divide(10, 5)
        self.assertEqual(result, 2)
    
    def test_muiltiplication_positive_numbers(self):
        result = multiply(3, 2)
        self.assertEqual(result, 6)


if __name__ == '__main__':
    unittest.main()