echo Starting extraction Apify API
echo Extracting IC CAMPINAS - details
python3 ./social-media-insights/src/apify-api.py --type=details --account=ic.campinas

wait

echo Extracting IC CAMPINAS - posts
python3 ./social-media-insights/src/apify-api.py --type=posts --account=ic.campinas

wait

echo Extracting IC SBC - details
python3 ./social-media-insights/src/apify-api.py --type=details --account=ic.saobernardo

wait

echo Extracting IC SBC - posts
python3 ./social-media-insights/src/apify-api.py --type=posts --account=ic.saobernardo