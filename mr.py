import sys

if len(sys.argv) > 1:
    arguments = sys.argv[1]
    print(f"params received by python: {arguments}")
else:
    print("Nothing")