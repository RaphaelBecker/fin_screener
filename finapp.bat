set bat_patch=%~dp0
cmd /k "%bat_patch%activate.bat & call streamlit run login.py & exit"