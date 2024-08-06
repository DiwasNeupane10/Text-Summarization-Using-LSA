Create a virtual environment in the root of the directory
open powershell
Following commands:

  python -m venv venv
  
  venv/Scripts/Activate
  
If this gives error of wont activate on windows then open a new powershell as admin and run the following command

  Set-ExecutionPolicy Unrestricted -Force
  
Then run the latter commands again
