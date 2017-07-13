PSU Campus Map
++++++++++++++
A web-mapping application for navigating the PSU campus.

Stack
=====

Back End
--------

- PostgreSQL 9.4+
- PostGIS 2
- GeoServer 2.10
- Python 3.6
- Django 1.11
- Django REST Framework 3.6

Front End
---------

- TypeScript
- Angular 4
- OpenLayers 4

Setting up for development
==========================

First fork and clone the repo::

    git clone git@github.com:{your-username}/campusmap
    cd campusmap

The easiest way to get set up is to install Docker and then run ``make init.``
You can then run all service and application containers::

    docker-compose up

Or you can run just the services via Docker and run the back and front end
servers locally::

    docker-compose up postgres geoserver
    cd backend && make init && make run
    cd ../frontend && make init && make run

If you don't have or want to use Docker at all, you'll have to set up Postgres
and GeoServer manually, which is no fun (especially GeoServer).

Importing Data
==============

Some GIS data is stored in the git repo. The bicycle route data needs be
downloaded from Metro's RLIS Discovery site::

    http://rlisdiscovery.oregonmetro.gov/?action=viewDetail&layerID=3312

and extracted into ``gisdata/bicycle-routes``.

Then run the following command in the ``backend`` directory to import all
configured GIS data sources::

    run import-gis-data

If you've already imported some data, you can use the ``--overwrite`` flag to
overwrite it.

You can also import data for a specific Django app or model::

    run import-gis-data --app buildings
    run import-gis-data --app buildings --model building
    run import-gis-data --model buildings.building  # shortcut for preceding


GeoServer
=========

Unfortunately, you'll still need to go in and manually create some stuff in
GeoServer, but that's not *too* hard:

NOTE: This assumes you're running Postgres and GeoServer via Docker. If you're
not, some of this will need to be adjusted slightly.

- Navigate to ``http://localhost:8080/geoserver/web/``

- Log in as ``admin`` with password ``geoserver``

- Create a workspace named ``campusmap``

- Create a PostGIS store in the ``campusmap`` workspace named ``campusmap``

  - host: ``database`` (this is the host name configured via Docker Compose)
  - database: ``campusmap``
  - user: ``campusmap``
  - password: [leave blank]

- Create a ``buildings`` layer from ``campusmap:campusmap``

  - Find the ``buildings_building`` table in the list and click the ``Publish``
    link
  - Set the layer's name to ``buildings``
  - Set the layer's title to ``Buildings``
  - Click the ``Compute from data`` and ``Compute from native bounds`` links

- Create a ``bicycle-parking`` layer from ``campusmap:campusmap`` by repeating
  the above steps for the ``bicycles_bicycleroute`` table

- Create a ``bicycle-routes`` layer from ``campusmap:campusmap`` by repeating
  the above steps for the ``bicycles_bicycleroute`` table

  - Create a custom style by clicking on ``Add new style`` under ``Styles`` and
    upload the ``style.sld`` file from the repo.
  - Assign this style by setting Default style in the ``bicycle-routes``
    layer's Publishing options (under ``WMS Settings``).

Deployment
==========

Setup
-----

Currently, only deployment to staging is supported. To prepare for deployment,
copy the virtualhost config in ``etc/httpd/vhost.d/stage-vhost.conf`` to the
staging server then run the following command from the ``backend`` directory::

    run -e stage make-mod-wsgi-config

This creates a ``mod_wsgi-express`` configuration that runs an Apache instance
just for this site. It can be controlled with the ``mod-wsgi`` command (from
the ``backend`` directory)::

    run -e stage mod-wsgi <start|stop|restart>

Deploying
---------

To deploy back end code::

    cd backend && make deploy

To deploy front end code::

    cd frontend && make deploy
