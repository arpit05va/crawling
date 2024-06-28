import { Injectable } from '@angular/core';
import { HttpClient,HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

interface Product{
  name: string;
  dis_price: string;
  actual_price: string;
  discount: string;
}

interface ScrapeResponse {
  flipkart: Product | null;
  amazon: Product | null;
}

@Injectable({
  providedIn: 'root'
})
export class ScraperService {
  private baseUrl:string ='http://127.0.0.1:5000/search';
  constructor(private http:HttpClient) { }

  getProduct(productName:string):Observable<ScrapeResponse>{
    const params = new HttpParams().set('name',productName);
    return this.http.get<ScrapeResponse>(this.baseUrl, { params });
  }
}
