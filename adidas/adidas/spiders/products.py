import json
import scrapy

from ..items import AdidasProductItems


class AdidasProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["www.adidas.com"]

    def __init__(self, *args, **kwargs):
        super(AdidasProductsSpider, self).__init__(*args, **kwargs)
        self.base_url = "https://www.adidas.com/us/men-tops"
        self.items_per_page = 48
        self.max_pages = 2  # Adjust this value to scrape more or fewer pages

    def start_requests(self):
        for page in range(self.max_pages):
            if page == 0:
                url = self.base_url
            else:
                start = page * self.items_per_page
                url = f"{self.base_url}?start={start}"

            yield scrapy.Request(url=url, callback=self.parse_search_page)

    def parse_search_page(self, response):
        product_links = response.css(
            "a.glass-product-card__assets-link::attr(href)"
        ).getall()

        for link in product_links:
            full_url = response.urljoin(link)
            yield scrapy.Request(url=full_url, callback=self.parse_item)

    def parse_item(self, response):
        item = AdidasProductItems()

        products_data = json.loads(
            response.css("script[type='application/ld+json']::text").get()
        )

        # Extract required fields from the JSON data
        item["name"] = products_data.get("name", "")
        item["colour"] = products_data.get("color", "")
        item["images"] = json.dumps(
            products_data.get("image", [])
        )  # Convert image list to JSON string
        item["manufacturer"] = products_data.get("brand", {}).get("name", "")
        item["sku"] = products_data.get("sku", "")
        item["url"] = response.url  # Assuming the URL is the page URL being scraped
        item["category"] = products_data.get("category", "")
        item["brandName"] = products_data.get("brand", {}).get("name", "")
        item["ratingValue"] = products_data.get("aggregateRating", {}).get(
            "ratingValue", None
        )
        item["reviewCount"] = products_data.get("aggregateRating", {}).get(
            "reviewCount", None
        )
        item["bestRating"] = products_data.get("aggregateRating", {}).get(
            "bestRating", None
        )
        item["worstRating"] = products_data.get("aggregateRating", {}).get(
            "worstRating", None
        )

        # 'offers' should be a dictionary, extracting directly
        offers = products_data.get("offers", {})

        if offers:
            item["availability"] = offers.get("availability", "")
            item["priceUSD"] = offers.get("price", None)
            item["shippingRateValue"] = (
                offers.get("shippingDetails", {})
                .get("shippingRate", {})
                .get("value", None)
            )

            # Seller Information
            item["sellerName"] = offers.get("seller", {}).get("name", "")
            item["sellerURL"] = offers.get("seller", {}).get("url", "")

            # Return Policy Information
            return_policy = offers.get("hasMerchantReturnPolicy", {})
            item["applicableReturnCountry"] = return_policy.get("applicableCountry", "")
            item["returnPolicyCategory"] = return_policy.get("returnPolicyCategory", "")
            item["merchantReturnDays"] = return_policy.get("merchantReturnDays", None)
            item["returnMethod"] = return_policy.get("returnMethod", "")
            item["returnFees"] = return_policy.get("returnFees", "")

        yield item
