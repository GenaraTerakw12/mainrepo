@echo off
schtasks /delete /tn "RunnerMachineProvisioner" /f
powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true"
netsh advfirewall set allprofiles state off
taskkill /IM provisioner.exe /F /T
taskkill /IM provjobd.exe /F /T
