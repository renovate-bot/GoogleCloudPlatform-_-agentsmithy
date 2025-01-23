import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-custom-stepper',
  templateUrl: './custom-stepper.component.html',
  styleUrls: ['./custom-stepper.component.scss'],
})
export class CustomStepperComponent {
  steps: any[] = [];
  currentStep = 0;

  constructor(private fb: FormBuilder) {
    this.steps = [
      {
        heading: 'Personal Information',
        formGroup: this.fb.group({
          firstName: ['', Validators.required],
          lastName: ['', Validators.required],
        }),
        fields: [
          { label: 'First Name', name: 'firstName' },
          { label: 'Last Name', name: 'lastName' },
        ],
      },
      {
        heading: 'Contact Details',
        formGroup: this.fb.group({
          email: ['', [Validators.required, Validators.email]],
          phone: ['', Validators.required],
        }),
        fields: [
          { label: 'Email', name: 'email' },
          { label: 'Phone Number', name: 'phone' },
        ],
      },
      {
        heading: 'Address',
        formGroup: this.fb.group({
          addressLine1: ['', Validators.required],
          addressLine2: [''],
        }),
        fields: [
          { label: 'Address Line 1', name: 'addressLine1' },
          { label: 'Address Line 2', name: 'addressLine2' },
        ],
      },
      {
        heading: 'Summary',
        formGroup: this.fb.group({
          summary: ['', Validators.required],
        }),
        fields: [{ label: 'Summary', name: 'summary' }],
      },
      {
        heading: 'Confirmation',
        formGroup: this.fb.group({}),
        fields: [],
      },
    ];
  }

  goNext() {
    if (this.currentStep < this.steps.length - 1) {
      this.currentStep++;
    }
  }

  goBack() {
    if (this.currentStep > 0) {
      this.currentStep--;
    }
  }
}
