from setuptools import setup

setup(
    name='WinDirectInput',
    version='1.3.9',
    author='AbdulRahim Khan',
    author_email='abdulrahimpds@gmail.com',
    description='A Windows-specific package for simulating keyboard and mouse inputs',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/abdulrahimpds/WinDirectInput',
    py_modules=['directinput'],
    install_requires=[
        'opencv-python',
        'numpy',
        'mss',
        'pyscreeze',
        'pillow',
        'pyperclip'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.8'
)
