REM #########################################################
REM ### Earthshaker Windows Launcher with CMD Logging
REM ### Created By Scott Danesi
REM #########################################################

REM ### Variables [Change these for your project] ###########
set project_name=Earthshaker
set project_path=C:\GoogleDrive\earthshaker-aftershock
set output_path=C:\GoogleDrive\earthshaker-aftershock\stdout
set project_python_filename=earthshaker.py

REM ### System Variables [Do Not Change These] ##############
For /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
For /f "tokens=1-3 delims=/:/ " %%a in ('time /t') do (set mytime=%%a-%%b-%%c)
set mytime=%mytime: =% 
set filename=%project_name%_StdOut_%mydate%_%mytime%

REM ### Start Game ##########################################
python %project_path%\%project_python_filename% >> "%output_path%\%filename%.txt" 2>&1