import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

import { AppToolbarComponent } from './toolbar.component';


describe('AppToolbarComponent Tests' , () => {

    let component: AppToolbarComponent;
    let fixture: ComponentFixture<AppToolbarComponent>;
    let testElement: DebugElement;
    let element: HTMLElement;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            declarations: [ AppToolbarComponent ],
            schemas: [ CUSTOM_ELEMENTS_SCHEMA ]
        }).compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(AppToolbarComponent);
        component = fixture.componentInstance;
        testElement = fixture.debugElement.query(By.all());
        element = testElement.nativeElement;
    });

    it('should contain a material toolbar', () => {
        expect(element.tagName.toLowerCase()).toEqual('md-toolbar');
    });

    it('should contain a link to pdx.edu', () => {
        expect(element.children[0].getAttribute('href')).toContain('pdx.edu');
    });
});
