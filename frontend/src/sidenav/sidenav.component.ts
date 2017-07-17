import { Component, OnInit, ViewChild } from '@angular/core';
import {Subscription} from 'rxjs/Subscription';
import { MdSidenav } from '@angular/material';
import { FeatureInfo }from './sidenav.service';
import SidenavService from './sidenav.service';
import MapService from '../map/map.service';

@Component({
    selector: 'sidenav',
    templateUrl: './sidenav.component.html',
    styleUrls: [
        './sidenav.component.scss'
    ],
})
export class SidenavComponent  {
    features: FeatureInfo;
    subscription: Subscription;

    @ViewChild('sidenav')
    private sidenav: MdSidenav;

    constructor (
        private sidenavService: SidenavService,
        private mapService: MapService
    ){
        this.features = null;
        this.subscription = this.sidenavService.getFeatureInfo().subscribe(
            feature => {
                this.features = feature;
                this.setSidenavState();
            });
    }

    setSidenavState (): void {
        if (this.features) {
            this.sidenav.open();
        }
        else {
            this.sidenav.close();
        }
    }

    hideSidenav (): void {
        this.features = null;
        this.setSidenavState();
        this.mapService.clearSelection();
    }
}
