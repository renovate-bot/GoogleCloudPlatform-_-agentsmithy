import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { CreateBotComponent } from './create-bot/create-bot.component';


const routes: Routes = [  
  {path: '', component: HomeComponent},
  {path:'create-bot/:templateId', component: CreateBotComponent},
  {path:'create-bot', component: CreateBotComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
