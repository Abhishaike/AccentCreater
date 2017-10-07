#!/bin/bash
cd ~/Development/AccentCreater/BetterBackend
source ./environments/analyzer/bin/activate
echo "Activated Environment"
mkdir lambda_package
# rm requirements.txt
# pip freeze>requirements.txt
# pip install -r requirements.txt -t ./lambda_package
cp -r lambda_site-packages/ ./lambda_package
echo "Copied packages"
cp accent_analyzer.py ./lambda_package
cp lambda_function.py ./lambda_package
echo "Copied code"
cp -r ffmpeg/ ./lambda_package/ffmpeg
echo "Copied ffmpeg"
cp AccentEncoder.pkl ./lambda_package
cp LSTM_MODEL_ARCHITECTURE_WEIGHTS.h5 ./lambda_package
echo "Copied analyzer files"
cd lambda_package
echo "Compressing package"
zip -r -9 -q lambda_package.zip .
mv lambda_package.zip ~/Development/AccentCreater/BetterBackend
echo "Zipped and moved package"
cd ~/Development/AccentCreater/BetterBackend
aws s3 cp lambda_package.zip s3://accent-analzyer-lambda-code/lambda_package.zip
echo "Uploaded package to bucket"
aws lambda update-function-code --function-name AccentAnalzyer_Analysis --s3-bucket accent-analzyer-lambda-code --s3-key lambda_package.zip
echo "Updated lambda code"
rm lambda_package.zip
rm -rf lambda_package
echo "Deleted zip and folder"
deactivate