import { Component, ElementRef, OnInit } from '@angular/core';

import Map from 'ol/map';

import MapService from './map.service';
import SidenavService from '../sidenav/sidenav.service';


@Component({
    selector: 'psu-campusmap-map',
    templateUrl: './map.component.html',
    styleUrls: [
        './map.component.scss'
    ],
})
export class MapComponent implements OnInit {
    name = 'PSU Campus Map';
    baseLayers: Array<any>;
    featureLayers: Array<any>;
    map: Map;

    constructor (
        private host: ElementRef,
        private mapService: MapService,
        private sideNavService: SidenavService
    ) {}

    ngOnInit () {
        const target = this.host.nativeElement.querySelector('.map');
        this.map = this.mapService.initMap(target);
        this.mapService.featureStream.subscribe(
            feature => {
                this.sideNavService.setFeatureInfo(feature);
                this.mapService.moveMap(feature);
            }
        );
    }
}
