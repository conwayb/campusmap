var MY_MAP;
define([
    'jquery', 'ol', 'bootstrap'
], function ($, ol) {
    function transform (coords) {
        return ol.proj.transform(coords, geographicProjection, projection);
    };

    function transformExtent (extent) {
        return ol.proj.transformExtent(extent, geographicProjection, projection);
    };

    function LayerSwitcher (options) {
        var layers = options.layers,
            elAttrs = {id: 'map-layer-switcher', title: 'Select base map'},
            elClasses = 'ol-control ol-unselectable',
            el = $('<div>').attr(elAttrs).addClass(elClasses),
            select = $('<select>').addClass('form-control');
        this.layers = layers;
        el.append(select);
        for (var label, i = 0, len = layers.length; i < len; ++i) {
            label = layers[i].get('label');
            select.append($('<option>').val(label).text(label));
        }
        el.on('change', this.switchLayer.bind(this));
        ol.control.Control.call(this, {
            element: el[0]
        });
    }

    ol.inherits(LayerSwitcher, ol.control.Control);

    LayerSwitcher.prototype.switchLayer = function (event) {
        var el = $(event.target),
            label = el.val();
        for (var layer, i = 0, len = this.layers.length; i < len; ++i) {
            layer = this.layers[i];
            layer.set('visible', layer.get('label') === label);
        }
    };

    var projection = ol.proj.get('EPSG:3857'),
        geographicProjection = ol.proj.get('EPSG:4326'),
        extent = [-13657661.739414563, 5700905.92043886, -13655116.88116592, 5702920.846916851],
        center = ol.extent.getCenter(extent),
        psuGreen = '#8c9516',
        psuGreenRGB = [140, 149, 22],
        baseLayers = [
            new ol.layer.Tile({
                label: 'Map',
                source: new ol.source.MapQuest({layer: 'osm'})
            }),
            new ol.layer.Tile({
                label: 'Satellite',
                visible: false,
                source: new ol.source.MapQuest({layer: 'sat'})
            }),
            new ol.layer.Group({
                label: 'Hybrid',
                visible: false,
                layers: [
                    new ol.layer.Tile({
                        source: new ol.source.MapQuest({layer: 'sat'})
                    }),
                    new ol.layer.Tile({
                        source: new ol.source.MapQuest({layer: 'hyb'})
                    })
                ]
            }),
            new ol.layer.Tile({
                label: 'OpenStreetMap',
                visible: false,
                source: new ol.source.OSM()
            })
        ],
        layers = [
            //new ol.layer.Tile({
            //    source: new ol.source.TileWMS({
            //        url: 'http://gis.rc.pdx.edu:6080/arcgis/services/arc/campus_map/MapServer/WMSServer',
            //        params: {
            //            layers: '4'
            //        }
            //    })
            //}),
            new ol.layer.Vector({
                source: new ol.source.ServerVector({
                    format: new ol.format.WFS(),
                    loader: function (extent) {
                        var url = [
                            'http://gis.rc.pdx.edu/arcgis/services/arc/campus_map/MapServer/WFSServer', [
                                'service=WFS',
                                'version=1.1.0',
                                'request=GetFeature',
                                'typename=arc_campus_map:Buildings',
                                'srsname=EPSG:3857',
                                //'bbox=' + extent.join(',') + ',EPSG:3857',
                                'filter=<ogc:Filter><ogc:Not><ogc:PropertyIsEqualTo><ogc:PropertyName>BUILDINGID</ogc:PropertyName><ogc:Literal></ogc:Literal></ogc:PropertyIsEqualTo></ogc:Not></ogc:Filter>'
                            ].join('&')
                        ].join('?')

                        $.ajax({
                            url: url,
                            success: function (data) {
                                var features = this.readFeatures(data);
                                if (features) {
                                    this.addFeatures(features);
                                }
                            }.bind(this)
                        });
                    },
                    projection: projection,
                    strategy: ol.loadingstrategy.createTile(new ol.tilegrid.XYZ({ maxZoom: 19 }))
                }),
                style: new ol.style.Style({
                    fill: new ol.style.Fill({
                        color: psuGreenRGB.concat([0.6])
                    })
                })
            })
        ];

    function Map (options) {
        ol.Map.call(this, options);

        // Feature popup
        this.featurePopupEl = $('<div>');
        this.featurePopup = new ol.Overlay({
            element: this.featurePopupEl[0],
            position: this.getView().getCenter(),
            positioning: 'center-center'
        });
        this.addOverlay(this.featurePopup);
    }

    ol.inherits(Map, ol.Map);

    Map.prototype.showFeaturePopup = function (feature) {
        this.featurePopupEl.popover('destroy');
        if (feature && typeof feature.getId() !== 'undefined') {
            var geom = feature.getGeometry(),
                centroid = ol.extent.getCenter(geom.getExtent()),
                props = feature.getProperties(),
                buildingCode = props.BUILDINGID,
                title = [props.LONGNAME, ' ', '(', buildingCode, ')'].join(''),
                buildingHref = ['http://www.pdx.edu/floorplans/buildings/', buildingCode.toLowerCase()].join(''),
                content = [];
            if (props.BLDG_ADDR) {
                var addr = props.BLDG_ADDR.split(' ');
                for (var word, i = 0, len = addr.length; i < len; ++i) {
                    word = addr[i];
                    // XXX: It would be nice the addresses were stored
                    // in the standard format instead of all upper case.
                    // This following works okay-ish.
                    if (i === 1) {
                        word = word.toUpperCase();
                    } else {
                        word = [word.charAt(0).toUpperCase(), word.substr(1).toLowerCase()].join('');
                    }
                    addr[i] = word;
                }
                addr = addr.join(' ');
                content.push(
                    '<p>', addr, '</p>',
                    '<p><a href="', buildingHref, '">Building info & floorplans</a>');
            }
            content = content.join('');
            this.featurePopup.setPosition(centroid);
            this.featurePopupEl.popover({
                animation: false,
                placement: 'top',
                html: true,
                title: title,
                content: content
            });
            this.featurePopupEl.popover('show');
        }
    };

    Map.prototype.hideFeaturePopup = function () {
        this.featurePopupEl.popover('destroy');
    };

    var map = new Map({
        target: 'map',
        controls: ol.control.defaults().extend([
            new ol.control.ScaleLine(),
            new ol.control.ZoomToExtent({
                extent: extent,
                tipLabel: 'Zoom to PSU campus'
            }),
            new LayerSwitcher({layers: baseLayers})
        ]),
        layers: baseLayers.concat(layers),
        view: new ol.View({
            center: center,
            zoom: 16
        })
    });

    var selectCache = {},
        highlighter = new ol.interaction.Select({
            condition: ol.events.condition.pointerMove,
            layers: [
                layers[0]
            ],
            style: function (feature, resolution) {
                var props = feature.getProperties(),
                    code = props.BUILDINGID,
                    style = selectCache[code];
                if (typeof style === 'undefined') {
                    selectCache[code] = style = new ol.style.Style({
                        fill: new ol.style.Fill({
                            color: psuGreen
                        }),
                        stroke: new ol.style.Stroke({
                            color: '#fff',
                            width: 2
                        }),
                        text: new ol.style.Text({
                            font: '20px sans-serif',
                            fill: new ol.style.Fill({
                                color: psuGreen
                            }),
                            stroke: new ol.style.Stroke({
                                color: '#fff',
                                width: 4
                            }),
                            text: [props.LONGNAME, ' ', '(', code, ')'].join(''),
                            textAlign: 'center'
                        })
                    });
                }
                return [style];
            }
        });

    map.addInteraction(highlighter);

    map.on('singleclick', function (event) {
        var feature = this.forEachFeatureAtPixel(event.pixel, function (feature) {
            return feature;
        });
        if (feature) {
            map.showFeaturePopup(feature);
        } else {
            map.hideFeaturePopup();
        }
    });

    map.getView().fitExtent(extent, map.getSize());
});
