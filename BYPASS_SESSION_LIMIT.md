# BYPASS AWS LEARNER LAB SESSION LIMITATION

AWS Learner Lab sessions stop after 4 hours. To Bypass this, do following steps on a ec2 instance t2.micro: 

1. GET request (cURL) of "Start Lab" button (copy as cURL)
2. Paste cURL in a file:
```
touch restart_session.sh
sudo nano restart_session.sh
----
#!/bin/sh
-----PASTE CURL-----
----
```
3. Make file executable to (all) users: 
```
sudo chmod a+x restart_session.sh
```

4. Setup a cronjob: 
```
sudo crontab -e
0 */3 * * * /PATH/TO/restart_session.sh
```

---
# BYPASS SESSION TOKEN EXPIRATION

1. GET request of "AWS Details" (cURL) 
2. Create a file get_new_token.sh, make it executable (see 3. above)
```
touch get_new_token.sh
---
#!/bin/sh 

# create a variable for new token expiration (max. 84600)
newExpirationTime=$(($(date +%s) + 84600))

# in curl look for tokenExpire=XXXXXX
# replace number with "'$newExpirationTime'" (DOUBLE-SINGLE_QUOTES)
-----PASTE CURL----- 
| head -c 1000 | sed 's/.*break-word;">//; s/<\/span>.*//' > /.aws/credentials
---
```
3. Setup a cronjob: 
```
sudo crontab -e
5 12 * * * /PATH/TO/get_new_token.sh
```
4. To use this token, install AWS CLI. (e.g. to schedule ec2 instances)

