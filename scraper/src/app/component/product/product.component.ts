import { Component, OnInit } from '@angular/core';
import { ScraperService } from 'src/app/service/scraper.service';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.css']
})
export class ProductComponent implements OnInit {

  productName:string = '';
  flipkartProduct:any = null;
  amazonProduct:any = null;

  productSearched:boolean = false;

  constructor(private productService:ScraperService) { }

  ngOnInit(): void {
  }

  fetchProduct():void {
    if(!this.productName.trim()){
      return;
    }
    this.productService.getProduct(this.productName).subscribe(data=>{
      this.flipkartProduct = data.flipkart;
      this.amazonProduct = data.amazon;
      this.productSearched = true;
      console.log(data);
    },error=>{
      this.productSearched=true;
      console.error(error);
    })
  }
}
