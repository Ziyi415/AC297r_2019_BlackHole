from setuptools import setup
APP = ['mainPage.py']
DATA_FILES = ['data/baseline_length_default.csv','data/single_tele_default.csv', 'icons/folder.png', 'images/eht.png']
OPTIONS = {
    # 'iconfile':'logoapp.icns',
    'argv_emulation': True,
    'packages': ['certifi'],
}
setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)