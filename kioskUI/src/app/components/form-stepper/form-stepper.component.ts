import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-form-stepper',
  templateUrl: './form-stepper.component.html',
  styleUrl: './form-stepper.component.scss'
})
export class FormStepperComponent {
  @Input() formGroup!: FormGroup;
  @Input() stepperConfig!: any;

  constructor(private router: Router){
  }

  onRadioChange(section: any, selectedOption: any) {
    section.options.forEach((option: { isSelected: boolean; }) => {
      option.isSelected = option === selectedOption; 
    });
    section.selectedOptionResponse = {
      subtitle : selectedOption.subtitle,
      caption: selectedOption.caption
    }
    selectedOption.onClick(); 
  }

  goToSpinnerComponent() {
    this.router.navigate(['/spinner']);
  }
}
