import pickle, ast


data = pickle.load(open("./ast_dump.pickle", "rb"))

print(ast.dump(data, indent=4))
