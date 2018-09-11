import boto3
import sys
import click

session = boto3.Session(profile_name='awssnapshot')
ec2 = session.resource('ec2')


@click.command()
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 Instances"
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.private_ip_address,
            i.public_dns_name,
            tags.get('Project', '<no project>')
            )))

        return



if __name__ == '__main__':
    list_instances()
