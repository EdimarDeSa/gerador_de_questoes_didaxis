pyinstaller --noconfirm --onedir --windowed --name "gerador_de_questoes_didaxis" -i "C:\Users\Edimar\Documents\GitHub\gerador_de_questoes_didaxis\icons\prova.ico" --add-data "C:\Users\Edimar\Documents\GitHub\gerador_de_questoes_didaxis\.venv\Lib\site-packages\customtkinter;customtkinter" --paths "C:\Users\Edimar\Documents\GitHub\gerador_de_questoes_didaxis\.venv\Lib\site-packages" --distpath "C:\Users\Edimar\Documents\GitHub\gerador_de_questoes_didaxis\compilado\dist" --workpath "C:\Users\Edimar\Documents\GitHub\gerador_de_questoes_didaxis\compilado\build" --specpath "C:\Users\Edimar\Documents\GitHub\gerador_de_questoes_didaxis\compilado" --uac-admin main.py
robocopy "C:\Users\Edimar\Documents\GitHub\gerador_de_questoes_didaxis\configs" "C:\Users\Edimar\Documents\GitHub\gerador_de_questoes_didaxis\compilado\dist\gerador_de_questoes_didaxis\configs"
robocopy "C:\Users\Edimar\Documents\GitHub\gerador_de_questoes_didaxis\icons" "C:\Users\Edimar\Documents\GitHub\gerador_de_questoes_didaxis\compilado\dist\gerador_de_questoes_didaxis\icons"
powershell Compress-Archive -Path "C:\Users\Edimar\Documents\GitHub\gerador_de_questoes_didaxis\compilado\dist\gerador_de_questoes_didaxis" -DestinationPath "C:\Users\Edimar\Documents\GitHub\gerador_de_questoes_didaxis\compilado\dist\gerador_de_questoes_didaxis.zip"
