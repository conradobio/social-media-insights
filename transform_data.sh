echo Starting Transformation Data

activate () {
    . ./social-media-insights/.venv/bin/activate
}
activate

echo Activate Virtual Env

echo Transforming Data
python3 ./social-media-insights/src/transform_data.py

echo Ended Transformation