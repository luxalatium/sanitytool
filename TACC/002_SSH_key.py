from __future__ import print_function
from TestBase   import TestBase 
from util       import run_cmd, capture, syshost

class SSH_key(TestBase): 

  error_message=""

  def __init__(self):
    self.host = syshost()
    if self.host == 'stampede3':
      self.public_key_file = 'id_ed25519.pub'
    else:
      self.public_key_file = 'id_rsa.pub'

  def setup(self):
    pass

  def description(self):
    return "SSH Key Test:"

  def error(self):
    print(self.error_message)

  def help(self):
    print(f"        Please check your .ssh directory, and append the contents of ~/.ssh/{self.public_key_file} to ~/.ssh/authorized_keys.\n")

  def execute(self):
    result  = True
    pub_key = capture(f'cat ~/.ssh/{self.public_key_file}').replace('\n','')
    cmd     = "grep -F \"%s\" ~/.ssh/authorized_keys > /dev/null 2>&1" % pub_key
    status  = run_cmd(cmd)

    if (status != 0):
      self.error_message+=f"        Error: ~/.ssh/{self.public_key_file} not found in ~/.ssh/authorized_keys.\n"
      return False 

    if self.host == 'stampede3':
      cmd2 ="awk '{if ($1!=\"ssh-ed25519\" || NF <= 1) print $0}' ~/.ssh/authorized_keys"
    else:
      cmd2 ="awk '{if ($1!=\"ssh-dss\" && $1!=\"ssh-rsa\" || NF <= 1) print $0}' ~/.ssh/authorized_keys"

    cmd2_out = capture(cmd2)

    if cmd2_out:
      self.error_message+="        Error: ~/.ssh/authorized_keys includes invalid or broken key(s).\n"
      return False
     
    return result
 
  def name(self):
    return "SSH Key"
