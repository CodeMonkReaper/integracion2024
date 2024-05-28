import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import { CatalogoComponent } from './comprador/catalogo/catalogo.component';
import { GestionProductoComponent } from './admin/gestion-producto/gestion-producto.component';
import { CategoriaComponent } from './categoria/categoria.component';
import { ChatComponent } from './chat/chat.component';
import { DisponibilidadComponent } from './disponibilidad/disponibilidad.component';
import { HistorialComponent } from './historial/historial.component';



const routes: Routes = [
  { path: 'login', component: LoginComponent},
  { path: 'register', component: RegisterComponent},
  { path: 'catalogo', component: CatalogoComponent},
  { path: 'gestionprod', component: GestionProductoComponent},
  { path: 'categoria', component: CategoriaComponent},
  { path: 'chat', component: ChatComponent},
  { path: 'stock', component: DisponibilidadComponent},
  { path: 'historialprecios', component: HistorialComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const  routingComponents = [LoginComponent, RegisterComponent, CatalogoComponent, GestionProductoComponent, CategoriaComponent,
  ChatComponent, DisponibilidadComponent, HistorialComponent]