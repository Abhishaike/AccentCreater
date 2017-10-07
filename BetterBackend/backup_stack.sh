#!/bin/bash
cd ~/Development/AccentCreater/BetterBackend
cd lambda_site-packages
echo "Compressing stack"
zip -r -q -9 stack.zip .
echo "Uploading stack"
aws s3 cp stack.zip s3://accent-analzyer-lambda-code/stack.zip
echo "Remove tmp files"
rm stack.zip