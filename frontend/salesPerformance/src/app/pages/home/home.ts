import { Component } from '@angular/core';
import { MaterialModule } from '../../shared/material-module/material-module';
import { Sidenav } from '../../shared/sidenav/sidenav';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-home',
  imports: [MaterialModule,Sidenav,RouterOutlet],
  templateUrl: './home.html',
  styleUrl: './home.scss'
})
export class Home {

}
