import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import 'rxjs/add/operator/map';
import { Observable } from 'rxjs/Observable';

import { environment } from '../environments/environment';

export interface SearchResult {
    id: Number,
    name: String
}

@Injectable()
export class SearchService {
    url = `${environment.apiURL}/search`;

    constructor (private http: Http) {

    }

    search (term): Observable<SearchResult[]> {
        return this.http
            .get(this.url, {params: {q: term}})
            .map(response => {
                return response.json().results as SearchResult[];
            })
            .catch(error => {
                if (error.status === 404) {
                    return Observable.of<any>([{error: error.statusText}]);
                }
                return Observable.throw("Search service error");
            });
    }
}
