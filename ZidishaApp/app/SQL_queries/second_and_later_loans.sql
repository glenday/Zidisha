/*
Raised amounts and interest rates for second or later loans.

First column must be the time stamp relevant for subsequent columns.
Last column must be the country name with the title set to country_name.
*/
SELECT  l2.created_at AS loan_date,
        b.created_at,
        l2.usd_amount AS usd_requested,
        l2.raised_percentage/100.0 AS raised_fraction,
        l2.raised_usd_amount AS usd_inflow,
        CASE    WHEN l2.raised_percentage = 100 THEN l2.usd_amount
                ELSE 0
                END AS usd_secured,
        l2.lender_interest_rate,
        l2.status,
        CASE    WHEN l2.status = 3 THEN TIMESTAMPDIFF(SECOND, l2.disbursed_at, l2.repaid_at)/86400.0

                ELSE NULL
                END AS time_to_repay,
        (l2.paid_amount + l2.loan_loss_reserve_fee + l2.registration_fee) / l2.amount - 1.0 AS fees_fraction,
        l2.loan_loss_reserve_fee,
        l2.registration_fee,
        c.name AS country_name
        FROM ( -- loans created after the first successful loan
            SELECT  l3.id,
                    l3.borrower_id
                    FROM loans AS l3
                    JOIN ( -- first successful loans
                        SELECT  borrower_id,
                                MIN(created_at) AS first_loan_date
                                FROM loans
                                WHERE raised_percentage = 100  AND status = 3
                                GROUP BY borrower_id
                    ) AS l1
                    ON l1.borrower_id = l3.borrower_id AND l3.created_at > l1.first_loan_date
        ) AS l4
        JOIN loans AS l2
        ON l4.id = l2.id
        JOIN borrowers AS b
        ON b.id = l4.borrower_id
        JOIN countries AS c
        ON c.id = b.country_id
        ORDER BY l2.created_at