import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Subject } from 'rxjs/Subject';
import { Observable } from 'rxjs/Observable'


const floorplanBaseURL = 'http://www.pdx.edu/floorplans/buildings/';

export interface FeatureInfo {
    name: String;
    code: String;
    buildingHref: String;
    address: String;
}

@Injectable()
export default class SidenavService {
    featureSubject: Subject<FeatureInfo>;
    featureInfo: FeatureInfo;

    constructor () {
        this.featureSubject = new Subject();
    }


    setFeatureInfo (feature): void {
        if (feature !== undefined) {
            const props = feature.getProperties();

            this.featureInfo = {
                name: props.name,
                code: props.code,
                buildingHref: `${floorplanBaseURL}${props.code.toLowerCase()}`,
                address: props.address
            };
            this.featureSubject.next(this.featureInfo);
        }
        else {
            this.featureSubject.next(null);
        }
    }

    getFeatureInfo (): Observable<any> {
        return this.featureSubject.asObservable()
    }

    hideFeatureInfo (): void {
        this.featureSubject.next(null);
    }

}
