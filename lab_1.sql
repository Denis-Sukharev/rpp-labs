create table region
(
	id integer PRIMARY KEY,
	name varchar(255) not null
);

create table tax_param
(
	id serial PRIMARY KEY,
	city_id integer REFERENCES region(id) not null,
	from_hp_car integer not null,
	to_hp_car integer not null,
	from_production_year_car integer not null,
	to_production_year_car integer not null,
	rate numeric not null
);

create table auto
(
	id serial primary key,
	city_id integer REFERENCES region(id) not null,
	tax_id integer REFERENCES tax_param(id) not null,
	name varchar(255) not null,
	horse_power integer not null,
	production_year integer not null,
	tax numeric not null
);

INSERT INTO region (id, name) VALUES
    (1, 'Москва'),
    (2, 'Санкт-Петербург'),
    (3, 'Новосибирск'),
    (4, 'Екатеринбург'),
    (5, 'Казань'),
    (6, 'Челябинск'),
    (7, 'Омск'),
    (8, 'Самара'),
    (9, 'Ростов-на-Дону'),
    (10, 'Уфа');

INSERT INTO tax_param (id, city_id, from_hp_car, to_hp_car, from_production_year_car, to_production_year_car, rate) VALUES
    (1, 1, 100, 200, 2000, 2022, 0.05),
    (2, 2, 80, 150, 2010, 2022, 0.04),
    (3, 3, 120, 250, 2005, 2022, 0.06),
    (4, 4, 90, 180, 2008, 2022, 0.045),
    (5, 5, 70, 140, 2015, 2022, 0.03),
    (6, 6, 110, 220, 2007, 2022, 0.055),
    (7, 7, 95, 180, 2012, 2022, 0.042),
    (8, 8, 75, 160, 2018, 2022, 0.035),
    (9, 9, 130, 260, 2006, 2022, 0.07),
    (10, 10, 85, 170, 2013, 2022, 0.048);

INSERT INTO auto (id, city_id, tax_id, name, horse_power, production_year, tax) VALUES
    (1, 1, 1, 'Audi A4', 150, 2019, 7.5),
    (2, 2, 2, 'BMW X5', 200, 2018, 8.0),
    (3, 3, 3, 'Ford Focus', 120, 2020, 6.0),
    (4, 4, 4, 'Toyota Camry', 170, 2017, 7.8),
    (5, 5, 5, 'Volkswagen Golf', 90, 2021, 4.5),
    (6, 6, 6, 'Mercedes-Benz C-Class', 180, 2016, 9.0),
    (7, 7, 7, 'Hyundai Sonata', 140, 2019, 6.3),
    (8, 8, 8, 'Nissan Qashqai', 160, 2020, 6.8),
    (9, 9, 9, 'Kia Rio', 130, 2018, 7.7),
    (10, 10, 10, 'Mazda CX-5', 150, 2017, 7.2);

