echo Starting extraction Apify API
echo Extracting ZION CHURCH - details
python3 ./social-media-insights/src/extract_data.py --type=details --account=zionsaopaulo

wait

echo Extracting ZION CHURCH - posts
python3 ./social-media-insights/src/extract_data.py --type=posts --account=zionsaopaulo

echo Ended Extraction
