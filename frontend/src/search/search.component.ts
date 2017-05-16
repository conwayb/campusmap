import { Component } from '@angular/core';

import { SearchService } from './search.service';

@Component({
    selector: 'psu-campusmap-search',
    templateUrl: './search.component.html',
    styleUrls: [
        './search.component.scss'
    ]
})
export class SearchComponent {
    term: String;

    constructor (private searchService: SearchService) {

    }

    search () {
        return this.searchService
            .search(this.term)
            .then(results => {
                console.log(results);
            })
            .catch(error => {
                console.log(error);
            })
    }
}
