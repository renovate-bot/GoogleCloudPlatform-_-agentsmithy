import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ChatComponent } from './components/main/chat/chat.component';
import { MainComponent } from './components/main/main.component';
import { ManageIntentComponent } from './components/manage-intent/manage-intent.component';

const routes: Routes = [
  {path: '', component: MainComponent},
  {path: 'chat', component: ChatComponent},
  {path: 'intent-management', component: ManageIntentComponent}
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
