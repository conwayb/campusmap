import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { MdSidenav } from '@angular/material';


import extent from 'ol/extent';
import condition from 'ol/events/condition';
import loadingstrategy from 'ol/loadingstrategy';
import proj from 'ol/proj';

import Map from 'ol/map';
import View from 'ol/view';

import GeoJSON from 'ol/format/geojson';

import SelectInteraction from 'ol/interaction/select';

import BingMapsSource from 'ol/source/bingmaps';
import OSMSource from 'ol/source/osm';
import VectorSource from 'ol/source/vector';

import TileLayer from 'ol/layer/tile';
import VectorLayer from 'ol/layer/vector';

import Fill from 'ol/style/fill';
import Stroke from 'ol/style/stroke';
import Style from 'ol/style/style';
import Text from 'ol/style/text';

import { environment } from '../environments/environment';

const floorplanBaseURL = 'http://www.pdx.edu/floorplans/buildings/';
const epsg = 'EPSG:3857';
const projection = proj.get(epsg);
const psuGreen = '#8c9516';
const psuGreenRGB = [140, 149, 22];
const mapExtent = [-13657661.739414563, 5700905.92043886, -13655116.88116592, 5702920.846916851];
const center = extent.getCenter(mapExtent);


interface FeatureInfo {
    name: String,
    code: String,
    buildingHref: String,
    address: String
}


@Component({
    selector: 'psu-campusmap-map',
    templateUrl: './map.component.html',
    styleUrls: [
        './map.component.scss'
    ]
})
export class MapComponent implements OnInit {
    name = 'PSU Campus Map';
    map: Map;
    baseLayers: Array<any>;
    featureInfo: FeatureInfo = <FeatureInfo>{};

    @ViewChild('sidenav')
    private sidenav: MdSidenav;

    constructor (private host: ElementRef) {
        // Pass
    }

    ngOnInit () {
        const baseLayers = this.makeBaseLayers();
        const layers = this.makeLayers();
        const allLayers = baseLayers.concat(layers);

        const map = new Map({
            target: this.host.nativeElement.querySelector('.map'),
            controls: [],
            layers: allLayers,
            view: new View({
                center: center,
                zoom: 16
            })
        });

        this.map = map;
        this.baseLayers = baseLayers;
        this.addEventListeners(map);
        this.addInteractions(map, baseLayers, layers);

        map.getView().fit(mapExtent);

        this.host.nativeElement.querySelector('.mat-sidenav-backdrop').remove();
    }

    makeBaseLayers () {
        return [
            new TileLayer({
                label: 'Map',
                shortLabel: 'Map',
                source: new BingMapsSource({
                    key: environment.map.bing.key,
                    imagerySet: 'Road'
                })
            }),
            new TileLayer({
                label: 'Satellite/Aerial',
                shortLabel: 'Satellite',
                visible: false,
                source: new BingMapsSource({
                    key: environment.map.bing.key,
                    imagerySet: 'Aerial'
                })
            }),
            new TileLayer({
                label: 'Hybrid',
                shortLabel: 'Hybrid',
                visible: false,
                source: new BingMapsSource({
                    key: environment.map.bing.key,
                    imagerySet: 'AerialWithLabels'
                })
            }),
            new TileLayer({
                label: 'OpenStreetMap',
                shortLabel: 'OSM',
                source: new OSMSource(),
                visible: false
            })
        ];
    }

    makeLayers () {
        return [
            this.makeFeatureLayer('buildings', new Style({
                fill: new Fill({
                    color: psuGreenRGB.concat([0.6])
                }),
                stroke: new Stroke({
                    color: [255, 255, 255, 0.8],
                    width: 2
                })
            }))
        ];
    }

    makeFeatureLayer (layerName, style?) {
        return new VectorLayer({
            source: this.makeWFSSource(layerName),
            style: style
        })
    }

    makeWFSSource (layerName) {
        const wfsURL = [
            `${environment.map.server.baseURL}/campusmap/wfs`, [
                'service=WFS',
                'version=1.1.0',
                'request=GetFeature',
                `srsname=${epsg}`,
                'outputFormat=application/json'
            ].join('&')
        ].join('?');

        return new VectorSource({
            format: new GeoJSON(),
            projection: projection,
            strategy: loadingstrategy.bbox,
            url: (extent) => {
                const bbox = `${extent.join(',')},${epsg}`;
                return `${wfsURL}&bbox=${bbox}&typename=campusmap:${layerName}`;
            }
        });
    }

    makeHighlighterInteraction (layer) {
        let selectCache = {};
        return new SelectInteraction({
            condition: condition.pointerMove,
            layers: [layer],
            style: (feature) => {
                const props = feature.getProperties();
                const name = props.name;
                const code = props.code;
                let style = selectCache[props.code];
                if (typeof style === 'undefined') {
                    selectCache[code] = style = new Style({
                        fill: new Fill({
                            color: psuGreen
                        }),
                        stroke: new Stroke({
                            color: 'white',
                            width: 4
                        }),
                        text: new Text({
                            font: '20px sans-serif',
                            fill: new Fill({
                                color: psuGreen
                            }),
                            stroke: new Stroke({
                                color: 'white',
                                width: 4
                            }),
                            text: code ? `${props.name} (${code})` : name,
                            textAlign: 'center'
                        })
                    });
                }
                return [style];
            }
        });
    }

    addEventListeners (map: Map) {
        map.on('click', (event) => {
            let feature = map.forEachFeatureAtPixel(event.pixel, (feature) => {
                return feature;
            });
            if (feature && typeof feature.getId() !== 'undefined') {
                this.showFeatureInfo(feature);
            }
            else {
                this.hideFeatureInfo();
            }
        })
    }

    addInteractions (map: Map, baseLayers, layers) {
        const highlighter = this.makeHighlighterInteraction(layers[0]);
        map.addInteraction(highlighter);
    }

    switchBaseLayer (layer) {
        const label = layer.get('label');
        this.baseLayers.forEach((layer) => {
            layer.set('visible', layer.get('label') === label);
        })
    }

    zoomIn (levels: number = 1) {
        this.zoomRelative(levels);
    }

    zoomOut (levels: number = 1) {
        this.zoomRelative(-levels);
    }

    zoomRelative (delta: number) {
        const view = this.map.getView();
        const currentZoom = view.getZoom();
        const newZoom = currentZoom + delta;
        view.setZoom(newZoom);
    }

    zoomToFullExtent () {
        this.map.getView().fit(mapExtent);
    }

    showFeatureInfo (feature) {
        const props = feature.getProperties();

        this.featureInfo = {
            name: props.name,
            code: props.code,
            buildingHref: `${floorplanBaseURL}${props.code.toLowerCase()}`,
            address: props.address
        };

        this.sidenav.open().then(() => {
            // XXX: Use of private property
            const sidenavWidth = this.sidenav._width;
            const threshold = sidenavWidth + (sidenavWidth * 0.1);

            const map = this.map;
            const mapView = map.getView();
            const center = extent.getCenter(feature.getGeometry().getExtent());
            const centerPixel = map.getPixelFromCoordinate(center);
            let x = centerPixel[0];
            const y = centerPixel[1];

            if (x < threshold) {
                x = x - (sidenavWidth / 2);
                mapView.animate({
                  center: map.getCoordinateFromPixel([x, y]),
                  duration: 400
                });
            }
        });
    }

    hideFeatureInfo () {
        // TBD
        this.sidenav.close();
    }
}
