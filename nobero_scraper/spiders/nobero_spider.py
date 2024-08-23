import scrapy
import re

class NoberoSpider(scrapy.Spider):
    name = "nobero_spider"
    allowed_domains = ["nobero.com"]
    start_urls = ['https://nobero.com/pages/men']

    def parse(self, response):
        # Extract subcategories with images
        subcategories = response.css('a[id="image-container"]')
        
        for subcategory in subcategories:
            subcategory_url = subcategory.css('::attr(href)').get(default='').strip()
            subcategory_img_url = subcategory.css('img::attr(src)').get(default='').strip()

            # Full URL for image and subcategory
            full_img_url = response.urljoin(subcategory_img_url)
            full_subcategory_url = response.urljoin(subcategory_url)

            # Request to follow the subcategory URL and pass the image URL in the meta
            yield scrapy.Request(
                full_subcategory_url, 
                callback=self.parse_subcategory, 
                meta={
                    'subcategory_image_url': full_img_url,  # Pass full image URL in meta
                    'subcategory_url': full_subcategory_url,
                    'subcategory_name': subcategory.css('::text').get(default='').strip()  # Extract subcategory name if available
                }
            )

    def parse_subcategory(self, response):
        # Get the subcategory information from the meta
        subcategory_img_url = response.meta['subcategory_image_url']
        subcategory_url = response.meta['subcategory_url']
        subcategory_name = response.meta.get('subcategory_name', 'Unknown')  # Default to 'Unknown' if not available

        # Select all product links within the subcategory
        products = response.css('a.product_link')
        
        for product in products:
            product_url = product.css('::attr(href)').get(default='').strip()
            discount = product.css('span.discount-per::text').get(default='').strip()
            img_url = product.css('img::attr(src)').get(default='').strip()

            # Request to follow the product URL and pass the subcategory info in the meta
            yield scrapy.Request(
                response.urljoin(product_url), 
                callback=self.parse_product, 
                meta={
                    'subcategory_name': subcategory_name,  # Pass subcategory name to the product parsing
                    'subcategory_image_url': subcategory_img_url,  # Pass subcategory image URL to the product parsing
                    'subcategory_url': subcategory_url,
                    'discount': discount,
                    'product_image_url': response.urljoin(img_url)
                }
            )

    def parse_product(self, response):
        # Extracting the title
        title = response.css('h1.capitalize::text').get(default='').strip()

        # Extracting the price
        price_text = response.css('h2#variant-price spanclass::text').get(default='').strip()
        mrp = response.css('span.line-through spanclass::text').get(default='').strip()
        pricecleaned = re.sub(r'[^\d.,]', '', price_text)
        mrpcleaned = re.sub(r'[^\d.,]', '', mrp)

        # Extracting other details
        description_div = response.css('div#description_content')

        material = description_div.css('strong:contains("Material:") + span::text').get(default='').strip()
        neck = description_div.css('strong:contains("Neck:") + span::text').get(default='').strip()
        sleeves = description_div.css('strong:contains("Sleeves:") + span::text').get(default='').strip()
        features = description_div.css('strong:contains("Features:") + span ~ span::text').getall()
        origin = description_div.css('strong:contains("Origin:") + span::text').get(default='').strip()
        wash_care = description_div.css('strong:contains("Wash Care:") + span::text').get(default='').strip()
        note = description_div.css('strong:contains("Please Note:") + span::text').get(default='').strip()

        features = [feature.strip() for feature in features if feature.strip()]
        features_text = '\n'.join(features)

        description = (
            f"Material: {material}\n"
            f"Neck: {neck}\n"
            f"Sleeves: {sleeves}\n"
            f"Features:\n{features_text}\n"
            f"Origin: {origin}\n"
            f"Wash Care: {wash_care}\n"
            f"Please Note: {note}"
        )

        categories_keywords = {
            "Oversized": ["Oversized"],
            "T-Shirts": ["T-Shirt","T-Shirts"],
            "Joggers": ["Joggers"],
            "Shorts": ["Shorts"],
            "Plus Size T-Shirts": ["Plus Size T-Shirts"],
            "Co-ord Sets": ["Co-ord"]
        }

        categories = [
            cat for cat, keywords in categories_keywords.items()
            if any(keyword in title for keyword in keywords)
        ]
       
        categories = categories if categories else ["Unknown"]
        
        image_url = response.css('figure#image-container img::attr(src)').get(default='').lstrip('//')
        image_url = 'https://' + image_url if image_url else ''
        
        color_text = response.css('span#selected-color-title::text').get(default='').strip()
        
        # Remove leading '-' if it exists
        if color_text.startswith('-'):
            color_text = color_text[1:].strip()
        
        sizes = response.css('input.size-select-input::attr(value)').getall()
        
        # Define the desired order
        size_order = ["S", "M", "L", "XL", "XXL", "XXXL"]
        
        # Create a dictionary for quick lookup
        size_dict = {size: i for i, size in enumerate(size_order)}
        
        # Sort sizes based on predefined order
        sorted_sizes = sorted(set(sizes), key=lambda x: size_dict.get(x, float('inf')))
        
        # Creating the JSON object
        product = {
            "category": categories,
            "url": response.url,
            "image_url": image_url,
            "title": title,
            "price": pricecleaned,
            "mrp": mrpcleaned,
            "last_7_day_sale": response.meta.get('discount', price_text),
            "category_image_url": response.meta.get('subcategory_image_url', ''),  # Include subcategory image URL
            "available_skus": [
                {
                    "color": color_text,
                    "size": sorted_sizes
                }
            ],
            "fit": response.css('div.product-metafields-values p::text').get(default='').strip(),
            "fabric": response.css('div.product-metafields-values:contains("Fabric") p::text').get(default='').strip(),
            "neck": response.css('div.product-metafields-values:contains("Neck") p::text').get(default='').strip(),
            "sleeve": response.css('div.product-metafields-values:contains("Sleeve") p::text').get(default='').strip(),
            "pattern": response.css('div.product-metafields-values:contains("Pattern") p::text').get(default='').strip(),
            "length": response.css('div.product-metafields-values:contains("Length") p::text').get(default='').strip(),
            "description": description,
        }

        # Outputting the product JSON
        yield product
