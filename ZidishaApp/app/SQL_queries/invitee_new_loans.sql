SELECT  first_loan_date,
        l2.usd_amount AS usd_requested,
        l2.raised_percentage/100.0 AS raised_fraction,
        l2.usd_amount * l2.raised_percentage/100.0 AS usd_inflow,
        CASE    WHEN l2.raised_percentage = 100 THEN l2.usd_amount
                ELSE 0
                END AS usd_secured,
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
        JOIN borrower_invites AS bi
        ON l1.borrower_id = bi.invitee_id
        JOIN borrowers AS b
        ON b.id = l1.borrower_id
        JOIN countries AS c
        ON c.id = b.country_id