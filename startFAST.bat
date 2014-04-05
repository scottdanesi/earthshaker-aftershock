cd C:\GoogleDrive\earthshaker-aftershock
For /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
For /f "tokens=1-3 delims=/:/ " %%a in ('time /t') do (set mytime=%%a-%%b-%%c)
set mytime=%mytime: =% 
set FileName=EarthshakerStdOut_%mydate%_%mytime%
python earthshaker.py >> "stdout\%FileName%.txt"
pause