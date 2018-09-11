# AWS Snapshot Checker
this is a demo file to test the various boto3 commands against ec2 instances in AWS.

##Configuring
Script uses the config files created by the aws cli
'aws configure --profile awssnapshot'


## Running

'pipenv run python awssnapshot/awssnapshot1.x.py <command>'
<--project=PROJECT TAG in AWS>"
*commands* is instances, volumes, or snapshots
*subcommand* is list, start, stop, create
*project* is optional
