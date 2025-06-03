import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MaterialModule } from '../../../shared/material-module/material-module';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-leaderboard',
  templateUrl: './leader-board.html',
  styleUrls: ['./leader-board.scss'],
  standalone: true,
  imports: [MaterialModule, CommonModule],
})
export class Leaderboard implements OnInit {
  role: string = '';
  leaderboards: any = {};
  selectedMonth: string = '';
  availableMonths: string[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.http.get<any>('http://localhost:8000/leaderboard').subscribe({
      next: (res: any) => {
        this.role = res.role;
        this.leaderboards = res.leaderboards;
        this.availableMonths = Object.keys(this.leaderboards).sort().reverse();
        this.selectedMonth = this.availableMonths[0];
      },
      error: (err: any) => {
        console.error('Failed to load leaderboard:', err);
      }
    });
  }

  selectMonth(month: string): void {
    this.selectedMonth = month;
  }

  getMonthLabel(monthKey: string): string {
    const [year, month] = monthKey.split('-');
    const date = new Date(+year, +month - 1);
    return date.toLocaleString('default', { month: 'long', year: 'numeric' });
  }

  // ✅ Template-safe helper to prevent type errors
  castKeyToString(key: unknown): string {
    return String(key);
  }
}
