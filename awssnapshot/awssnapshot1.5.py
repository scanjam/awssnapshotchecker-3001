import boto3
import sys
import click

session = boto3.Session(profile_name='awssnapshot')
ec2 = session.resource('ec2')

def filter_instances(project):
    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def cli():
    """AWS Snapshot Manager"""

@cli.group('snapshots')
def snapshots():
    """Commands for Snapshots"""

@snapshots.command('list')
@click.option('--project', default=None,
    help="Only snapshots for project (tag Project:<name>)")
def list_volumes(project):
    "List EC2 snapshots"

    instances = filter_instances(project)

    for i in instances:
     for v in i.volumes.all():
        for s in v.snapshots.all():
            print(", ".join((
             i.id,
             v.id,
             s.id,
             s.state,
             s.progress,
             s.start_time.strftime("%c"),
             )))

    return


@cli.group('volumes')
def volumes():
    """Commands for Volumes"""

@volumes.command('list')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_volumes(project):
    "List EC2 volumes"

    instances = filter_instances(project)

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        for v in i.volumes.all():
            print(", ".join((
                tags.get('Name', '<no name>'),
                i.id,
                v.id,
                v.state,
                str(v.size) + " Gib",
                v.encrypted and "Encrypted" or "Not Encrypted"
             )))

    return

@cli.group('instances')
def instances():
    """Commands for Instances"""

@instances.command('snapshot')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def create_snapshots(project):
    "Create Snapshots for EC2 Instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}..".format(i.id))

        i.stop()
        i.wait_until_stopped()

        for v in i.volumes.all():
            print("Creating Snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by Script - James")

        print("Starting {0}...".format(i.id))

        i.start()
        i.wait_until_running()
        print ("Started {0}...".format(i.id))

    print("Job's Done!")

    return

@instances.command('list')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 Instances"
    instances = filter_instances(project)

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        print(', '.join((
            tags.get('Name', '<no name>'),
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.private_ip_address,
            i.public_dns_name,
            tags.get('Project', '<no project>')
            )))

    return

@instances.command('stop')
@click.option('--project', default=None,
    help='Only instances for project')
def stop_instances(project):
    "Stop EC2 Instances"
    instances = filter_instances(project)


    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()

        return

@instances.command('start')
@click.option('--project', default=None,
    help='Only instances for project')
def start_instances(project):
    "Start EC2 Instances"
    instances = filter_instances(project)

    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()

        return

if __name__ == '__main__':
    cli()
