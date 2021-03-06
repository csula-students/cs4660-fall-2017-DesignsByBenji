"""Files tests simple file read related operations"""
from io import open
class SimpleFile(object):
    """SimpleFile tests using file read api to do some simple math"""
    def __init__(self, file_path):
        self.numbers = []
        """
        TODO: reads the file by path and parse content into two
        dimension array (numbers)
        """
        f = open(file_path)
        for line in f:
            self.numbers.append([float(i) for i in line.strip().split(' ')])
        f.close()

    def get_mean(self, line_number):
        """
        get_mean retrieves the mean value of the list by line_number (starts
        with zero)
        """
        avg = 0
        for i in self.numbers[line_number]:
            avg += i
        avg = avg/len(self.numbers[line_number])
        return avg

    def get_max(self, line_number):
        """
        get_max retrieves the maximum value of the list by line_number (starts
        with zero)
        """
        return max(self.numbers[line_number])

    def get_min(self, line_number):
        """
        get_min retrieves the minimum value of the list by line_number (starts
        with zero)
        """
        return min(self.numbers[line_number])

    def get_sum(self, line_number):
        """
        get_sum retrieves the sumation of the list by line_number (starts with
        zero)
        """
        sum = 0
        for i in self.numbers[line_number]:
            sum += i
        return sum
