# jenkins-script-demo

-----------
### Setup
Please consider using a [virtualenv](https://virtualenv.pypa.io/en/stable/installation/), setup your virtualenv and then all you have to do is:

`pip install -r requirments.txt`

Now you need to point the script to your jenkins instance with your correct credentials in the [defaults.json file](https://github.com/felfel/jenkins-script-demo/blob/master/defaults.json)
or feel free to use the optional command line arguments.
Then simply run the script

`python run_demo.py`

-----------
### Optional arguments:

+ -h, --help :
  
  show this help message and exit

+ -ha http_address, --httpAddress http_address

  Http address of the jenkins server

+ -hp http_address, --httpPort http_address

  Http port of the jenkins server
   
+ -u username, --username username

  Username to authenticate with jenkins server
   
+ -ps password, --password password

  Password to authenticate with jenkins server
   
+ -d, --dummy           

  Use this flag if you want dummy jobs to be created automatically, for testing purposes ofcourse
 
-------------
