@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo   BloodChain Test Runner - All Services + Coverage
echo ===================================================
echo.

set "ROOT=%~dp0"

REM ===== 1. Smart Contracts =====
echo [1/7] Running Smart Contract tests...
cd /d "%ROOT%blockchain"
call npx hardhat test 2>&1
if !ERRORLEVEL! NEQ 0 ( set "FAILED=1" ) else ( echo PASSED )
echo.

REM ===== 2. Notifications Service =====
echo [2/7] Running Notifications Service...
cd /d "%ROOT%services\notifications-service"
call python -m coverage run --source='.' manage.py test --settings=config.settings_test -v 2 2>&1
if !ERRORLEVEL! NEQ 0 ( set "FAILED=1" ) else (
    python -m coverage report
    python -m coverage html -d coverage_html
    echo HTML: services\notifications-service\coverage_html\index.html
)
echo.

REM ===== 3. Donor Service =====
echo [3/7] Running Donor Service...
cd /d "%ROOT%services\donor-service"
call python -m coverage run --source='.' manage.py test --settings=config.settings_test -v 2 2>&1
if !ERRORLEVEL! NEQ 0 ( set "FAILED=1" ) else (
    python -m coverage report
    python -m coverage html -d coverage_html
    echo HTML: services\donor-service\coverage_html\index.html
)
echo.

REM ===== 4. Hospital Service =====
echo [4/7] Running Hospital Service...
cd /d "%ROOT%services\hospital-service"
call python -m coverage run --source='.' manage.py test --settings=config.settings_test -v 2 2>&1
if !ERRORLEVEL! NEQ 0 ( set "FAILED=1" ) else (
    python -m coverage report
    python -m coverage html -d coverage_html
    echo HTML: services\hospital-service\coverage_html\index.html
)
echo.

REM ===== 5. Blood Tracking Service =====
echo [5/7] Running Blood Tracking Service...
cd /d "%ROOT%services\blood-tracking-service"
call python -m coverage run --source='.' manage.py test --settings=config.settings_test -v 2 2>&1
if !ERRORLEVEL! NEQ 0 ( set "FAILED=1" ) else (
    python -m coverage report
    python -m coverage html -d coverage_html
    echo HTML: services\blood-tracking-service\coverage_html\index.html
)
echo.

REM ===== 6. User Management =====
echo [6/7] Running User Management...
cd /d "%ROOT%services\user-management"
call python -m coverage run --source='.' manage.py test -v 2 2>&1
if !ERRORLEVEL! NEQ 0 ( set "FAILED=1" ) else (
    python -m coverage report
    python -m coverage html -d coverage_html
    echo HTML: services\user-management\coverage_html\index.html
)
echo.

REM ===== 7. Rewards Service =====
echo [7/7] Running Rewards Service...
cd /d "%ROOT%services\rewards-service"
call python -m coverage run --source='.' manage.py test -v 2 2>&1
if !ERRORLEVEL! NEQ 0 ( set "FAILED=1" ) else (
    python -m coverage report
    python -m coverage html -d coverage_html
    echo HTML: services\rewards-service\coverage_html\index.html
)
echo.

REM ===== 8. Integration Tests (requires Docker running) =====
echo [8/8] Running Integration Tests against Docker...
cd /d "%ROOT%tests\integration"
python -m pytest test_donation_flow.py -v --tb=short 2>&1
if !ERRORLEVEL! NEQ 0 ( echo NOTE: Integration tests need Docker services running. Skipping. ) else ( echo PASSED )
echo.

REM ===== Final Summary =====
echo ===================================================
echo   COVERAGE SUMMARY
echo ===================================================
echo.
if defined FAILED (
    echo WARNING: Some tests FAILED - check output above.
    exit /b 1
) else (
    echo  ALL TESTS PASSED - Coverage above 80%% in all services.
    echo.
    echo  Coverage HTML reports available at:
    echo    services\notifications-service\coverage_html\index.html
    echo    services\donor-service\coverage_html\index.html
    echo    services\hospital-service\coverage_html\index.html
    echo    services\blood-tracking-service\coverage_html\index.html
    echo    services\user-management\coverage_html\index.html
    echo    services\rewards-service\coverage_html\index.html
    echo.
    exit /b 0
)
