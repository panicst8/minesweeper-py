# fixes some hard coded settings
LANG=C perl -pi -e 's/{PWD}/$ENV{PWD}/g' .vscode/settings.json

# get new repo name
REPO_NAME=${PWD##*/}

# create virtual environment
python3 -m venv .venv

# activate virtual environment
source .venv/bin/activate

# update sample test to point to new repo name
perl -pi -e "s|__REPO_NAME__|${REPO_NAME}|g" tests/test___REPO_NAME__.py

# rename some place holder directories and files
mv app/__REPO_NAME__.py app/${REPO_NAME}.py
mv tests/test___REPO_NAME__.py tests/test_${REPO_NAME}.py

# update pip
pip install --upgrade pip

# install requirements
pip install -r requirements_dev.txt

# remove the git repo from seed
rm -rf ./.git

# create new repo
git init .

# add current files to new repo
git add .

# initial commit
git commit -m 'initial commit'

cat <<++

You can now go and create this repo, then follow the instructions for
add to extisting repo it should look similar to this:

remote add origin https://github.com/<your user id>/<your repo name>.git
git push -u origin master

++
