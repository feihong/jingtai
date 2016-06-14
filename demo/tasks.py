from invoke import task
from jingtai import Site


site = Site('/jingtai/')


@task
def serve(ctx):
    site.serve(port=8000)


@task
def build(ctx):
    site.build()


@task
def clean(ctx):
    site.clean()


@task
def publish(ctx):
    site.publish()
