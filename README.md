# AWS Snapshot Checker
This is a rudimentary python script to test the various boto3 commands against ec2 instances in AWS.
It includes things like list instances and list volumes etc, but predominantly created to manage snapshots on multiple instances based on their tag.

Pipenv was also used to house all the required installation files including boto3, boto3core, sys, click.

Use this script at your own risk as it could/may apply to all instances in your given region if not used carefully.

##Configuring
Script uses the config files created by the aws cli
'aws configure --profile awssnapshot'

'Project' is an AWS tag filter

awssnapshotter.py instances list
awssnapshotter.py volumes list
awssnapshotter.py snapshots create --Project=DEV
 
## Running

'pipenv run python awssnapshot/awssnapshotter.py <command>'
<--project=PROJECT TAG in AWS>"
*commands* is instances, volumes, or snapshots
*subcommand* is list, start, stop, create
*project* is optional
