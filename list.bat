for %%i in (*.zip) do (
	7z x "%~dp0%%i"
)
pause

for %%i in (*.rar) do (
	7z x "%~dp0%%i"
)
pause