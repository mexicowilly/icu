common_shared_name = 'icuuc'
if target_machine.system() == 'windows'
  common_shared_name += icu_lib_major_version
endif
common_shared_name += library_suffix
common_static_name = 's' + common_shared_name

common_sources = run_command(python_exec,
                             '..' / 'meson' / 'lines_as_string.py',
                             'sources.txt').stdout().strip().split(' ')

common_args = [
  cpp_def + 'U_COMMON_IMPLEMENTATION',
  cpp_def + 'DEFAULT_ICU_PLUGINS=' + get_option('prefix') / get_option('libdir')
]
if get_option('data_packaging') == 'archive'
  common_args += cpp_def + 'ICU_DATA_DEFAULT_DIR=' + get_option('prefix') / get_option('datadir')
endif

# dirent.h
if not cpp_compiler.check_header('dirent.h')
  common_args += cpp_def + 'U_HAVE_DIRENT_H=0'
endif

# nl_langinfo CODESET
if cpp_compiler.check_header('langinfo.h') and cpp_compiler.has_function('nl_langinfo')
  langinfo_tmpl = '''#include <langinfo.h>
int main()
{
  nl_langinfo(@0@);
  return 0;
}'''
  if cpp_compiler.links(langinfo_tmpl.format('CODESET'))
    # Do nothing. This is the normal case.
  elif cpp_compiler.links(langinfo_tmpl.format('_NL_CTYPE_CODESET_NAME'))
    common_args += cpp_def + 'NL_LANGINFO_CODESET=_NL_CTYPE_CODESET_NAME'
  else
    common_args += cpp_def + 'U_HAVE_NL_LANGINFO_CODESET=0'
  endif
endif

# tzset
zero_or_one = '1'
if cpp_compiler.has_function('tzset')
    common_args += cpp_def + 'U_TZSET=tzset'
elif cpp_compiler.has_function('_tzset')
    common_args += cpp_def + 'U_TZSET=_tzset'
else
    zero_or_one = '0'
endif
common_args += cpp_def + 'U_HAVE_TZSET=' + zero_or_one

# tzname
zero_or_one = '1'
common_tzname_src = '''#ifndef _XOPEN_SOURCE
  #define _XOPEN_SOURCE
#endif
#include <stdlib.h>
#include <time.h>
#ifndef @0@
  extern char* @0@[];
#endif
int main()
{
  atoi(*@0@);
  return 0;
}'''
if cpp_compiler.links(common_tzname_src.format('tzname'))
  common_args += cpp_def + 'U_TZNAME=tzname'
elif cpp_compiler.links(common_tzname_src.format('_tzname'))
  common_args += cpp_def + 'U_TZNAME=_tzname'
else
  zero_or_one = '0'
endif
common_args += cpp_def + 'U_HAVE_TZNAME=' + zero_or_one

# timezone
timezone_src = '''#ifndef _XOPEN_SOURCE
#define _XOPEN_SOURCE
#endif
#include <time.h>
int main()
{
  @0@ = 1;
  return 0;
}'''
tz_var_name = ''
zero_or_one = '0'
foreach tz_try : [ 'timezone', '_timezone', '__timezone' ]
  if cpp_compiler.links(timezone_src.format(tz_try))
    tz_var_name = tz_try
    zero_or_one = '1'
    break
  endif
endforeach
common_args += cpp_def + 'U_HAVE_TIMEZONE=' + zero_or_one
if tz_var_name != ''
  common_args += cpp_def + 'U_TIMEZONE=' + tz_var_name
endif

common_deps = [ thread_dep, libdl_dep, libm_dep ]

if build_shared
  common_shared = shared_library(common_shared_name,
                                 common_sources,
                                 cpp_args : common_args,
                                 link_with : stubdata_shared,
                                 dependencies : common_deps,
                                 version : icu_version)
  common_shared_dep = declare_dependency(dependencies : common_deps,
                                         include_directories : include_directories('.'),
                                         link_with : common_shared)
else
  common_shared_dep = dependency('', required : false)
endif

if build_static
  common_static = static_library(common_static_name,
                                 common_sources,
                                 cpp_args : common_args + [ '-DU_STATIC_IMPLEMENTATION' ],
                                 link_with : stubdata_static,
                                 dependencies : common_deps)
  common_static_dep = declare_dependency(dependencies : common_deps,
                                         include_directories : include_directories('.'),
                                         link_with : common_static)
else
  common_static_dep = dependency('', required : false)
endif
