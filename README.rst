PSU Campus Map
++++++++++++++
A web-mapping application for navigating the PSU campus.

Application Stack
=================

Frontend: Angular 4

Backend: Django 1.11 (with DRF)

Database: Postgresql 9.6/POSTGIS

GIS/Map server: Geoserver

Setting up for development
=========================

The easiest way to get set up is to install Docker and then run ``make init.``
You can then choose to run all the application containers in docker by running ``docker-compose up.``

You may choose to run the frontend or backend application locally. Run ``make init`` in each subdirectory to initialize the application locally. Run ``make run`` in the subdirectory to start the the application.


Importing Data
==============

GIS data is stored in the git repo. The bicycle route data needs be
downloaded from Metro's RLIS Discovery site first:

    http://rlisdiscovery.oregonmetro.gov/?action=viewDetail&layerID=3312

and extracted into ``./gisdata/bicycle-routes``.

Then run the following command from the backend application context: `run import-gis-data`.

GeoServer
=============

Unfortunately, you'll still need to go in and manually create some stuff
in GeoServer, but that's not *too* hard:

- Go to http://localhost:8080/geoserver/web/
- Log in with username ``admin`` and password ``geoserver``
- Create a workspace named ``campusmap``
- Create a PostGIS store in the ``campusmap`` workspace named ``campusmap``
  - host: ``database`` (this is the host name configured via Docker Compose)
  - database: ``campusmap``
  - user: ``campusmap``
  - password: [leave blank]
- Create a `buildings` layer from ``campusmap:campusmap``
  - Find the ``buildings_building`` table in the list and click the ``Publish`` link
  - Set the layer's name to ``buildings``
  - Set the layer's title to ``Buildings``
  - Click the ``Compute from data`` and ``Compute from native bounds`` links
- Create a ``bicycle-parking`` layer from ``campusmap:campusmap` by repeating the above steps using the ``bicycles_bicycleroute`` table.
- Create a ``bicycle-routes`` layer from ``campusmap:campusmap``
  - Follow the above steps to create the layer from the database store.
  - Create a custom style by clicking on ``Add new style`` under ``Styles`` and upload the ``style.sld`` file from the repo.
  - Assign this style by setting Default style in the ``bicycle-routes`` layer's Publishing options (under ``WMS Settings``).


### Front End Tools

This app uses the ng cli tool to serve the frontend static site. Run ``make run`` in the frontend subdirectory or run ``npm start``. Other npm scripts are available; see package.json under ``scripts``.
