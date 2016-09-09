import sys
import filecmp

def main():
    """Checks if two files are equal"""

    if len(sys.argv)==3:
        file_a = sys.argv[1]
        file_b = sys.argv[2]
        if filecmp.cmp(file_a, file_b):
            print("Files are eqaul, whoopee")

        else:
            print("Files are not equal :( ")

if __name__ == '__main__':
    main()



