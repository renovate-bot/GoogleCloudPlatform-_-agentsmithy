import { Component } from '@angular/core';
import { Router } from "@angular/router";
import { TEMPLATE_NAMES } from '../../environments/contants';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
})
export class HomeComponent {

  templates = TEMPLATE_NAMES;
  constructor(public router: Router){}

  routeToCreateBot(templateId?: string){
    if(templateId) this.router.navigate(["create-bot/"+templateId]);
    else this.router.navigate(["create-bot"])
  }
}
