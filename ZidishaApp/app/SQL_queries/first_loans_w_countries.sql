/*
Raised amounts and interest rates for first time loans.

First column must be the time stamp relevant for subsequent columns.
Last column must be the country name with the title set to country_name.
*/
SELECT  l1.first_loan_date,
        b.created_at,
        l2.usd_amount AS usd_requested,
        l2.raised_percentage/100.0 AS raised_fraction,
        l2.raised_usd_amount AS usd_inflow,
        CASE    WHEN l2.raised_percentage = 100 THEN l2.usd_amount
                ELSE 0
                END AS usd_secured,
        l2.lender_interest_rate,
        l2.status,
        l2.disbursed_at,
        l2.repaid_at,
        c.name AS country_name
        FROM (
            SELECT  borrower_id,
                    MIN(created_at) AS first_loan_date
                    FROM loans
                    GROUP BY borrower_id
                    ORDER BY first_loan_date
        ) AS l1
        JOIN loans AS l2
        ON l1.borrower_id = l2.borrower_id AND l1.first_loan_date = l2.created_at
        JOIN borrowers AS b
        ON b.id = l1.borrower_id
        JOIN countries AS c
        ON c.id = b.country_id
        ORDER BY l1.first_loan_date