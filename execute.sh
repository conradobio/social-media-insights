echo Starting extraction Apify API
echo Extracting IC CAMPINAS - details
python3 ./src/apify-api.py --type=details --account=ic.campinas

echo Extracted IC CAMPINAS - details
wait

echo Extracting IC CAMPINAS - posts
python3 ./src/apify-api.py --type=posts --account=ic.campinas

echo Extracting IC SBC - details
python3 ./src/apify-api.py --type=details --account=ic.saobernardo

echo Extracted IC SBC - details
wait

echo Extracting IC SBC - posts
python3 ./src/apify-api.py --type=posts --account=ic.saobernardo