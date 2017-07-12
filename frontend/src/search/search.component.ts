import { Component, OnInit } from '@angular/core';

import 'rxjs/add/observable/of';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/debounceTime';
import 'rxjs/add/operator/distinctUntilChanged';
import 'rxjs/add/operator/switchMap';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';

import { SearchResult, SearchService } from './search.service';

@Component({
    selector: 'psu-campusmap-search',
    templateUrl: './search.component.html',
    styleUrls: [
        './search.component.scss'
    ],
    providers: [
        SearchService
    ]
})
export class SearchComponent implements OnInit {
    private searchTerms = new Subject<string>();

    results: Observable<SearchResult[]>;

    error: {
        status: number,
        message: string
    };

    constructor (private searchService: SearchService) {

    }

    ngOnInit (): void {
        this.results = this.searchTerms
            .debounceTime(300)
            .distinctUntilChanged()
            .switchMap(term => {
                if (term) {
                    return this.searchService.search(term)
                        .map(results => {
                            this.error = null;
                            return results;
                        })
                        .catch(error => {
                            this.error = error;
                            return Observable.of<SearchResult[]>([]);
                        });
                }
                this.error = null;
                return Observable.of<SearchResult[]>([]);
            })
    }

    search (term: string): void {
        this.searchTerms.next(term);
    }

    reset () {
        this.searchTerms.next(null);
    }
}
