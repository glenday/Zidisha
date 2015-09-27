/*
Raised amounts and interest rates for all loans.

First column must be the time stamp relevant for subsequent columns.
Last column must be the country name with the title set to country_name.
*/
SELECT  l.created_at,
        l.usd_amount AS usd_requested,
        l.raised_percentage/100.0 AS raised_fraction,
        l.raised_usd_amount AS usd_inflow,
        CASE    WHEN l.raised_percentage = 100 THEN l.usd_amount
                ELSE 0
                END AS usd_secured,
        l.lender_interest_rate,
        c.name AS country_name
        FROM loans AS l
        JOIN borrowers AS b
        ON b.id = l.borrower_id
        JOIN countries AS c
        ON b.country_id = c.id
        ORDER BY l.created_at
