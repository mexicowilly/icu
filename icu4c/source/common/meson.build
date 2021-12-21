common_shared_name = 'icuuc'
if build_machine.system() == 'windows'
  common_shared_name += icu_lib_major_version
endif
common_static_name = 's' + common_shared_name

common_sources = run_command(python_exec, '-c', 'print(open("sources.txt").read().splitlines())').stdout().strip()
