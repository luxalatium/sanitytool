from __future__ import print_function
from TestBase   import TestBase
from util       import syshost, capture

class Compilers(TestBase):
  
  error_message=""

  def __init__(self):
    pass

  def setup(self):
    pass

  def description(self):
    return "Check available compilers:"

  def error(self):
    print(self.error_message)

  def execute(self):

    host=syshost()

    if syshost == 'stampede3':
      compilers=["gcc","g++","gfortran","icx","icpx","ifx","mpicc","mpicxx","mpif90"]
    else:
      compilers=["gcc","g++","gfortran","icc","icpc","ifort","mpicc","mpicxx","mpif90"]
      
    Flag=True

    for compiler1 in compilers:
      typecmd="type %s" %compiler1 
      output=capture(typecmd)
      if "not found" in output:
        Flag=False
        self.error_message+="        ERROR: Compiler %s is not available now!\n" %compiler1
    return Flag     

  def help(self):
    print("        Please check your $PATH again, compilers are missing.\n")

  def name(self):
    return "Check existing compilers"

