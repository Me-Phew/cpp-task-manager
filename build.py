from py2exe import freeze

freeze(
    console=[{'script': 'ctm.py'}],
    windows=[],
    data_files=[],
    zipfile='library.zip',
    options={},
    version_info={}
)
