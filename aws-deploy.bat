@echo off
echo ========================================
echo AWS Flask API Deployment Script
echo ========================================

REM Check if AWS CLI is installed
aws --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: AWS CLI is not installed or not in PATH
    echo Please install AWS CLI first: https://aws.amazon.com/cli/
    pause
    exit /b 1
)

REM Check if logged into AWS
aws sts get-caller-identity >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Not logged into AWS
    echo Please run: aws configure
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Testing Flask app locally...
python -c "import app; print('Flask app imports successfully')"
if %errorlevel% neq 0 (
    echo ERROR: Flask app has import errors
    pause
    exit /b 1
)

echo.
echo Choose deployment method:
echo 1. AWS Lambda (Serverless)
echo 2. AWS EC2 (Traditional Server)
echo 3. AWS App Runner (Container)
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" goto lambda
if "%choice%"=="2" goto ec2
if "%choice%"=="3" goto apprunner

echo Invalid choice. Exiting...
pause
exit /b 1

:lambda
echo.
echo ========================================
echo Deploying to AWS Lambda
echo ========================================
echo.
echo Required files for Lambda deployment:
echo - serverless.yml (Serverless Framework config)
echo - lambda_function.py (Lambda handler)
echo.
echo Install Serverless Framework:
echo npm install -g serverless
echo serverless plugin install -n serverless-python-requirements
echo.
echo Then run: serverless deploy
echo.
pause
goto end

:ec2
echo.
echo ========================================
echo Deploying to AWS EC2
echo ========================================
echo.
echo Steps for EC2 deployment:
echo 1. Launch EC2 instance (Ubuntu/Amazon Linux)
echo 2. SSH to instance: ssh -i your-key.pem ec2-user@your-instance-ip
echo 3. Install Python: sudo yum install python3 pip3
echo 4. Upload files: scp -i your-key.pem -r . ec2-user@your-instance-ip:~/flask-api
echo 5. Install deps: pip3 install -r requirements.txt
echo 6. Run app (Production): gunicorn app:app -b 0.0.0.0:5000
echo.
echo For production, use supervisor or systemd service
echo.
pause
goto end

:apprunner
echo.
echo ========================================
echo Deploying to AWS App Runner
echo ========================================
echo.
echo Creating apprunner.yaml...
(
echo version: 1.0
echo runtime: python3
echo build:
echo   commands:
echo     build:
echo       - pip install -r requirements.txt
echo run:
echo   runtime-version: 3.9
echo   command: gunicorn app:app
echo   network:
echo     port: 5000
echo     env: PORT
) > apprunner.yaml

echo.
echo apprunner.yaml created successfully!
echo.
echo Next steps:
echo 1. Create GitHub repository with this code
echo 2. Go to AWS App Runner console
echo 3. Create service from GitHub repository
echo 4. Configure port 5000 and environment variables
echo.
pause
goto end

:end
echo.
echo ========================================
echo Deployment script completed!
echo ========================================
echo.
echo Environment Variables needed:
echo - GEMINI_API_KEY=your-gemini-api-key
echo - PORT=5000 (for App Runner/Lambda)
echo.
echo Model file location:
echo - Ensure models/best_model.pth exists
echo - Or update model path in app.py
echo.
pause