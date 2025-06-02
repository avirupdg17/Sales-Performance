import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from '../../shared/material-module/material-module';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule,FormsModule,MaterialModule],
  templateUrl: './login.html',
  styleUrl: './login.scss'
})
export class Login {
  username: string = '';
  password: string = '';
  selectedRole: string = '';
  constructor(private http: HttpClient) {}
  onSubmit() {
    console.log('Username:', this.username);
    console.log('Password:', this.password);
    console.log('Selected Role:', this.selectedRole);
    const payload = {
      username: this.username,
      password: this.password,
      role: this.selectedRole
    };
    this.http.post('http://localhost:8000/login', payload).subscribe({
      next: (response) => {
        console.log('Login successful:', response);
      },
      error: (error) => {
        console.error('Login failed:', error);
      }
    });
  }
}