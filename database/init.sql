CREATE TABLE IF NOT EXISTS tracking (
    id SERIAL PRIMARY KEY,
    item_number VARCHAR(13) NOT NULL UNIQUE,
    status VARCHAR(50) NOT NULL,
    location VARCHAR(255),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_item_number ON tracking(item_number);

INSERT INTO tracking (item_number, status, location) VALUES
    ('EF582568151TH', 'Delivered', 'Bangkok, Thailand'),
    ('EA666458151TH', 'In Transit', 'Chiang Mai, Thailand'),
    ('RG453678925TH', 'Out for Delivery', 'Phuket, Thailand'),
    ('EF582621151TH', 'Processing', 'Nonthaburi, Thailand'),
    ('AB123456789TH', 'Shipped', 'Khon Kaen, Thailand');
