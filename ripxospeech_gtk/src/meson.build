ripxospeech_gtk_sources = [
  'main.c',
  'ripxospeech_gtk-application.c',
  'ripxospeech_gtk-window.c',
]

ripxospeech_gtk_deps = [
  dependency('gtk4'),
  dependency('libadwaita-1', version: '>= 1.4'),
]

ripxospeech_gtk_sources += gnome.compile_resources('ripxospeech_gtk-resources',
  'ripxospeech_gtk.gresource.xml',
  c_name: 'ripxospeech_gtk'
)

executable('ripxospeech_gtk', ripxospeech_gtk_sources,
  dependencies: ripxospeech_gtk_deps,
       install: true,
)
