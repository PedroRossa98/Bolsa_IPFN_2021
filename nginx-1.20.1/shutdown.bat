
:LOOP
tasklist | find /i "nginx.exe">nul  && Taskkill /F /IM  "nginx.exe" & exit/b
timeout /t 30
goto:LOOP