import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule, routingComponents } from './app-routing.module';
import { AppComponent } from './app.component';
import { CategoriaComponent } from './categoria/categoria.component';
import { HistorialComponent } from './historial/historial.component';
import { DisponibilidadComponent } from './disponibilidad/disponibilidad.component';
import { ChatComponent } from './chat/chat.component';
import { IndexComponent } from './index/index.component';

@NgModule({
  declarations: [
    AppComponent,
    routingComponents,
    CategoriaComponent,
    HistorialComponent,
    DisponibilidadComponent,
    ChatComponent,
    IndexComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
