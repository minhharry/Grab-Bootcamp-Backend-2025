from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType, ArrayType, TimestampType

# {"name": "Phúc Rau Má - Lạc Long Quân", "restaurant_type": "CAFÉ/DESSERT -Chi nhánh", "avatar_url": "https://down-ws-vn.img.susercontent.com/vn-11134259-7r98o-lwaud2iv0us954@resize_ss640x400!@crop_w640_h400_cT", "price_range": "15.000 - 35.000", "opening_hours": "10:30 - 22:45", 
#  "address": "107H Lạc Long Quân, P. 3, Quận 11, TP. HCM", "longitude": 106.6419109, "latitude": 10.7603451, "avgRating": 9.6, "rating_count": 1, 
#  "source": "ShopeeFood", "reviews": [{"Title": "Phúc rau má", "Description": "Có rất nhìu món để cho khách hàng lựa chọn, sinh tố , rau má , nước ép, iceBlened, Yogurt đá xay, Trà trái cây .. Đãm bảo chất lượng trên từng ly nước cho quý khách với tiêu chí của quán là Ngon- bổ - rẻ- và chất lượng. Cám ơn quý khách đã ủng hộ quán ạ. 🥰🥰🥰", "AvgRating": 9.6, "Review_date": "24/10/2021", "Author": "Sophie Nguyễn"}], "images": [{"name": "Rau má kem Machiato (Mặn/ ngọt)", "current_price": "20.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Rau má sinh tố khoai môn đậu phộng", "current_price": "35.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Sinh tố sầu riêng", "current_price": "42.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Sinh tố khoai môn", "current_price": "30.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Sinh tố dâu kiwi", "current_price": "40.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Sinh tố dưa lưới dâu tây", "current_price": "38.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Sinh tố dâu tằm", "current_price": "30.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Soda blue chanh dây", "current_price": "30.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Soda dâu tằm", "current_price": "28.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Ép cóc", "current_price": "25.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Ép cam dâu tây", "current_price": "45.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Ép carrot cà chua dây tây", "current_price": "48.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Ép chanh dây dâu syrup", "current_price": "30.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Trà tắc xí muội", "current_price": "30.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Trà dâu xí muội", "current_price": "35.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Trà đào hoa nhài", "current_price": "35.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Trà bưởi hồng hoa nhài", "current_price": "40.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Yogurt táo ĐX", "current_price": "40.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Cookie Cafe Đá Xay", "current_price": "42.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Chanh dây đá xay", "current_price": "35.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "Sâm Dứa Sữa", "current_price": "25.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "BT Mỡ Hành Trứng Cút", "current_price": "29.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}, {"name": "BT Mỡ Hành Trứng Cút", "current_price": "29.000đ", "img_url": "https://mms.img.susercontent.com/vn-11134517-7r98o-lqn24i7chcfw9c@resize_ss120x120!@crop_w120_h120_cT"}], "restaurant_url": "https://shopeefood.vn/ho-chi-minh/phuc-rau-ma-lac-long-quan", "crawl_time": "2025-05-05 18:51:05", "crawl_id": "2025-05-05-001", "source_unique_id": 1079433}

shopeefood_raw_schema = StructType([
    StructField("name", StringType(), True),
    StructField("restaurant_type", StringType(), True),
    StructField("avatar_url", StringType(), True),
    StructField("price_range", StringType(), True),  # Chuỗi, sẽ parse thành JSON
    StructField("opening_hours", StringType(), True),
    StructField("address", StringType(), True),
    StructField("longitude", FloatType(), True),
    StructField("latitude", FloatType(), True),
    StructField("avgRating", StringType(), True),  # Chuỗi, sẽ cast sang float
    StructField("rating_count", StringType(), True),  # Chuỗi, sẽ cast sang int
    StructField("source", StringType(), True),
    StructField("reviews", ArrayType(
        StructType([
            StructField("Title", StringType(), True),
            StructField("Description", StringType(), True),
            StructField("AvgRating", StringType(), True),  # Chuỗi, sẽ cast sang float
            StructField("Review_date", StringType(), True),
            StructField("Author", StringType(), True)
        ])
    ), True),
    StructField("images", ArrayType(
        StructType([
            StructField("name", StringType(), True),
            StructField("current_price", StringType(), True),
            StructField("img_url", StringType(), True)
        ])
    ), True),
    StructField("restaurant_url", StringType(), True),
    StructField("crawl_time", StringType(), True),  # Chuỗi, sẽ cast sang timestamp
    StructField("crawl_id", StringType(), True),
    StructField("source_unique_id", IntegerType(), True),  # Chuỗi, sẽ cast sang int
])