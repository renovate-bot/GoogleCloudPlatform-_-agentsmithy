import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatTooltipModule} from '@angular/material/tooltip';
import { initializeApp, provideFirebaseApp } from '@angular/fire/app';
import { provideAuth, getAuth } from '@angular/fire/auth';
import { provideFirestore, getFirestore } from '@angular/fire/firestore';
import { environment } from '../environments/environment';
import { provideHttpClient } from "@angular/common/http";
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatMenuModule } from '@angular/material/menu';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {MatStepperModule} from '@angular/material/stepper';
import { MatFormFieldModule } from '@angular/material/form-field';
import { ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { ToastMessageComponent } from './common/components/toast-message/toast-message.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { CreateBotComponent } from './components/create-bot/create-bot.component';
import { HomeComponent } from './components/home/home.component';
import { PredefinedBotComponent } from './components/predefined-bot/predefined-bot.component';
import { FooterComponent } from './components/footer/footer.component';
import { CustomStepperComponent } from './components/custom-stepper/custom-stepper.component';
import { StepperCompComponent } from './components/stepper-comp/stepper-comp.component';
import { MatRadioModule } from '@angular/material/radio';
import { FormStepperComponent } from './components/form-stepper/form-stepper.component';
import { ConfigureBotComponent } from './components/configure-bot/configure-bot.component';
import { SpinnerComponent } from './components/spinner/spinner.component';
import { ExportComponent } from './components/export/export.component';

@NgModule({
  declarations: [
    AppComponent,
    ToastMessageComponent,
    CreateBotComponent,
    HomeComponent,
    PredefinedBotComponent,
    FooterComponent,
    CustomStepperComponent,
    StepperCompComponent,
    FormStepperComponent,
    ConfigureBotComponent,
    SpinnerComponent,
    ExportComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatTooltipModule,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatStepperModule,
    MatFormFieldModule,
    MatInputModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    MatSelectModule,
    MatProgressSpinnerModule,
    MatMenuModule,
    MatCheckboxModule,
    MatRadioModule
  ],
  providers: [
    provideClientHydration(),
    provideHttpClient(),
    provideFirebaseApp(() => initializeApp(environment.firebase)),
    provideAuth(() => getAuth()),
    provideFirestore(() => getFirestore()),
    provideAnimationsAsync(),
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
