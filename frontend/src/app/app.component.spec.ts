import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

import { AppComponent } from './app.component';


describe('AppComponent Tests' , () => {

    let component: AppComponent;
    let fixture: ComponentFixture<AppComponent>;
    let testElement: DebugElement;
    let element: HTMLElement;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            declarations: [ AppComponent ],
            schemas: [ CUSTOM_ELEMENTS_SCHEMA ]
        }).compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(AppComponent);
        component = fixture.componentInstance;
        testElement = fixture.debugElement.query(By.all());
        element = testElement.nativeElement;
    });

    it('should contain the toolbar component', () => {
        expect(element.tagName.toLowerCase()).toEqual('psu-campusmap-toolbar');
    });

});
