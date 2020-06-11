# CPPModPy
C++20 Modules (MSVCs cl.exe) Easy Python Builder (ONLY FOR VERY SIMPLE PROJECTS, no partitions, no header units etc...)
Tested only with VS2019 Preview

This is very easy C++20 modules builder only for Visual Studio cl compiler, it will work only for simple cases
- export module X;
- import X;

First it will try to generate dependencies based on source text files, then it will compile source files recursively so dependent modules will be built first.
It will try not to recompile already compiled sources in current build session, and it will try not to compile sources based on modification time of generated .obj files.

# How to use
1. Place your C++ modules(.ixx) in src folder
2. Change path to vsvars.bat in make.py
3. Run "python make.py"
