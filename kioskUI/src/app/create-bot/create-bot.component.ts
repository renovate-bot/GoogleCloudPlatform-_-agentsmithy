import { Component, ViewChild, ElementRef, inject} from '@angular/core';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatStepper } from '@angular/material/stepper';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import * as FileSaver from 'file-saver';
import { TEMPLATE_NAMES } from '../../environments/contants';
import {ActivatedRoute} from '@angular/router';

enum ProjectFormKeys {
  PROJECT_ID = 'project_id',
  REGION = 'region',
  CHATBOT_TEMPLATE = 'chatbot_template',
  FIREBASE_PROJECT_ID = 'firebase_project_id',
  FIREBASE_API_KEY = 'api_key',
  FIREBASE_AUTH_DOMAIN = 'auth_domain',
  CHATBOT_NAME = 'chatbot_name',
}

const BASE_URL = "https://mail.google.com/mail/?view=cm&fs=1&";
const EMAIL_SUBJET = "[Quick Bot] Request access to repository";

@Component({
  selector: 'app-create-bot',
  templateUrl: './create-bot.component.html',
  styleUrl: './create-bot.component.scss'
})
export class CreateBotComponent {
  @ViewChild('stepper') stepper: MatStepper | undefined;
  @ViewChild("fileInput") fileInput?: ElementRef;

  protected readonly projectFormKeys = ProjectFormKeys;
  protected projectForm: any;
  protected addFirebaseConfig = false;
  protected regionList = [
    "africa-south1",
    "asia-east1",
    "asia-east2",
    "asia-northeast1",
    "asia-northeast2",
    "asia-northeast3",
    "asia-south1",
    "asia-south2",
    "asia-southeast1",
    "asia-southeast2",
    "australia-southeast1",
    "australia-southeast2",
    "europe-central2",
    "europe-north1",
    "europe-southwest1",
    "europe-west1",
    "europe-west10",
    "europe-west12",
    "europe-west2",
    "europe-west3",
    "europe-west4",
    "europe-west6",
    "europe-west8",
    "europe-west9",
    "me-central1",
    "me-central2",
    "me-west1",
    "northamerica-northeast1",
    "northamerica-northeast2",
    "northamerica-south1",
    "southamerica-east1",
    "southamerica-west1",
    "us-central1",
    "us-central2",
    "us-east1",
    "us-east4",
    "us-east5",
    "us-east7",
    "us-south1",
    "us-west1",
    "us-west2",
    "us-west3",
    "us-west4",
    "us-west8"
  ];
  protected completedConfiguration = false;
  protected deploy: string = '';
  protected undeploy: string = '';
  protected templateList = [
    TEMPLATE_NAMES.get('SINGLE_PLAYBOOK'),
    TEMPLATE_NAMES.get('MULTIPLE_PLAYBOOK'),
    TEMPLATE_NAMES.get('AGENT_BUILDER_SEARCH'),
    TEMPLATE_NAMES.get('AGENT_BUILDER_DOCUMENT_SEARCH'),
  ];
  selectedTemplate : string | null = null;
  private readonly activatedRoute = inject(ActivatedRoute);

  constructor(
    private readonly router: Router,
    private fb: FormBuilder,
    private http: HttpClient,
  ) { }

  ngOnInit() {
    this.projectForm = this.fb.group({
      [this.projectFormKeys.PROJECT_ID]: new FormControl('', [Validators.required]),
      [this.projectFormKeys.CHATBOT_TEMPLATE]: new FormControl('', [Validators.required]),
      [this.projectFormKeys.REGION]: new FormControl('', [Validators.required]),
      [this.projectFormKeys.FIREBASE_PROJECT_ID]: new FormControl(''),
      [this.projectFormKeys.FIREBASE_API_KEY]: new FormControl(''),
      [this.projectFormKeys.FIREBASE_AUTH_DOMAIN]: new FormControl(''),
      [this.projectFormKeys.CHATBOT_NAME]: new FormControl('')
    });
    this.activatedRoute.paramMap.subscribe({
      next: (params)=>{
        if(this.templateList.map(x=>x.name)?.includes(params.get('templateId'))){
          this.projectForm.get(this.projectFormKeys.CHATBOT_TEMPLATE)?.setValue(params.get('templateId'));
        }
      }
    });

  }

  routeToHome() {
    this.router.navigate(['/']);
  }

  onSubmit() {
    this.http.get('deploy.py', { responseType: 'text' })
      .subscribe(pythonScript => {
        // Process the Python script and replace placeholders
        if(this.addFirebaseConfig) {
          const formData = {
            project_id: this.projectForm.value.project_id,
            region: this.projectForm.value.region,
            chatbot_name: this.projectForm.value.chatbot_name,
            chatbot_template: this.projectForm.value.chatbot_template,
            required_login: "True",
            firebase_project_id: this.projectForm.value.firebase_project_id,
            api_key: this.projectForm.value.api_key,
            auth_domain: this.projectForm.value.auth_domain,
          };
          this.deploy = this.replacePlaceholders(pythonScript, formData);
        } else {
          const formData = {
            project_id: this.projectForm.value.project_id,
            region: this.projectForm.value.region,
            chatbot_name: this.projectForm.value.chatbot_name,
            chatbot_template: this.projectForm.value.chatbot_template,
            required_login: "False",
          };
          this.deploy = this.replacePlaceholders(pythonScript, formData);
        }
      });
    
    this.http.get('undeploy.py', { responseType: 'text' })
      .subscribe(pythonScript => {
        console.log(pythonScript);
        // Process the Python script and replace placeholders
        const formData = {
          project_id: this.projectForm.value.project_id,
          region: this.projectForm.value.region,
          chatbot_name: this.projectForm.value.chatbot_name,
        };
        this.undeploy = this.replacePlaceholders(pythonScript, formData);
      });
  }

  replacePlaceholders(script: string, data: any): string {
    // Simple string replacement (adjust as needed)
    for (const key in data) {
      script = script.replace(`{{${key}}}`, data[key]);
    }
    return script;
  }

  downloadFile() {
    const fileName= this.projectForm.value.chatbot_name?.replaceAll(" ", "_");
    let blob = new Blob([this.deploy], { type: 'text/plain;charset=utf-8' });
    FileSaver.saveAs(blob, `${fileName}_setup.py`);
    blob = new Blob([this.undeploy], { type: 'text/plain;charset=utf-8' });
    FileSaver.saveAs(blob, `${fileName}_decomission.py`);
  }

  openFirebaseTutorial() {
    window.open("https://screencast.googleplex.com/cast/NTc5NDE2MDU3MjM2Njg0OHw0M2RiYjUzZi1iZg");
  }

  openFirebaseConfiguration() {
    window.open("https://screenshot.googleplex.com/6pGLF5GJtWgHcGJ.png")
  }

  openGCPIdTutorial() {
    window.open("https://screenshot.googleplex.com/C4E35pxgGaDi6Uw.png")
  }

  sendEmailToTeam() {
    const body = `Hi team!
    
I'm interested in setting up a quick bot application in my GCP project

Regards,`;

    var mailUrl = `${BASE_URL}su=${EMAIL_SUBJET}&to=${encodeURIComponent("quick-bot-team@google.com")}&body=${encodeURIComponent(body)}`;
    window.open(mailUrl)
  }

  checkChangesAndRefetchScript(){
    if(this.projectForm.valid && this.stepper?.selectedIndex === 2){
      this.onSubmit();
    }
  }

  updateForm(){
    this.addFirebaseConfig = !this.addFirebaseConfig;
    if(this.addFirebaseConfig){
      this.projectForm.controls[ProjectFormKeys.FIREBASE_API_KEY].setValidators([Validators.required]);
      this.projectForm.controls[ProjectFormKeys.FIREBASE_AUTH_DOMAIN].setValidators([Validators.required]);
      this.projectForm.controls[ProjectFormKeys.FIREBASE_PROJECT_ID].setValidators([Validators.required]);
    }else{
      this.projectForm.controls[ProjectFormKeys.FIREBASE_API_KEY].setValidators(null);
      this.projectForm.controls[ProjectFormKeys.FIREBASE_AUTH_DOMAIN].setValidators(null);
      this.projectForm.controls[ProjectFormKeys.FIREBASE_PROJECT_ID].setValidators(null);
    }
    this.projectForm.controls[ProjectFormKeys.FIREBASE_API_KEY].updateValueAndValidity();
    this.projectForm.controls[ProjectFormKeys.FIREBASE_AUTH_DOMAIN].updateValueAndValidity();
    this.projectForm.controls[ProjectFormKeys.FIREBASE_PROJECT_ID].updateValueAndValidity();  }
}
