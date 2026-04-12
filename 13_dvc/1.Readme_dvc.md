## Practice
https://doc.dvc.org/command-reference/pull

-- sudo apt install unzip
-- install aws-cli on your machine
-- create access keys
-- aws configure

git init
git branch -m main
uv init
uv venv
activate the venv
uv add dvc dvc_s3

dvc init
dvc add data/wine_data.csv # notice a wine_data.csv.dvc file will be created

cat wine_data.csv.dvc
vi or edit the wine_data.csv file and save it

git add data/wine_data.csv.dvc data/.gitignore

dvc add data/wine_data.csv
cat data/wine_data.csv.dvc # compare before and after the md5 value will change

Create an s3 bucket let the same is demo-bucket
dvc remote add -d winedata s3://wine-related-data-299029453147-us-east-1-an 

dvc remote list

aws configure # get the keys and configure it
dvc push # check the data in s3
