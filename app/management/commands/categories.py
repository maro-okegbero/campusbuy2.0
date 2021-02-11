from app.models import Category

obj = dict(
    model=Category,
    data=[

        dict(
            name="Mobile and Tablets",
            code="mobile_and_tablets",
            description="The nicest phones and tablets"),

        dict(
            name="Health & Beauty",
            code="health_&_beauty",
            description="cosmetic products to keep you fresh",
        ),
        dict(
            name="Computing",
            code="computing",
            description="Laptops, desktops and computing accessories"
        ),
        dict(
            name="Electronics",
            code="electronics",
            description="Fans, HotPlates and other appliances"
        ),
        dict(
            name="Men's Clothing and Accessories",
            code="men_clothing_&_accessories",
            description="Shirts,Jeans,Sneakers,Ties e.t.c"
        ),
        dict(
            name="Women's Clothing and Accessories",
            code="women_clothing_&_accessories",
            description="Gowns, Tops, Heels, Lingerie e.t.c"
        ),
        dict(
            name="Educational Materials",
            code="educational_materials",
            description="TD Boards, T-Squares, Textbooks e.t.c"
        )
    ]
)
