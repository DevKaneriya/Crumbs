// Category Interface
export interface Category {
  id: number;
  route: string;
  name: string;
  text: string;
  icon: string;
  image: string;
  content: string;
  display_order?: number;
}

// Category with Products Interface
export interface CategoryWithProducts extends Category {
  products: ProductList[];
}

// Product Image Interface
export interface ProductImage {
  id: number;
  image_path: string;
  display_order: number;
}

// Product Variant (Price) Interface
export interface ProductVariant {
  id: number;
  weight: string;
  original_price: string;
  discounted_price: string;
  in_stock: boolean;
}

// Product List Interface (lightweight for listings)
export interface ProductList {
  id: number;
  name: string;
  short: string;
  categories: string[];
  images: (ProductImage | undefined)[];
  variants: ProductVariant[];
}

// Product Detail Interface (full product information)
export interface Product {
  id: number;
  name: string;
  short: string;
  categories: Category[];
  about?: string;
  footer?: string;
  benefits?: string[];
  ingredients?: string[];
  nutritional_value?: { [key: string]: string };
  images: (ProductImage | undefined)[];
  variants: ProductVariant[];
}
