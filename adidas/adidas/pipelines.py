# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class AdidasPipeline:
    def process_item(self, item, spider):
        return item


class DataStandardizationPipeline:
    def process_item(self, item, spider):
        adaptor = ItemAdapter(item)

        # Standardize return policy category
        if (
            adaptor.get("returnPolicyCategory")
            == "https://schema.org/MerchantReturnFiniteReturnWindow"
        ):
            adaptor["returnPolicyCategory"] = "MerchantReturnFiniteReturnWindow"

        # Standardize merchant return days
        merchant_return_days = adaptor.get("merchantReturnDays")
        if merchant_return_days is not None:
            adaptor["merchantReturnDays"] = int(merchant_return_days)

        # Standardize return method
        if adaptor.get("returnMethod") == "https://schema.org/ReturnByMail":
            adaptor["returnMethod"] = "ReturnByMail"

        # Standardize return fees
        if adaptor.get("returnFees") == "https://schema.org/FreeReturn":
            adaptor["returnFees"] = "FreeReturn"

        return item


class SQLitePipeline:
    def __init__(self) -> None:
        # Connect to the SQLite database or create it if it doesn't exist
        self.conn = sqlite3.connect("products.db")
        self.cur = self.conn.cursor()

        # Create the 'products' table with all the fields you want to store
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                name,
                colour,
                images,
                manufacturer,
                sku,
                url,
                category,
                availability,
                priceUSD,
                brandName,
                shippingRateValue,
                sellerName,
                sellerURL,
                applicableReturnCountry,
                returnPolicyCategory,
                merchantReturnDays,
                returnMethod,
                returnFees,
                ratingValue,
                reviewCount,
                bestRating,
                worstRating
            )
            """
        )

    def process_item(self, item, spider):
        # Check if the item is already in the database
        self.cur.execute("""SELECT * FROM products WHERE sku = ?""", (item["sku"],))

        result = self.cur.fetchone()

        if result:
            spider.logger.warn(f"Item already in DB, {item['sku']}")
        else:
            # Insert the new item into the database
            self.cur.execute(
                """
                INSERT INTO products(
                    name, 
                    colour, 
                    images, 
                    manufacturer, 
                    sku, 
                    url, 
                    category, 
                    availability, 
                    priceUSD, 
                    brandName, 
                    shippingRateValue, 
                    sellerName, 
                    sellerURL, 
                    applicableReturnCountry, 
                    returnPolicyCategory, 
                    merchantReturnDays, 
                    returnMethod, 
                    returnFees, 
                    ratingValue, 
                    reviewCount, 
                    bestRating, 
                    worstRating
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item["name"],
                    item["colour"],
                    item["images"],
                    item["manufacturer"],
                    item["sku"],
                    item["url"],
                    item["category"],
                    item["availability"],
                    item["priceUSD"],
                    item["brandName"],
                    item["shippingRateValue"],
                    item["sellerName"],
                    item["sellerURL"],
                    item["applicableReturnCountry"],
                    item["returnPolicyCategory"],
                    item["merchantReturnDays"],
                    item["returnMethod"],
                    item["returnFees"],
                    item["ratingValue"],
                    item["reviewCount"],
                    item["bestRating"],
                    item["worstRating"],
                ),
            )
            self.conn.commit()

        return item

    def close_spider(self, spider):
        # Close the database connection when the spider is closed
        self.conn.close()
