$requests = 100
while($true) {
    $requests += Get-Random -Minimum 5 -Maximum 25
    $body = "srefinal_requests_total{pod=`"srefinal-app-fake`",namespace=`"srefinal-prod`"} $requests`n"
    try {
        Invoke-WebRequest -Uri "http://localhost:9090/api/v1/write" -Method Post -Body $body -UseBasicParsing -ErrorAction SilentlyContinue
    } catch {}
    Write-Host "Отправлена метрика: srefinal_requests_total = $requests"
    Start-Sleep -Seconds 1
}