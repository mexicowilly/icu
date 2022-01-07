# These libraries are fine to build in subdirectories
subdir('toolutil')
subdir('ctestfw')

# TODO: Figure out the plugin test in icuinfo
# TODO: Figure out the table generator and tests in escapesrc

# The tools must not use subdirectories for the build instructions. The
# Python data build tool requires that all tool executables reside in
# the same directory.
foreach tool : [ 'makeconv', 'genrb', 'genbrk', 'gencnval', 'gensprep', 'icuinfo',
                 'genccode', 'gencmn', 'icupkg', 'pkgdata', 'gentest', 'gennorm2',
                 'gencfu', 'gendict', 'icuexportdata', 'escapesrc' ]
  tool_sources = [ ]
  tool_args = [ ]
  tool_deps = [ toolutil_shared_dep, toolutil_static_dep ]
  tool_include_directories = [ ]

  if tool == 'escapesrc'
    tool_sources = [ 'escapesrc/escapesrc.cpp' ]
    tool_deps = [ libdl_dep, libm_dep ]
    tool_include_directories = [ '..' / 'common' ]
  else
    tool_sources_raw = run_command(python_exec,
                                   '..' / 'meson' / 'lines_as_string.py',
                                   tool / 'sources.txt').stdout().strip().split(' ')
    foreach tool_source : tool_sources_raw
      tool_sources += tool / tool_source
    endforeach
  endif

  if tool == 'genccode'
    if cpp_compiler.check_header('elf.h')
      tool_args += [ cpp_def + 'U_HAVE_ELF_H=1' ]
    endif
  elif tool == 'pkgdata'
    tool_args += [ cpp_def + 'UDATA_SO_SUFFIX=".' + (target_machine.system() == 'windows' ? 'dll' : 'so') + '"' ]
  endif

  executable(tool,
             tool_sources,
             cpp_args : tool_args,
             dependencies : tool_deps,
             include_directories : tool_include_directories)
endforeach

if get_option('enable_icuio')
  executable('derb',
             'genrb/derb.cpp',
             dependencies : [ toolutil_shared_dep, toolutil_static_dep, io_shared_dep, io_static_dep ])
endif
