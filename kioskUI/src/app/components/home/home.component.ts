import { Component, OnInit, SecurityContext } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {

constructor(public router: Router, private domSanitizer: DomSanitizer, private matIconRegistry: MatIconRegistry) { 

  this.matIconRegistry.addSvgIcon(
    'spark',
    this.domSanitizer.bypassSecurityTrustResourceUrl('assets/images/spark.svg')
  );

  this.matIconRegistry.addSvgIcon(
    'spark-shine',
    this.domSanitizer.bypassSecurityTrustResourceUrl('assets/images/spark-shine.svg')
  );

}

  routeToCreateBot(templateId?: string) {
    if (templateId)
      this.router.navigate(["create-bot/" + templateId]);
    else
      this.router.navigate(["create-bot"])
  }

  routeToPrebuiltBot(templateId?: string) {
    if (templateId)
      this.router.navigate(["predefined-bot/" + templateId]);
    else
      this.router.navigate(["predefined-bot"])
  }
}
