# Information
- **CTF:** *TJCTF*
- **Challenge name:** *serpent*
- **Challenge description:** *go to the deepest level*
- **Category:** *rev*
- **Date:** *June 2025*
# Approach
We are provided with a .pickle file (`ast_dump.pickle`). A simple search informs us that it is a file format used by python to store serialised objects.

A further search reveals how we can deserialise the data to retrieve the python object using the pickle module.

When I saw the filename contain the letters `ast`, I was immediately reminded of [abstract syntax trees](https://en.wikipedia.org/wiki/Abstract_syntax_tree), a way to represent the meaning of written code in a computer. ASTs are commonly used by parsers (within compilers or interpreters) to assign meaning written code.

We can very easily work out the type of the object we have just deserialised by using the `type()` method and passing the object as an argument. We find that its type is `ast.Module`. This is an object that represents the AST when a certain chunk of code was compiled! 

Further searching reveals that we can obtain a string representation the entire AST by calling `ast.dump()` and supplying the AST that we had obtained through deserialisation (Note: in my solve script, I included another argument `indent=4`; this argument simply tells the method to properly indent the output).

When we finally execute the script, we notice that a lot of things are printed!

Since we are already told that we need to "go to the deepest layer", and our code is already nicely indented, I simply chose to scroll through the output and find the most indented chunk of text. Sure enough, our flag was there, hidden amidst the sea of fake flags!
# Flag
```tjctf{f0ggy_d4ys}```
# Tags
- TJCTF
- Rev
- AST
- Python
---
*Written on 09-06-2025*

