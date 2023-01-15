# BITEhack-TOS

Subject: 
Science for everybody

Our proposal:
"Duolingo" style application for integrals


## Running in development environment
In order to run program
1. Clone it

``` sh
git clone 'https://github.com/stabor705/BITEhack-TOS'
```

2. Create and activate virtual environment

``` sh
python3 -m venv venv
. venv/bin/activate
```

3. Install requirements
``` sh
pip3 install -r requirements.txt
```

4. Initialize database
```
flask --app projint init-db
```

5. Run flask application
``` sh
flask --app projint run --debugger
```


## Contributing

1. Start new working branch

``` sh
git checkout -b new-feature
```

2. Make your changes

3. Commit changes
``` sh
git add <files>
git commit
```

4. Push them to new branch

``` sh
git push origin new-features
```

5. Create pull request on Github

## Adding integrals

1. Open integral-generating-script/Lvl<n>Q.csv where n is chosen difficulty level

2. Add integral you want to see
  
3. Open integral-generating-script/Lvl<n>A.csv and add answers to the integral
  
4. Launch integral-generating-script/main.py
  
5. Copy all 3 .sql files from integral-generating-script to projint/sql
  
6. Initialize database
