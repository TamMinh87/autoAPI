### How to run ###

## Prepare environment ##

* install python (3.6+)
* special case for Debian-based Linux distros:
    * install packages:`python python-dev python-libxml2 libxml2-dev python-libxslt1 libxslt1-dev libjpeg-dev zlib1g-dev`
* for MacOs install `libxml` and `libxslt` by brew or another package manager
* install virtualenv see https://virtualenv.pypa.io/en/latest/installation.html (preferred)
* checkout this repository from the bitbucket, cd to repo directory
```
```    
* activate virtualenv 
```
    virtualenv -p python3.6 .env
    source .env/bin/activate
```
* install requirements
```
    pip install -r requirements.txt
```
* create file env.ini from file _env.ini in folder config/
```
    cp config/_env.ini config/env.ini
```

if you need html reports locally

* install JDK >= 1.7 (allure requires jdk >= 1.7)
* install allure see http://wiki.qatools.ru/display/AL/Allure+Commandline


## run tests ##

For running tests command `py.test` is used. To find out actual info about options and parameters, 
just use `py.test --help`. Basically, the command for running tests looks like 
```
    pytest <tests_path> -s --alluredir=output <opts> 
 
```
where `tests_path` is like `tests/twitch` and `opts` are component-specific options.

Available options:

* `--env=` if used, then staging of the corresponding venture will be tested. Actual values can be found in config/env.ini
* `--db_host=` - database hostname
* `--db_user=` - user who can connect to database
* `--db_password=` - database user password

Actual list of command-line parameters see at `tests/conftest.py:option_list`.

All parameters can be filled  up in the [local] section in the `env.ini` filed

## usage ##

* develop a test, put it to correct service
* run test
```
    pytest --api_url=http://api.greentech-vn.com tests/api/rewards/ --alluredir=output
```
* generate report
```
    allure generate output
```
where `output` is the directory which is defined at `--aluredir` option when running test
* open report
```
    allure report open
```
