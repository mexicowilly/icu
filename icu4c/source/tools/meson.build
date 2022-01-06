# These libraries are fine to build in subdirectories
subdir('toolutil')
subdir('ctestfw')

# The tools must not use subdirectories for the build instructions. The
# Python data build tool requires that all tools are in the same directory.
foreach tool : [ 'makeconv', 'genrb', 'genbrk', 'gencnval', 'gensprep' ]
  tool_sources_raw = run_command(python_exec,
                                 '..' / 'meson' / 'lines_as_string.py',
                                 tool / 'sources.txt').stdout().strip().split(' ')
  tool_sources = [ ]
  foreach tool_source : tool_sources_raw
    tool_sources += tool / tool_source
  endforeach
  executable(tool,
             tool_sources,
             dependencies : [ toolutil_shared_dep, toolutil_static_dep ])
endforeach

if get_option('enable_icuio')
  executable('derb',
             'genrb/derb.cpp',
             dependencies : [ toolutil_shared_dep, toolutil_static_dep, io_shared_dep, io_static_dep ])
endif
