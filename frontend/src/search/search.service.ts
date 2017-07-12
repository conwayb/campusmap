import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import 'rxjs/add/observable/throw';
import 'rxjs/add/operator/map';
import { Observable } from 'rxjs/Observable';

import { environment } from '../environments/environment';

export class SearchResult {
    id: number;
    name: string;
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
                let message;

                if (error.status === 404) {
                    message = `No results found for "${term}"`;
                } else {
                    message = 'Unable to search at this time';
                }

                return Observable.throw({
                    status: error.status,
                    message: message
                });
            });
    }
}
