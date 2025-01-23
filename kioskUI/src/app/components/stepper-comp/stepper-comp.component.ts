import { Component } from '@angular/core';
import { Validators, FormBuilder, FormArray, FormGroup, AbstractControl } from '@angular/forms';

@Component({
  selector: 'app-stepper-comp',
  templateUrl: './stepper-comp.component.html',
  styleUrls: ['./stepper-comp.component.scss']
})
export class StepperCompComponent {
  formGroup: FormGroup;
  selectedRunTime: string = 'resoningEngine';


  constructor(private _formBuilder: FormBuilder) { }

  get formArray(): AbstractControl | null { return this.formGroup.get('formArray'); }


  ngOnInit() {
    this.formGroup = this._formBuilder.group({
      formArray: this._formBuilder.array([
        this._formBuilder.group({
          agentName: ['', Validators.required],
          agentType: ['', Validators.required],
          industry: ['', Validators.required],
        }),
        this._formBuilder.group({
          runTime: ['', Validators.required]
        }),
      ])
    });
  }

  // formArray1(): FormArray {
  //   return this.formGroup.get('formArray') as FormArray;
  // }

  selectRunTime(value: string) {
    console.log(value);
    // this.formArray1().at(1).patchValue({runtime: value});
    // console.log(this.formArray1());

    this.selectedRunTime = value;
  }


}
