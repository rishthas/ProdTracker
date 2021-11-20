SELECT "product_product"."id",
    "product_product"."serial_num",
    "product_product"."model_id",
    "product_product"."pur_invoce_no",
    "product_product"."purchase_date",
    "product_product"."branch_id",
    "product_product"."invoice_date",
    "product_product"."invoce_no",
    "product_product"."customer_code",
    "product_product"."status"
FROM "product_product"
WHERE (
        "product_product"."purchase_date" < 2021 -11 -01
        AND (
            "product_product"."invoce_no" IS NULL
            OR "product_product"."invoice_date" >= 2021 -11 -01
        )
        AND "product_product"."id" IN (
            SELECT U0."product_id"
            FROM "product_stockcheck" U0
            WHERE (
                    U0."month" = 10
                    AND U0."year" = 2021
                )
        )
    )