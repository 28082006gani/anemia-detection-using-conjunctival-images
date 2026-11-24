param(
    [string]$Message = ""
)

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  AnemiaScan - Automatic GitHub Repository Sync" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

# Stage all changes
Write-Host "[1/3] Staging modified and new files..." -ForegroundColor Yellow
git add .

# Check if there are changes
$diff = git diff --cached --name-only
if (-not $diff) {
    Write-Host "[INFO] No changes to commit. Everything is already up to date!" -ForegroundColor Green
    return
}

# Determine commit message
if ([string]::IsNullOrWhiteSpace($Message)) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $Message = "Update AnemiaScan: $timestamp"
}

Write-Host "[2/3] Committing changes: '$Message'..." -ForegroundColor Yellow
git commit -m $Message

Write-Host "[3/3] Pushing to GitHub (main branch)..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================================" -ForegroundColor Green
    Write-Host "  [SUCCESS] Successfully pushed all updates to GitHub!" -ForegroundColor Green
    Write-Host "  Repo: https://github.com/28082006gani/anemia-detection-using-conjunctival-images" -ForegroundColor Green
    Write-Host "========================================================" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Git push failed. Please verify your credentials/connection." -ForegroundColor Red
}
