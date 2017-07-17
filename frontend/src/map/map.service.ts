import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable'

import extent from 'ol/extent';
import condition from 'ol/events/condition';
import loadingstrategy from 'ol/loadingstrategy';
import proj from 'ol/proj';

import View from 'ol/view';
import Map from 'ol/map';
import GeoJSON from 'ol/format/geojson';
import SelectInteraction from 'ol/interaction/select';

import BingMapsSource from 'ol/source/bingmaps';
import OSMSource from 'ol/source/osm';
import TileWMSSource from 'ol/source/tilewms';
import VectorSource from 'ol/source/vector';

import TileLayer from 'ol/layer/tile';
import VectorLayer from 'ol/layer/vector';

import Fill from 'ol/style/fill';
import Stroke from 'ol/style/stroke';
import Circle from 'ol/style/circle';
import Style from 'ol/style/style';
import Text from 'ol/style/text';

import { colorsHex, colorsRGB } from '../constants';
import { environment } from '../environments/environment';


const floorplanBaseURL = 'http://www.pdx.edu/floorplans/buildings/';
const epsg = 'EPSG:3857';
const projection = proj.get(epsg);
const mapExtent = [-13657661.739414563, 5700905.92043886, -13655116.88116592, 5702920.846916851];
const center = extent.getCenter(mapExtent);


@Injectable()
export default class MapService {
    baseLayers: Array<any>;
    map: Map;
    featureStream: Observable<any>;

    constructor () {}

    initMap (target) {
        const baseLayers = this.makeBaseLayers();
        const featureLayers = this.makeFeatureLayers();
        const allLayers = baseLayers.concat(featureLayers);

        const map = new Map({
            target: target,
            controls: [],
            layers: allLayers,
            view: new View({
                center: center,
                zoom: 16
            })
        });

        this.addInteractions(map, baseLayers, featureLayers);
        this.addEventListeners(map);
        map.getView().fit(mapExtent);
        this.map = map;
        return map;
    }

    makeBaseLayers () {
        return [
            new TileLayer({
                label: 'Map',
                shortLabel: 'Map',
                source: new BingMapsSource({
                    key: environment.map.bing.key,
                    imagerySet: 'CanvasLight'
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

    makeFeatureLayers () {
        return [
            this.makeFeatureLayer('buildings', {
                style: new Style({
                    fill: new Fill({
                        color: colorsRGB.psuGreen.concat([0.6])
                    }),
                    stroke: new Stroke({
                        color: [255, 255, 255, 0.8],
                        width: 2
                    })
                })
            }),
            this.makeTileLayer('bicycle-routes', {maxResolution: 2}),
            this.makeFeatureLayer('bicycle-parking', {
                style: new Style({
                    image: new Circle({
                        fill: new Fill({
                            color: 'white'
                        }),
                        stroke: new Stroke({
                            color: '#333',
                            width: 1
                        }),
                        radius: 10
                    }),
                    text: new Text({
                        font: '14px Material Icons',
                        fill: new Fill({
                            color: 'black'
                        }),
                        text: "directions_bike"
                    })
                }),
                maxResolution: 2 }
            )
        ];
    }

    makeFeatureLayer (layerName, options: {
        minResolution?: Number,
        maxResolution?: Number,
        style?: Style
    }) {
        return new VectorLayer({
            source: this.makeWFSSource(layerName),
            minResolution: options.minResolution,
            maxResolution: options.maxResolution,
            style: options.style
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

    makeTileLayer (layerName, options: {
        minResolution?: Number,
        maxResolution?: Number,
    }) {
        return new TileLayer({
            source: this.makeTileSource(layerName),
            minResolution: options.minResolution,
            maxResolution: options.maxResolution
        });
    }

    makeTileSource (layerName) {
        const wmsURL = `${environment.map.server.baseURL}/campusmap/wms`;

        return new TileWMSSource({
            serverType: 'geoserver',
            url: wmsURL,
            params: {
                LAYERS: `campusmap:${layerName}`
            }
        });
    }

    makeBuildingHighlighterInteraction (layer) {
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
                            color: colorsHex.psuGray
                        }),
                        stroke: new Stroke({
                            color: 'white',
                            width: 4
                        }),
                        text: new Text({
                            font: '20px sans-serif',
                            fill: new Fill({
                                color: colorsHex.psuGray
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

    makeBuildingSelectInteraction (layer) {
        return new SelectInteraction({
            condition: condition.pointerDown,
            layers: [layer],
            style: (feature) => {
                const props = feature.getProperties();
                const name = props.name;
                const code = props.code;
                let style = new Style({
                    fill: new Fill({
                        color: colorsHex.psuGray
                    }),
                    stroke: new Stroke({
                        color: 'white',
                        width: 4
                    }),
                });
                return [style];
            }
        });
    }

    addInteractions (map: Map, baseLayers, featureLayers) {
        const buildingSelector = this.makeBuildingSelectInteraction(
            featureLayers[0]);
        map.addInteraction(buildingSelector);
        const buildingHighlighter = this.makeBuildingHighlighterInteraction(
            featureLayers[0]);
        map.addInteraction(buildingHighlighter);

    }

    addEventListeners (map: Map) {
        let clickStream = Observable.fromEvent(map, 'click');
        this.featureStream = clickStream.map(
            (event) => {
                let feature = map.forEachFeatureAtPixel(
                    event['pixel'], (feature) => {
                        return feature;
                    });
                return feature;
        });
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

    moveMap (feature) {
        if (feature !== undefined) {
            // XXX: hardcoded width
            const sidenavWidth = 400;
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
        }
    }

    clearSelection () {
        const interactions = this.map.getInteractions();
        const selected = interactions.getArray().filter(
            (interaction) => interaction instanceof SelectInteraction
        );
        selected.map((select) => select.getFeatures().clear());
    }
}
