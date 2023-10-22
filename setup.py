from setuptools import setup

setup(
    name='EditorDeQuestoes',
    version='3.5.0',
    packages=['unitest', 'BackEndFunctions', 'BackEndFunctions.Errors', 'BackEndFunctions.DataClasses',
              'BackEndFunctions.FileManagerLib', 'FrontEndFunctions', 'FrontEndFunctions.Hints',
              'FrontEndFunctions.SetupFrames', 'FrontEndFunctions.SetupFrames.HelpFrame',
              'FrontEndFunctions.SetupFrames.OptionsTab', 'FrontEndFunctions.CustomFrames'],
    url='https://github.com/EdimarDeSa/gerador_de_questoes_didaxis',
    license='MIT',
    author='Edimar de Sá',
    author_email='edimar.sa@efscode.com.br',
    description='App criado para simplificar o processo de criar e gerir bancos de questoes xlsx usados na plataforma Didaxis',

)
