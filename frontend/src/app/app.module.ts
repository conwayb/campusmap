import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { FlexLayoutModule } from '@angular/flex-layout';
import {
    MdButtonModule,
    MdCardModule,
    MdIconModule,
    MdInputModule,
    MdListModule,
    MdMenuModule,
    MdSidenavModule,
    MdToolbarModule
} from '@angular/material';

import { AppComponent } from './app.component';
import { AppToolbarComponent } from './toolbar.component';
import { MapComponent } from '../map/map.component';
import { SearchComponent } from '../search/search.component';
import { SearchService } from '../search/search.service';

@NgModule({
    imports: [
        BrowserModule,
        BrowserAnimationsModule,
        FormsModule,
        HttpModule,

        // Material
        FlexLayoutModule,
        MdButtonModule,
        MdCardModule,
        MdIconModule,
        MdInputModule,
        MdListModule,
        MdMenuModule,
        MdSidenavModule,
        MdToolbarModule
    ],
    declarations: [
        AppComponent,
        AppToolbarComponent,
        MapComponent,
        SearchComponent
    ],
    providers: [
        SearchService
    ],
    bootstrap: [
        AppComponent
    ]
})

export class AppModule { }
