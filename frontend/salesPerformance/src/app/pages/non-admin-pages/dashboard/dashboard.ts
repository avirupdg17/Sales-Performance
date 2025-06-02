import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MaterialModule } from '../../../shared/material-module/material-module';
import { CommonModule } from '@angular/common';

interface PerformanceData {
  month: string;
  fwa: number;
  mnp: number;
  jioMnp: number;
  mdsso: number;
  simBilling: number;
}

interface RankingData {
  month: string;
  rank: number | null;
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.scss'],
  imports:[MaterialModule,CommonModule],
})
export class Dashboard implements OnInit {
  isDataLoaded: boolean = false; // Track loading state
  displayedColumns: string[] = ['month', 'fwa', 'mnp', 'jmnp', 'mdsso', 'simBillings'];
  dataSource: PerformanceData[] = [];

  rankingDisplayedColumns: string[] = [];
  rankingRow: {[month: string]: number | string} = {};  // store ranks in a single row

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.isDataLoaded = false; // Initialize loading state
    this.http.get<any>('http://localhost:8000/dashboard').subscribe((response:any) => {
      this.dataSource = response.performance.map((entry: any) => ({
        month: entry.month,
        fwa: entry.metrics.fwa,
        mnp: entry.metrics.mnp,
        jioMnp: entry.metrics.jio_mnp,
        mdsso: entry.metrics.mdsso,
        simBilling: entry.metrics.sim_billing,
      }));

      this.rankingDisplayedColumns = response.ranking.map((entry: any) => entry.month);

      // Create a single row object with month: rank (or N/A if rank is null)
      response.ranking.forEach((entry: any) => {
        this.rankingRow[entry.month] = entry.rank !== null ? entry.rank : 'N/A';
      });
    });
    this.isDataLoaded = true;
  }

  viewIncentiveScheme(): void {
    // Add your logic here to view the incentive scheme
    alert("Incentive scheme feature coming soon!");
  }
}
