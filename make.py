import os
import re
import sys

import subprocess as sub

#choose your vsvars.bat
vsvars_bat = "c:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Preview\\VC\\Auxiliary\\Build\\vcvars64.bat"
#where to search source files
src_dir = "src"
#output for modules and obj files
out_dir = ".\\out\\"
#output executable
output_file = "bin\\hello.exe"
#compiler
compiler = "cl.exe"
#include dirs
includes = "" # for example "/I .\\dep\\inc /I .\\sub "
#library dirs
libdirs = "" # for example "/LIBPATH:\".\\dep\\lib\""
#libs to link
libs = "" # for example "shell32.lib gdi32.lib user32.lib"
#compiler args
cargs = includes + ("/nologo /experimental:module /module:output %s /std:c++latest /EHsc /MD /Fo%s /module:search %s /c") % (out_dir, out_dir, out_dir)
#linker args
largs = "/nologo /experimental:module /std:c++latest /MD" + " " + libs


#source extenstions
source_exts = [".ixx", ".cpp", ".cc", ".c", ".cxx"]

class BuildSession:
    def __init__(self):
       self.file_by_mod = {} # <mod, filename>
       self.deps = {} # <filename, array of modules>
       self.compiled = {} # <filename,bool> already compiled flag
       self.obj_files = [] # list of generated or existing object files to link


def makedirs():
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

def vs_env_dict():
    cmd = r'cmd /s /c ""%s" & set"' % (vsvars_bat)
    output = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.STDOUT, stdin=sub.PIPE).communicate()[0]
    output = output.decode().split("\r\n")
    return dict((e[0].upper(), e[1]) for e in [p.rstrip().split("=", 1) for p in output] if len(e) == 2)

def readModName(line):
    find = re.search("^export module (.*);", line)
    if find != None:
        return find.group(1)
    return None

def resolveImportMod(line):
    find = re.search("^import (.*);", line)
    if find != None:
        return find.group(1)
    return None

def resolveModName(lines):
    for line in lines:
        modname = readModName(line)
        if modname != None:
            return modname
    return "[no mod]"

def resolveImportMods(lines):
    mods = []
    for line in lines:
        mod = resolveImportMod(line)
        if mod != None:
            mods.append(mod)
    return mods

def resolveDependencies(build):
    print("resolving dependencies...")
    for root,dirs,files in os.walk(src_dir):
        for file in files:
            ext = os.path.splitext(file)[1]
            fullpath = os.path.join(root, file)
            if ext in source_exts:
                file = open(fullpath, "r")
                lines = file.readlines()
                mod = resolveModName(lines)
                if mod != None:
                    build.file_by_mod[mod] = fullpath
                
                imps = resolveImportMods(lines)
                build.deps[fullpath] = imps

                print("%s(%s) - %s" % (fullpath, mod, imps)) # shows dependencies of each file
                file.close()

def getObjName(filename):
    base = os.path.basename(filename)
    ext = os.path.splitext(base)
    base = base.replace(ext[1], ".obj")
    return os.path.join(out_dir, base)

def compile(filename):
    command = "%s %s %s" % (compiler, cargs, filename)
    ret = os.system(command)
    if ret != 0:
        print("ERROR!")
        return False
    return True

def recursiveCompile(filename, should, build):
    obj_fname = getObjName(filename)
    if obj_fname not in build.obj_files:
        build.obj_files.append(obj_fname)
    
    if filename in build.compiled and build.compiled[filename]:
        return True, False

    obj_mtime = 0
    if os.path.exists(obj_fname):
        obj_mtime = os.path.getmtime(obj_fname)
        file_mtime = os.path.getmtime(filename)
        should |= (file_mtime > obj_mtime)
    else:
        should = True

    for dep in build.deps[filename]:
        if dep in build.file_by_mod: #skip std modules
            file = build.file_by_mod[dep]
            ret, interrupt = recursiveCompile(file, False, build)
            if interrupt:
                return False, True
            should |= ret

    if should:
        comp = compile(filename)
        build.compiled[filename] = comp
        return should, not comp

    return should, False

def make():
    makedirs()
    build = BuildSession()
    resolveDependencies(build)
    should = False
    os.environ.update(vs_env_dict())
    print("compiling...")
    for root,dirs,files in os.walk(src_dir):
        for file in files:
            ext = os.path.splitext(file)[1]
            fullpath = os.path.join(root, file)
            if ext in source_exts:
                ret,interrupt = recursiveCompile(fullpath, False, build)
                if interrupt:
                    sys.exit(1)
                  
    print("linking...")
    exe_mtime = 0
    if os.path.exists(output_file):
        exe_mtime = os.path.getmtime(output_file)
    shouldlink = False
    for obj_fname in build.obj_files:
        file_mtime = os.path.getmtime(obj_fname)
        if file_mtime > exe_mtime:
            shouldlink = True
            
    allobj = ' '.join(build.obj_files);
    # print(allobj) #show all object files to be linked
                
    if shouldlink:
        command = "%s %s %s /link /OUT:%s %s" % (compiler, largs, allobj, output_file, libdirs)
        ret = os.system(command)
        if ret != 0:
            print("ERROR!")
            sys.exit(1)
    else:
        print("no obj files modified...")
    
    print("SUCCESS")

make()
    