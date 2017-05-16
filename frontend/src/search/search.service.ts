import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { environment } from '../environments/environment';

@Injectable()
export class SearchService {
    url = `${environment.apiURL}/search`;

    constructor (private http: Http) {

    }

    search (term): Promise<any> {
        const params = {
            q: term
        };
        const options = {
            params: params
        };
        return this.http
            .get(this.url, options).toPromise()
            .then(response => response.json().data)
            .catch(error => Promise.reject(error));
    }
}
