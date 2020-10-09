
import os
from spack.build_systems.autotools import AutotoolsPackage
from spack.util.environment import is_system_path
from spack.directives import depends_on, extends
from spack.package import run_before
from spack.util.executable import Executable
from llnl.util.filesystem import join_path
from spack.util.environment import EnvironmentModifications

class ConfixPackage(AutotoolsPackage):
  """Specialized class for packages built using confix."""

  confix_prefixes = []
  confix_args = []

  depends_on('py-confix')
  depends_on('libtool')
  depends_on('automake')
  depends_on('autoconf')

  def add_confix_arg( self, arg ):
    self.confix_args.append(arg)

  def confix_configure(self):
    read_only_prefixes = ","
    read_only_prefixes = read_only_prefixes.join( self.confix_prefixes )

    reconfigure = Executable('confix2.py')
    self.confix_args.append( '--readonly-prefix=' + read_only_prefixes )

    reconfigure(*self.confix_args)

    # touch maybe nonexisting files
    open( 'NEWS', 'a' ).close()
    open( 'README', 'a' ).close()
    open( 'AUTHORS', 'a' ).close()
    open( 'ChangeLog', 'a' ).close()

  def add_include_path(self,env,dep_name):
    include_path = self.spec[dep_name].prefix.include
    if not is_system_path(include_path):
       env.append_path('SPACK_INCLUDE_DIRS', include_path)

    # also add a possible confix repo
    self.add_confix_repo(dep_name)

  def add_confix_repo(self,dep_name):
    confix_repo_path = join_path( self.spec[dep_name].prefix, "share/confix-2.3.0/repo" )
    if os.path.exists(confix_repo_path):
       self.confix_prefixes.append( self.spec[dep_name].prefix )

