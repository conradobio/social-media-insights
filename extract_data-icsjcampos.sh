echo Starting extraction Apify API
echo Extracting IC SÃO JOSE DOS CAMPOS - details
python3 ./social-media-insights/src/extract_data.py --type=details --account=ic.sjcampos

wait

echo Extracting IC SÃO JOSE DOS CAMPOS - posts
python3 ./social-media-insights/src/extract_data.py --type=posts --account=ic.sjcampos

