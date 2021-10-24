echo off
& $env:pybase E:\Project\ML_and_DL\CBD\Chatbot\Database\laptop_price_database.py
Start-Sleep -s 5
& $env:pybase E:\Project\ML_and_DL\CBD\Chatbot\Database\order_record_database.py
Write-Output "Start creating chart which is extracted from "Order record" database."
Start-Sleep -s 5
& $env:pybase E:\Project\ML_and_DL\CBD\Chatbot\Chart\plot_order_record.py
Start-Sleep -s 5
& $env:pybase E:\Project\ML_and_DL\CBD\Chatbot\Report\generate_analytic_report.py
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" "E:\Project\ML_and_DL\CBD\Chatbot\Report\Analytical Report.pdf"
pause

